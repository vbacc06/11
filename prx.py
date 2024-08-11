import requests
import threading
import os
from colorama import Fore, init
from concurrent.futures import ThreadPoolExecutor

# Initialize Colorama
init(autoreset=True)

# URLs for proxy sources
proxy_urls = [
    'https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all',
    'https://api.proxyscrape.com/v2/?request=getproxies&protocol=https&timeout=10000&country=all',
    'https://proxyspace.pro/https.txt',
    'https://proxyspace.pro/socks4.txt',
    'https://proxyspace.pro/socks5.txt',
    'https://api.openproxylist.xyz/http.txt',
    'https://api.proxyscrape.com/v2/?request=displayproxies',
    'http://rootjazz.com/proxies/proxies.txt',
    'https://multiproxy.org/txt_all/proxy.txt',
    'https://proxy-spider.com/api/proxies.example.txt',
]

# File paths
scan_output_file = 'list.txt'
check_output_file = 'proxy.txt'

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def download_and_save_proxies(urls, output_file):
    """ Download proxies from given URLs and save them to output_file. """
    all_proxies = set()
    for url in urls:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                proxies = response.text.splitlines()
                for proxy in proxies:
                    proxy = proxy.strip()
                    if proxy:
                        all_proxies.add(proxy)
                print(f"\033[1;31m> \033[1;32mScarn Proxy Successfully \033[1;31m[\033[1;33mHenry Proxy\033[1;31m]")
            else:
                print(f"\033[1;32m> \033[1;31mFailed to download proxies from {url}")
        except Exception as e:
            print(f"\033[1;31m> \033[1;37mError downloading proxies from \033[1;31m{url}\033[1;37m: \033[1;32m{e}")
    
    with open(output_file, 'w') as file:
        for proxy in all_proxies:
            file.write(proxy + '\n')

    print(f"> Total Proxy Count: [{len(all_proxies)}] proxies")
    print(f"> Proxies saved to {output_file}")

def scan_proxies():
    """ Scan proxies and save them to list.txt. """
    clear_console()
    print(f"\033[1;31m> \033[1;37mScanning proxies \033[1;30m...")
    download_and_save_proxies(proxy_urls, scan_output_file)

class Proxy:
    def __init__(self, proxy):
        self.proxy = proxy
    
    def is_valid(self, timeout=5):
        try:
            response = requests.get('http://www.google.com', proxies={'http': self.proxy, 'https': self.proxy}, timeout=timeout)
            return response.status_code == 200
        except:
            return False
    
def check_proxies(input_file, timeout, threads):
    """ Check the proxies from the input file and save valid ones to proxy.txt. """
    clear_console()
    print(f"\033[1;31m> \033[1;37mChecking proxies from \033[1;31m{input_file}...")
    
    with open(input_file, 'r') as file:
        proxies = [line.strip() for line in file if line.strip()]
    
    valid_proxies = []
    
    def check_proxy(proxy):
        p = Proxy(proxy)
        if p.is_valid(timeout):
            valid_proxies.append(proxy)
            print(f"\033[1;31m> \033[1;37mProxies Are Active: \033[1;32m{proxy}")
    
    with ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(check_proxy, proxies)
    
    with open(check_output_file, 'w') as file:
        for proxy in valid_proxies:
            file.write(proxy + "\n")
    
    print(f"\033[1;31m> \033[1;37mTotal Live Proxy Count: \033[1;31m[\033[1;32m{len(valid_proxies)}\033[1;31m]")
    print(f"\033[1;31m> \033[1;37mChecked proxies saved to: \033[1;33m{check_output_file}")

def main():
    while True:
        clear_console()
        print("""
                    \033[1;31m╔══════════════════════════════════════════════════════╗
                    \033[1;31m║             \033[1;37m╔═╗╦═╗╔═╗═╗ ╦╦ ╦  ╔╦╗╔═╗╔═╗╦             \033[1;31m║
                    \033[1;31m║             \033[1;37m╠═╝╠╦╝║ ║╔╩╦╝╚╦╝   ║ ║ ║║ ║║             \033[1;31m║
                    \033[1;31m║             \033[1;37m╩  ╩╚═╚═╝╩ ╚═ ╩    ╩ ╚═╝╚═╝╩═╝           \033[1;31m║
                    \033[1;31m╚══════════════════════════════════════════════════════╝
                                                            \033[1;31m[\033[1;37mProxy - Tools\033[1;31m]
                                                            \033[1;31m[\033[1;37mMake:@HaiBe_Vx\033[1;31m]
                    \033[1;31m[\033[1;35m1\033[1;31m] > \033[1;33mScan Proxy Count
                    \033[1;31m[\033[1;35m2\033[1;31m] > \033[1;33mCheck ProxyFile
                    \033[1;31m[\033[1;35m3\033[1;31m] > \033[1;33mExit Proxy

""")
        choice = input(f"\033[1;31m[\033[1;37mProxyTool\033[1;31m]~$: \033[1;37m")
        
        if choice == '1':
            scan_proxies()
        elif choice == '2':
            filename = input(f"\033[1;31mEnter File Proxy: \033[1;37m")
            timeout = int(input(f"\033[1;31mEnter Timeout: \033[1;37m"))
            threads = int(input(f"\033[1;31mThreads: \033[1;37m"))
            check_proxies(filename, timeout, threads)
        elif choice == '3':
            print(f"\033[1;36m> \033[1;31mYou have exited the proxy!!")
            break
        else:
            print(f"Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
