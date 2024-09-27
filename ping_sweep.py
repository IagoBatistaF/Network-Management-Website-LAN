import ipaddress
from ping3 import ping

def ping_sweep(start_ip, end_ip):
    reachable_hosts = []

    # Generate IP addresses from start to end
    current_ip = ipaddress.ip_address(start_ip)
    end_ip = ipaddress.ip_address(end_ip)

    while current_ip <= end_ip:
        response = ping(str(current_ip), timeout=1)  # Send a ping
        if response is not None:
            reachable_hosts.append(str(current_ip))  # If ping succeeds, add to list
        current_ip += 1  # Move to the next IP address

    return reachable_hosts

def main():
    start_ip = '10.1.73.1'
    end_ip = '10.1.73.255'

    reachable_hosts = ping_sweep(start_ip, end_ip)

    if reachable_hosts:
        print("Reachable devices:")
        for host in reachable_hosts:
            print(host)
    else:
        print("No reachable devices found.")

if __name__ == "__main__":
    main()
