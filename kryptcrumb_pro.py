import http.server, socketserver, threading, os, time, sys, shutil, ssl
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import datetime

RED = "\033[1;31m"; GREEN = "\033[1;32m"; YELLOW = "\033[1;33m"; BLUE = "\033[1;34m"; RESET = "\033[0m"

def print_banner():
    os.system('clear')
    logo = [
        "██╗  ██╗██████╗ ██╗   ██╗██████╗ ████████╗",
        "██║ ██╔╝██╔══██╗██║   ██║██╔══██╗╚══██╔══╝",
        "█████╔╝ ██████╔╝██║   ██║██████╔╝   ██║   ",
        "██╔═██╗ ██╔══██╗██║   ██║██╔═══╝    ██║   ",
        "██║  ██╗██║  ██║╚██████╔╝██║        ██║   ",
        "╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝        ╚═╝   "
    ]
    for line in logo: print(f"{RED}{line}{RESET}")
    print(f"{YELLOW}{'[ KRYPTCRUMB PRO v15 - FULLY RESTORED ]'.center(40)}{RESET}")
    print(f"{BLUE}{'========================================'.center(40)}{RESET}")

def setup_ssl():
    print(f"\n{YELLOW}[*] Generating Certificate (.crt)...{RESET}")
    try:
        key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        subject = issuer = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, u"KryptCrumb_Root_CA")])
        cert = x509.CertificateBuilder().subject_name(subject).issuer_name(issuer).public_key(key.public_key()).serial_number(x509.random_serial_number())\
        .not_valid_before(datetime.datetime.utcnow()).not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=365))\
        .add_extension(x509.BasicConstraints(ca=True, path_length=None), critical=True)\
        .sign(key, hashes.SHA256())
        
        with open("kryptcrumb.crt", "wb") as f:
            f.write(cert.public_bytes(serialization.Encoding.PEM))
        
        if os.path.exists("/sdcard/Download"):
            shutil.copy("kryptcrumb.crt", "/sdcard/Download/kryptcrumb.crt")
            print(f"{GREEN}[+] Success! Saved to /sdcard/Download/kryptcrumb.crt{RESET}")
        else:
            print(f"{YELLOW}[!] Cannot find /sdcard/Download. Run 'termux-setup-storage'.{RESET}")
            
    except Exception as e: print(f"{RED}[!] Error: {e}{RESET}")
    input(f"\n{BLUE}Press Enter to return...{RESET}")

def main_menu():
    while True:
        print_banner()
        print(f"{BLUE} 1.{RESET} Activate KryptCrumb")
        print(f"{BLUE} 2.{RESET} SSL Setup (Certificate .crt)")
        print(f"{BLUE} 3.{RESET} View Captured Cookies")
        print(f"{BLUE} 4.{RESET} Clear Cookies Log")
        print(f"{BLUE} 5.{RESET} Exit")
        choice = input(f"\n{GREEN}>>{RESET} Choice: ")
        
        if choice == '1':
            mode = input(f"{YELLOW}Select Mode (1: Standard, 2: Encrypted Traffic): {RESET}")
            class MyTCPServer(socketserver.TCPServer): allow_reuse_address = True
            httpd = MyTCPServer(("", 8080), http.server.SimpleHTTPRequestHandler)
            
            if mode == '2' and os.path.exists("kryptcrumb.crt"):
                print(f"{GREEN}[*] KryptCrumb Active (Encrypted Mode){RESET}")
            else:
                print(f"{GREEN}[*] KryptCrumb Active (Standard Mode){RESET}")
                
            threading.Thread(target=httpd.serve_forever, daemon=True).start()
            sys.stdin.readline()
            httpd.shutdown(); httpd.server_close()
        elif choice == '2': setup_ssl()
        elif choice == '3':
            if os.path.exists('captured_cookies.txt'): os.system('cat captured_cookies.txt')
            else: print(f"{YELLOW}[!] No captured data found.{RESET}")
            input(f"\n{BLUE}Press Enter...{RESET}")
        elif choice == '4':
            if os.path.exists('captured_cookies.txt'):
                os.remove('captured_cookies.txt')
                print(f"{GREEN}[*] Cookies log deleted!{RESET}")
            else: print(f"{YELLOW}[!] No log file found.{RESET}")
            time.sleep(1.5)
        else: break

if __name__ == "__main__": main_menu()
