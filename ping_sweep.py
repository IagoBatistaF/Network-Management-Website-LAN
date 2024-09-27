import ipaddress
import subprocess
from ping3 import ping
from scapy.all import ARP, Ether, srp

# Ping sweep function
def ping_sweep(start_ip, end_ip):
    results = []
    current_ip = ipaddress.ip_address(start_ip)
    end_ip = ipaddress.ip_address(end_ip)

    while current_ip <= end_ip:
        print(f"Pinging {current_ip}...")  # Indicator for the current IP
        response = ping(str(current_ip), timeout=1)
        status = "Online" if response is not None else "Offline"
        results.append((str(current_ip), status))  # Store the result
        current_ip += 1

    return results

# ARP scan function
def get_arp_table_scapy(ip_range):
    print(f"Performing ARP scan for range {ip_range}...")  # ARP scan indicator
    arp = ARP(pdst=ip_range)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp

    result = srp(packet, timeout=3, verbose=0)[0]
    arp_entries = [(res.psrc, res.hwsrc) for sent, res in result]  # Extract IP and MAC addresses
    return arp_entries

# Function to get user or device name using 'nbtstat -A <IP>' only if MAC exists
def get_nbtstat_user(ip):
    try:
        print(f"Running nbtstat for {ip}...")  # nbtstat execution indicator
        # Run the 'nbtstat -A <IP>' command
        result = subprocess.run(['nbtstat', '-A', ip], capture_output=True, text=True)
        
        # Search for the first EXCLUSIVO (UNIQUE) entry in the output
        for line in result.stdout.splitlines():
            if '<00>' in line and 'EXCLUSIVO' in line:
                return line.split()[0]  # Extract the NetBIOS name (before <00>)
        
        return ""  # If no name is found, return an empty string
    except Exception as e:
        return ""  # Return empty string if any issues occur

# Function to get details from nmap -sP with specific directory
def get_nmap_scan(ip_range):
    nmap_path = r"C:\Program Files (x86)\Nmap"  # Path to Nmap
    print(f"Running Nmap scan from {nmap_path} for range {ip_range}...")  # Nmap scan indicator
    nmap_data = {}
    try:
        # Run the 'nmap -sP <IP Range>' command from the specified directory
        result = subprocess.run(['nmap', '-sP', ip_range], capture_output=True, text=True, cwd=nmap_path)
        
        current_ip = ""
        for line in result.stdout.splitlines():
            if "Nmap scan report for" in line:
                current_ip = line.split()[-1]
                nmap_data[current_ip] = {"device_name": "", "mac": ""}
            elif "MAC Address" in line and current_ip:
                mac_info = line.split(" ", 2)
                mac = mac_info[1] if len(mac_info) > 1 else ""
                device_name = mac_info[2].strip("()") if len(mac_info) > 2 else ""
                nmap_data[current_ip]["mac"] = mac
                nmap_data[current_ip]["device_name"] = device_name
        return nmap_data
    except Exception as e:
        print(f"Error running Nmap: {str(e)}")  # Nmap error indicator
        return {}  # Return an empty dictionary if there's an error

# Writing results to file
def write_results_to_file(results, filename):
    print(f"Writing results to file: {filename}...")  # Writing to file indicator
    with open(filename, 'w') as file:
        for ip, status, mac, user, static_or_dynamic, nmap_device_name in results:
            file.write(f"{ip} ; {status} ; {mac} ; {user} ; {static_or_dynamic} ; {nmap_device_name}\n")

# Main function to run ping sweep, ARP scan, NBTStat, and Nmap
def main():
    start_ip = '10.1.73.1'
    end_ip = '10.1.73.255'
    ip_range = "10.1.73.0/24"  # Define the network range

    print(f"Starting ping sweep from {start_ip} to {end_ip}...")  # Ping sweep start indicator
    # Perform a ping sweep
    ping_results = ping_sweep(start_ip, end_ip)

    print("Ping sweep completed.\n")  # Ping sweep end indicator

    # Perform an ARP scan
    arp_entries = get_arp_table_scapy(ip_range)

    print("ARP scan completed.\n")  # ARP scan end indicator

    # Perform an Nmap scan
    nmap_data = get_nmap_scan(ip_range)

    print("Nmap scan completed.\n")  # Nmap scan end indicator

    # Combine results from ping, ARP, nbtstat, and Nmap
    combined_results = []
    for ip, status in ping_results:
        mac = "No MAC"  # Default when no MAC is found
        static_or_dynamic = "Unknown"  # Default assumption for ARP entry
        user = ""
        nmap_device_name = ""

        # Check if the IP address was found in the ARP table
        for arp_ip, arp_mac in arp_entries:
            if ip == arp_ip:
                mac = arp_mac
                static_or_dynamic = "Static"  # Example assumption for ARP entry

        # Check if the IP address was found in the Nmap scan
        if ip in nmap_data:
            if nmap_data[ip]["mac"]:
                mac = nmap_data[ip]["mac"]
            nmap_device_name = nmap_data[ip]["device_name"]

        # Only run 'nbtstat' if MAC address is found
        if mac != "No MAC":
            user = get_nbtstat_user(ip)

        combined_results.append((ip, status, mac, user, static_or_dynamic, nmap_device_name))

    # Save the results to a file
    output_file = "arp_ping_nmap_results.txt"
    write_results_to_file(combined_results, output_file)

    print(f"\nResults saved in {output_file}.")

if __name__ == "__main__":
    main()
