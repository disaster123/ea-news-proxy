# News Proxy

This project provides a news proxy service that intercepts and manages requests to `ec.forexprostools.com` and `nfs.faireconomy.media` domain. It uses a self-signed SSL certificate for secure communication.

## Disclaimer

**Disclaimer:** This script is a quick proof of concept and may not be fully secure or optimized. Use it at your own risk. The author is not responsible for any harm, data loss, or problems caused by the use of this software.

## Installation

1. **Download the Release Archive:**

   Visit the [Releases page](https://github.com/disaster123/ea-news-proxy/releases) on GitHub and download the latest release archive (`news-proxy-release.zip`). This file contains the executable, `README.txt`, and the startup batch script.

2. **Extract the Archive:**

   After downloading the `news-proxy-release.zip`, extract the contents to a new directory. This will create a folder with `news-proxy.exe`, `README.txt`, and `start-in-loop.bat`.

   - On Windows, you can usually right-click the `.zip` file and select "Extract All..." or use a tool like [7-Zip](https://www.7-zip.org/).

3. **Read the README.txt:**

   Inside the extracted folder, open the `README.txt` file for easy-to-read instructions on using the proxy. For a better reading experience, you might prefer viewing the Markdown version of this file directly on GitHub [here](https://github.com/disaster123/ea-news-proxy/blob/main/README.md).

4. **Run the Executable:**

   Navigate to the directory where you extracted the files and run the `news-proxy.exe` by double-clicking on it. On the first run, the server will automatically generate the required SSL certificates (`server.cert` and `private.key`) if they do not already exist. The server will start on port 443 with HTTPS enabled by default.

5. **Windows SmartScreen Warning:**

   On the first start of the `.bat` or `.exe`, Windows SmartScreen might show a warning. This happens because the file was downloaded from the internet. To proceed, click on "More info" and then "Run anyway" to allow the program to execute.

## Setup via Hosts File on Windows

To redirect requests from `ec.forexprostools.com` and `nfs.faireconomy.media` to your local proxy server, modify the hosts file on your Windows machine:

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
   127.0.0.1 nfs.faireconomy.media
   ```

4. **Save the File:**

   Save the changes and close Notepad.

This configuration ensures that requests to `ec.forexprostools.com` and `nfs.faireconomy.media` are redirected to your local proxy server.

## Add to Windows Autostart

To automatically start the proxy when your computer boots, create a shortcut to the `start-in-loop.bat` file and place it in the Windows startup folder:

1. **Create a Shortcut for `start-in-loop.bat`:**

   Right-click on the `start-in-loop.bat` file, select "Create shortcut."

2. **Move the Shortcut to the Startup Folder:**

   Press `Win + R`, type `shell:startup`, and press Enter. This will open the Startup folder.

3. **Copy the Shortcut:**

   Drag the shortcut you created earlier into this folder. The proxy will now start automatically when you log in to Windows.

## Advantages of Using Investing.com

- **Auto-detection of News Timezones:** Investing.com provides the added advantage of automatically detecting the correct timezones for news events, making it easier to keep track of economic news in your local time.

