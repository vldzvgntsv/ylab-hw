import re


def domain_name(url):
    pattern = r'(https?://)?(www.)?([A-Za-z_0-9-]+).*'
    return re.search(pattern, url).group(3)


assert domain_name("https://www.cnet.com") == "cnet"
assert domain_name("http://github.com/carbonfive/raygun") == "github"
assert domain_name("http://www.zombie-bites.com") == "zombie-bites"
assert domain_name("http://google.com") == "google"
assert domain_name("http://google.co.jp") == "google"
assert domain_name("www.xakep.ru") == "xakep"
assert domain_name("https://youtube.com") == "youtube"

url = input()
print(domain_name(url))
