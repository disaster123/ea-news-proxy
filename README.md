# News Proxy

This project provides a news proxy service that intercepts and manages requests to the `ec.forexprostools.com` domain. It uses a self-signed SSL certificate for secure communication and supports **ONLY** Investing.com.

## Installation

1. **Download the Executable:**

   Visit the [Releases page](https://github.com/disaster123/ea-news-proxy/releases) on GitHub and download the latest executable file (`news-proxy.exe`). The file is available for direct download.

2. **Create a Directory:**

   Create a new directory where you will place the downloaded executable file and where the SSL certificates will be generated. For example, you might create a directory named `news-proxy` on your desktop or any other location.

3. **Move the Executable:**

   After downloading the `news-proxy.exe`, move it into the directory you created.

4. **Run the Executable:**

   Navigate to the directory containing `news-proxy.exe` and run the executable by double-clicking on it. On the first run, the server will automatically generate the required SSL certificates (`server.cert` and `private.key`) if they do not already exist. The server will start on port 443 with HTTPS enabled by default.

## Setup via Hosts File on Windows

To redirect requests from `ec.forexprostools.com` to your local proxy server, modify the hosts file on your Windows machine:

1. **Open Notepad as Administrator:**

   Search for Notepad, right-click on it, and select "Run as administrator."

2. **Edit the Hosts File:**

   Open the hosts file located at:

   ```
   C:\Windows\System32\drivers\etc\hosts
   ```

3. **Add the Following Line:**

   Add this line to the end of the file:

   ```
   127.0.0.1 ec.forexprostools.com
   ```

4. **Save the File:**

   Save the changes and close Notepad.

This configuration ensures that requests to `ec.forexprostools.com` are redirected to your local proxy server.

## Caveats

- **Inaccessible via Browser:** The site `ec.forexprostools.com` will no longer be accessible directly via your browser. All traffic to this site will be routed through the proxy server.

- **Limited Support:** The proxy supports **ONLY** Investing.com. Other data sources or functionalities may not work correctly.

