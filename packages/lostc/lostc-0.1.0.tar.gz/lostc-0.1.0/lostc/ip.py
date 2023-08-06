def ip_in_range(ip, range):
    floor, ceil = range
    return ip_full(ceil) >= ip_full(ip) >= ip_full(floor)


def ip_full(ip):
    return ".".join([item.zfill(3) for item in ip.split(".")])


if __name__ == "__main__":
    print(ip_in_range("192.168.199.2", ("192.168.198.1", "192.168.198.100")))
    print(ip_in_range("192.168.199.2", ("192.168.199.1", "192.168.199.100")))
    print(ip_in_range("192.168.199.2", ("192.168.199.50", "192.168.199.100")))
    print(ip_in_range("192.168.199.2", ("192.168.199.100", "192.168.199.1")))
    print(ip_in_range("192.168.199.1", ("192.168.199.1", "192.168.199.100")))
    print(ip_in_range("192.168.199.100", ("192.168.199.1", "192.168.199.100")))
