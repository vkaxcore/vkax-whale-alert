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

### **Step 6: Set Up the Python Script**

1. **Create the Python Script**:

   Navigate to the directory where you want to store the script. For example, let's store it in `/home/ubuntu/`.

   ```bash
   nano /home/ubuntu/create_rss_feed.py
   ```

   Copy the Python script you provided earlier into this file and save it (`Ctrl + O`, then `Ctrl + X` to exit).

2. **Run the Python Script**:

   Before running the script, make sure the VKAX daemon is running and fully synced. Then, run the script with:

   ```bash
   python3 /home/ubuntu/create_rss_feed.py
   ```

   The script will now generate an RSS feed based on the last 100 blocks that contain transactions exceeding 10,000,000 VKAX.

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

### **Step 9: Done!**

You should now have VKAX built from source and the Python script set up and running on your Ubuntu 22.04 system. You can periodically check the generated RSS feed for high-value transactions.
