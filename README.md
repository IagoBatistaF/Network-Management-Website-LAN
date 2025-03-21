# **Check Devices Script**

This Python script, `check_devices.py`, performs a network-wide scan by pinging a range of IP addresses, performing ARP scans, and gathering device information using commands like nbtstat and nmap. It stores the results in a text file, and optionally, integrates with a SQLite database to store information about devices that are discovered.

## **Features**
+ **Ping Sweep:** Pings all devices within a specified IP range to check if they are online or offline.

+ **ARP Scan:** Scans for MAC addresses on the network and determines if the address is static or dynamic.

+ **NBTStat Lookup:** Retrieves the NetBIOS name of devices with valid MAC addresses.

+ **Nmap Integration:** Uses Nmap to perform a detailed network scan, retrieving MAC addresses and device names.

+ **Results File:** Saves the results to a .txt file in the format:

```

IP ; Status ; MAC ; User ; Static or Dynamic ; Nmap Device Name

```

+ **SQLite Integration:** _**Optionally**_ stores devices with MAC addresses in an SQLite database.

## **Prerequisites**

Before using the script, make sure you have the following installed:



+ **Python 3.x**

+  **Python Libraries:** You can install the required libraries using pip:

```
pip install ping3 scapy
```

+ **Nmap:** Make sure Nmap is installed and can be accessed from C:\Program Files (x86)\Nmap. You can download Nmap from https://nmap.org/download.html.

+ **_SQLite (Optional):_** _If you're using the SQLite integration to store device information, Python comes with the sqlite3 module by default, so no additional setup is needed._

## **How It Works**

+ **Ping Sweep:** The script will first perform a ping sweep across the specified IP range (10.1.73.0/24 by default) and store whether each IP is online or offline.

+ **ARP Scan:** It then performs an ARP scan on the network to retrieve MAC addresses associated with the IPs.

+ **NBTStat Lookup:** For IP addresses with valid MAC addresses, the script runs the nbtstat command to retrieve the device's NetBIOS name.

+ **Nmap Scan:** The script also runs an Nmap scan to gather further information, such as device names and MAC addresses, and checks whether the IP addresses have static or dynamic MAC addresses.

+ **Results File:** The results are written to a file called arp_ping_nmap_results.txt in the following format:
```

10.1.73.88 ; Online ; AA:AA:AA:AA:AA:AA (Dell) ; USER-122 ; Static ; Nmap Device Name

```
+ **_SQLite Database (Optional):_** _If enabled, the script will store the details of devices with valid MAC addresses in an SQLite database, with each row containing the IP, device name, and MAC._

## Running the Script:

The script can be executed directly from the command line:
```

python check_devices.py

```
+ **Configuring IP Range:** By default, the script scans the IP range 10.1.73.0/24. You can modify the range by updating the start_ip, end_ip, and ip_range variables in the main() function.

+ **Nmap Configuration:** The script assumes that Nmap is installed in C:\Program Files (x86)\Nmap. If Nmap is installed in a different directory, update the nmap_path variable in the script to reflect the correct location.

### Output Format

The results are saved in a file called arp_ping_nmap_results.txt and follow this format:

```

IP ; Status ; MAC ; User ; Static or Dynamic ; Nmap Device Name

```
1. **IP:** The IP address of the device.

2. **Status:** Either "Online" or "Offline" depending on the ping result.

3. **MAC:** The MAC address of the device (or "No MAC" if unavailable).

4. **User:** The NetBIOS name retrieved from the nbtstat command (if available).

5. **Static or Dynamic:** Indicates whether the MAC address is static or dynamic.

6. **Nmap Device Name:** Device name returned by Nmap (if available).

### Example Output

```
10.1.73.88 ; Online ; AA:AA:AA:AA:AA:AA (Dell) ; USER-122 ; Static ; 
10.1.73.89 ; Offline ; No MAC ;  ; Unknown ; 
10.1.73.90 ; Online ; BB:BB:BB:BB:BB:BB (Vendor Name) ; HomeWifi ; Dynamic ; Router
```
## **Customization**

+ **Adjusting the IP Range:** Modify the IP range in the main() function by setting the start_ip, end_ip, and ip_range variables.

+ **Adjusting the Nmap Path:** Ensure the Nmap installation path is correctly set in the nmap_path variable.

## **Known Issues**

+ **nbtstat Performance:** The nbtstat command can be slow for larger networks. To optimize this, the script only runs nbtstat if a valid MAC address is found during the ARP scan.

+ **Nmap Path:** Ensure that Nmap is installed in the correct directory (C:\Program Files (x86)\Nmap). If not, the script will not be able to run the Nmap scan properly.
