Here’s a detailed step-by-step guide to build VKAX from source on Ubuntu 22.04 and then install the script provided. This will help you set up everything from compiling VKAX to running the Python script.

### **Step 1: Install Dependencies**

First, you need to install some essential dependencies for building VKAX on Ubuntu.

1. **Update your system and install necessary dependencies**:

   Open a terminal and run the following commands:

   ```bash
   sudo apt update
   sudo apt upgrade -y
   sudo apt install -y build-essential libtool autotools-dev automake pkg-config libssl-dev libboost-all-dev libevent-dev bsdmainutils libzmq3-dev libdb-dev libdb++-dev libminiupnpc-dev libsodium-dev libnatpmp-dev libprotobuf-dev protobuf-compiler libqt5gui5 libqt5core5a libqt5dbus5 libqt5widgets5 qtbase5-dev qtchooser qtbase5-dev-tools libqt5webkit5-dev libprotobuf-dev libunbound-dev
   ```

2. **Install additional tools for Git and networking**:

   ```bash
   sudo apt install -y git curl
   ```

### **Step 2: Clone the VKAX Repository**

1. **Clone the VKAX source code from GitHub**:

   Run the following command to clone the VKAX repository:

   ```bash
   git clone https://github.com/vkaxcore/vkax.git
   ```

2. **Navigate to the VKAX directory**:

   ```bash
   cd vkax
   ```

### **Step 3: Build VKAX**

1. **Run autogen** to prepare the build system:

   ```bash
   ./autogen.sh
   ```

2. **Configure the build**:

   Set up the build configuration by running the following command:

   ```bash
   ./configure
   ```

3. **Compile the VKAX code**:

   Once configured, run `make` to compile VKAX:

   ```bash
   make
   ```

4. **Install VKAX**:

   After building, install VKAX by running:

   ```bash
   sudo make install
   ```

### **Step 4: Set Up VKAX Core Daemon**

1. **Create a directory for your VKAX data**:

   ```bash
   mkdir ~/.vkaxcore
   ```

2. **Create a configuration file for VKAX**:

   Create the `vkax.conf` file in the `~/.vkaxcore/` directory:

   ```bash
   nano ~/.vkaxcore/vkax.conf
   ```

   Add the following configuration (you can adjust the settings as needed):

   ```
   rpcuser=daemonrpcuser
   rpcpassword=daemonrpcpassword
   rpcport=11111
   rpcallowip=127.0.0.1
   daemon=1
   server=1
   ```

   Save the file by pressing `Ctrl + O`, then exit by pressing `Ctrl + X`.

3. **Start VKAX Daemon**:

   Start the VKAX daemon with the following command:

   ```bash
   vkaxd
   ```

   This will run the VKAX daemon in the background and begin syncing the blockchain.

4. **Verify the VKAX Daemon is Running**:

   To check if VKAX is running correctly, use:

   ```bash
   vkax-cli getinfo
   ```

   This should show information about your VKAX node.

### **Step 5: Install Python and Script Dependencies**

1. **Install Python 3 and pip**:

   Run the following command to install Python and `pip`:

   ```bash
   sudo apt install -y python3 python3-pip
   ```

2. **Install Requests and Other Python Libraries**:

   Install the necessary Python libraries for your script:

   ```bash
   pip3 install requests
   ```

Certainly! Here is the updated **Step 6** with instructions to download the script directly from GitHub instead of manually creating it:

---

### **Step 6: Set Up the Python Script**

1. **Download the Python Script**:

   Instead of manually copying the script, you can download it directly from the GitHub repository.

   Run the following command to download the `vkax_rss_feed.py` script:

   ```bash
   curl -o /home/ubuntu/vkax_rss_feed.py https://raw.githubusercontent.com/realsetvin/vkax-whale-alert/main/vkax_rss_feed.py
   ```

   This will download the script and save it as `vkax_rss_feed.py` in the `/home/ubuntu/` directory.

2. **Install Requests and Other Python Libraries**:

   If you haven’t already, install the necessary Python libraries for the script. In particular, you’ll need the `requests` module, which you can install with:

   ```bash
   pip3 install requests
   ```

3. **Run the Python Script**:

   Now that the script is downloaded, you can run it with:

   ```bash
   python3 /home/ubuntu/vkax_rss_feed.py
   ```

   The script will start fetching transactions from the VKAX blockchain and create an RSS feed with transactions over the 1,000,000 VKAX threshold.

---

### **Step 7: Automate the Script (Optional)**

To run the script automatically on a regular basis, you can use `cron` jobs.

1. **Edit crontab**:

   Open the crontab editor:

   ```bash
   crontab -e
   ```

