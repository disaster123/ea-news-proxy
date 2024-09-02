from http.server import HTTPServer, BaseHTTPRequestHandler
import ssl
import requests
import socket
import socket
import time
import sys
import dns.resolver
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization as crypto_serialization

# File paths for the certificate and key
CERT_FILE = 'server.cert'
KEY_FILE = 'private.key'
cache = {}
dns_cache = {}
hostname = "ec.forexprostools.com"

class Unbuffered(object):
   def __init__(self, stream):
       self.stream = stream
   def write(self, data):
       self.stream.write(data)
       self.stream.flush()
   def writelines(self, datas):
       self.stream.writelines(datas)
       self.stream.flush()
   def __getattr__(self, attr):
       return getattr(self.stream, attr)

def update_real_ip(hostname):
    ip_address = get_ip_from_hostname(hostname, '8.8.8.8')
    
    print(f"Hostname: {hostname} points to: {ip_address}")
    
    override_dns(hostname, ip_address)

def get_ip_from_hostname(hostname, dns_server):
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [dns_server]
    
    try:
        # DNS-Abfrage für A-Record (IPv4)
        answer = resolver.resolve(hostname, 'A')
        
        # Die erste gefundene IP-Adresse zurückgeben
        return str(answer[0])
    except dns.resolver.NXDOMAIN:
        return "Der Hostname konnte nicht aufgelöst werden (NXDOMAIN)."
    except dns.resolver.Timeout:
        return "Die DNS-Abfrage hat den Timeout überschritten."
    except dns.resolver.NoNameservers:
        return "Kein Nameserver konnte erreicht werden."
    except dns.resolver.NoAnswer:
        return "Die DNS-Abfrage lieferte keine Antwort."

# Capture a dict of hostname and their IPs to override with
def override_dns(domain, ip):
    global dns_cache
    dns_cache[domain] = ip

prv_getaddrinfo = socket.getaddrinfo

# Override default socket.getaddrinfo() and pass ip instead of host
# if override is detected
def new_getaddrinfo(*args):
    global dns_cache
    if args[0] in dns_cache:
        print("Forcing FQDN: {} to IP: {}".format(args[0], dns_cache[args[0]]))
        return prv_getaddrinfo(dns_cache[args[0]], *args[1:])
    else:
        return prv_getaddrinfo(*args)

def fetch_webpage(url):
    headers = {
        'User-Agent': (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        ),
        'Accept': (
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
        ),
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Referer': 'https://www.google.com/',  # Setzt den Referer, um einen normalen Seitenfluss zu simulieren
        'Cache-Control': 'max-age=0',
        'DNT': '1',  # Do Not Track Header
    }
     
    try:
        response = requests.get(url, headers=headers, timeout=5)
        status_code = response.status_code
        content = response.text
        
        return status_code, content
    except requests.RequestException as e:
        # Fehlerbehandlung bei Netzwerkproblemen oder HTTP-Fehlern
        return None, str(e)

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        global cache
        global hostname
        code = 403
        text = "no data"
        requested_url = self.path

        in_cache = False
        in_timeout = False
        if cache.get(requested_url, {}).get('content', '') != '':
            if (cache.get(requested_url, {}).get('time', 0) + (5*60*60)) < time.time():
                in_timeout = True

            in_cache = True

        if not in_cache or in_timeout:
            print(f"Refresh Cache: {requested_url}")
            update_real_ip(hostname)
            code, text = fetch_webpage("https://" + hostname + requested_url)

            if code == 200:
                print(f"Update Cache: {requested_url}")
                cache.update( { requested_url: { 'content': text, 'time': time.time() } } )
            else:
                # do nothing - we just keep the old content in cache - so it can still be served below
                print(f"ERROR: Updating Cache: use old stale cache Code: {code}")

        if cache.get(requested_url, {}).get('content', '') != '':
            print(f"Use Cache: {requested_url}")
            text = cache.get(requested_url, {}).get('content', '')
            code = 200
        else:
            # keep original status code
            print(f"No Cache found: {requested_url}")

        self.send_response(code)
        self.end_headers()
        self.wfile.write(text.encode())


class MyHTTPServer(HTTPServer):
    def server_bind(self):
        # Call the original server_bind method
        super().server_bind()
        # Set the listen backlog
        self.socket.listen(25)

def create_self_signed_cert(cert_file: str, key_file: str):
    # Generate a private key
    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

    # Generate a self-signed certificate
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, u"US"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"California"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, u"San Francisco"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"Fake Company"),
        x509.NameAttribute(NameOID.COMMON_NAME, u"news-proxy.fake"),
    ])

    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        x509.datetime.datetime.utcnow()
    ).not_valid_after(
        x509.datetime.datetime.utcnow() + x509.datetime.timedelta(days=365)
    ).sign(key, hashes.SHA256())

    # Write the private key to a file
    with open(key_file, "wb") as f:
        f.write(
            key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            )
        )

    # Write the certificate to a file
    with open(cert_file, "wb") as f:
        f.write(
            cert.public_bytes(
                encoding=serialization.Encoding.PEM
            )
        )

    print(f"Created self-signed certificate and private key: {cert_file}, {key_file}")

def ensure_certificates():
    if not os.path.exists(CERT_FILE) or not os.path.exists(KEY_FILE):
        create_self_signed_cert(CERT_FILE, KEY_FILE)
    else:
        print(f"Certificate and key already exist: {CERT_FILE}, {KEY_FILE}")


sys.stdout = Unbuffered(sys.stdout)


ensure_certificates()

httpd = MyHTTPServer(('localhost', 443), SimpleHTTPRequestHandler)

httpd.socket = ssl.wrap_socket (httpd.socket,
        keyfile=KEY_FILE,
        certfile=CERT_FILE, server_side=True)

# install override DNS
socket.getaddrinfo = new_getaddrinfo

httpd.serve_forever()

