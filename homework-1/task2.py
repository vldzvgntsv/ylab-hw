def int32_to_ip(int32):
    bin_ip: str = f'{int32:b}'.zfill(32)
    ip_list: list = []
    i: int = 0
    while i < 32:
        ip_list.append(str(int(bin_ip[0+i:8+i], 2)))
        i += 8
    ip = '.'.join(ip_list)
    return ip


assert int32_to_ip(2154959208) == "128.114.17.104"
assert int32_to_ip(0) == "0.0.0.0"
assert int32_to_ip(2149583361) == "128.32.10.1"


int32 = int(input())
print(int32_to_ip(int32))