2. **Add a cron job** to run the script every hour (or adjust as needed):

   Add the following line to run the script every hour:

   ```bash
   0 * * * * /usr/bin/python3 /home/ubuntu/create_rss_feed.py
   ```

   This will execute the script every hour. Save and close the crontab (`Ctrl + O`, then `Ctrl + X`).

### **Step 8: Monitoring and Debugging**

1. **Check Logs**:

   To see the output of the Python script and debug any issues, check the generated log files or output.

   For example, you can check if the script is producing any errors in the system log:

   ```bash
   tail -f /var/log/syslog
   ```

2. **Verify VKAX Daemon**:

   You can monitor the progress of your VKAX node by checking its status:

   ```bash
   vkax-cli getblockcount
   ```

### **Step 9: Distribute!**
To read the RSS feed that the Python script generates, you can use several methods depending on your preferences and available tools. Here are the most common ways to read an RSS feed:

### **1. Use a Web Browser**

Most modern web browsers (like Chrome, Firefox, or Edge) can open and display RSS feeds directly.

- **Open the RSS feed in your browser**: 
   - Navigate to the location where the RSS feed file is saved (e.g., `vkax_high_value_transactions.xml`).
   - If the file is hosted on a web server (like your own server), you can open the URL to the RSS feed (e.g., `https://your-site-url.com/vkax_high_value_transactions.xml`).
   - The browser will display the RSS feed in XML format. It won't be nicely formatted but you can still view the data.
   
   **Note**: Some browsers, like Firefox, may offer a basic visual interface for reading RSS feeds. For a better experience, you might want to use an RSS reader (described below).

### **2. Use an RSS Reader**

There are many dedicated RSS readers available that will fetch, display, and update your RSS feeds automatically. These can help you read RSS feeds in a more user-friendly format.

- **Popular RSS readers include**:
   - **Feedly**: A cloud-based RSS reader, accessible via browser and mobile apps. You can simply add the URL of your RSS feed to start reading.
   - **RSSOwl**: A free, desktop-based RSS reader that works on Windows, Linux, and macOS.
   - **QuiteRSS**: Another free desktop RSS reader with a simple interface and useful features.

   To use any of these:
   1. **Add the feed URL**: If the RSS feed is hosted online, use the URL where the feed is located (e.g., `https://your-site-url.com/vkax_high_value_transactions.xml`).
   2. **View the feed**: The RSS reader will show the feed in an organized way, typically with titles, timestamps, and links to each transaction.

### **3. Use Command Line Tools**

If you are on a Linux-based system and prefer the command line, there are tools you can use to fetch and display RSS feed data.

- **Using `w3m`** (a text-based browser):
   1. Install `w3m` if it's not already installed:

      ```bash
      sudo apt install w3m
      ```

   2. Use `w3m` to open the RSS feed in the terminal:

      ```bash
      w3m /path/to/vkax_high_value_transactions.xml
      ```

   This will render the XML file in a text-based browser.

- **Using `rss2email`** (a command-line RSS reader):

   1. Install `rss2email`:

      ```bash
      sudo apt install rss2email
      ```

   2. Fetch the feed directly from the file or URL:

      ```bash
      rss2email /path/to/vkax_high_value_transactions.xml
      ```

   Alternatively, if you have a URL for the feed:

      ```bash
      rss2email https://your-site-url.com/vkax_high_value_transactions.xml
      ```

### **4. Programmatically Read the RSS Feed**

If you'd like to programmatically access and process the RSS feed (for example, to display it in a web application or integrate with another service), you can parse the XML file using a programming language like Python.

Here’s an example of how to read an RSS feed in Python:

```python
import feedparser

# URL to the RSS feed
rss_feed_url = "https://your-site-url.com/vkax_high_value_transactions.xml"

# Parse the RSS feed
feed = feedparser.parse(rss_feed_url)

# Display each entry in the feed
for entry in feed.entries:
    print(f"Title: {entry.title}")
    print(f"Link: {entry.link}")
    print(f"Description: {entry.description}")
    print(f"Published: {entry.published}")
    print("-" * 40)
```

### **5. Use an RSS to Email Service**

If you prefer to receive the RSS feed updates directly in your email, you can use an online service to convert the RSS feed into email notifications.

- **Feedly** and other RSS services often provide email notifications.
- **Mailbrew**: A service that allows you to receive RSS updates as daily email summaries.

### **6. Automate RSS Feed Checks (Optional)**

If you want to automate checking the RSS feed, you can set up a cron job on your server or computer to periodically fetch the feed and run the necessary logic.

For example, set up a cron job that runs every hour to check for new transactions in the RSS feed.

---

Choose the method that best fits your needs. If you want automatic updates and notifications, an RSS reader or email service is recommended. If you prefer reading it directly from your system, the command line or browser methods work well.
