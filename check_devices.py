import ipaddress
from ping3 import ping
from scapy.all import ARP, Ether, srp

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

def get_arp_table_scapy(ip_range):
    arp = ARP(pdst=ip_range)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp

    result = srp(packet, timeout=3, verbose=0)[0]
    arp_entries = [(res.psrc, res.hwsrc) for sent, res in result]
    return arp_entries

def write_results_to_file(results, filename):
    with open(filename, 'w') as file:
        for ip, status in results:
            file.write(f"{ip} ; {status}\n")

def main():
    start_ip = '10.1.73.1'
    end_ip = '10.1.73.255'

    # Perform a ping sweep
    ping_results = ping_sweep(start_ip, end_ip)

    # Perform an ARP scan
    ip_range = "10.1.73.1/24"  # Adjust as needed
    arp_entries = get_arp_table_scapy(ip_range)

    # Combine results
    combined_results = []
    for ip, status in ping_results:
        mac = "Unknown"
        static_or_dynamic = "Dynamic"  # You might need to implement logic to determine this
        # Check if IP is in ARP entries
        for arp_ip, arp_mac in arp_entries:
            if ip == arp_ip:
                mac = arp_mac
                static_or_dynamic = "Static"  # Example assumption; adjust as needed
        combined_results.append((ip, status, mac, static_or_dynamic))

    # Specify the output filename
    output_file = "arp_ping_results.txt"
    with open(output_file, 'w') as file:
        for ip, status, mac, static_or_dynamic in combined_results:
            file.write(f"{ip} ; {status} ; {mac} ; {static_or_dynamic}\n")

    print(f"\nResults saved in {output_file}.")

if __name__ == "__main__":
    main()
