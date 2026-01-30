#!/usr/bin/env python3
import os
import requests
from colorama import Style, Fore
from pyfiglet import Figlet
import threading
import time
import random
from tqdm import tqdm
from ipaddress import IPv4Address
from queue import Queue

DEFAULT_TIMEOUT = 3.0
DEFAULT_THREADS = 100

host_fount = []
datos = []
ips = []
data_lock = threading.Lock()

def persistencia(host, dato):
    with data_lock:
        host_fount.append(host)
        datos.append(dato)

def IP(i):
    salida = os.popen(f"nslookup {i}").read().split()
    if len(salida) < 5:
        return []
    salida = salida[4:]
    ips_local = []
    idx = 0
    while idx < len(salida):
        if salida[idx] == "Address:" and idx + 1 < len(salida):
            ips_local.append(salida[idx + 1])
            idx += 2
        else:
            idx += 1
    return ips_local

def solicitud(opcion, i, codigos, session, timeout):
    data = {}
    protocolo = {1: "http://", 2: "https://"}

    if i.startswith("http:"):
        i = i[7:]
        opcion = 1
    elif i.startswith("https:"):
        i = i[8:]
        opcion = 2

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 12; moto g power (2022) Build/S3RQS32.20-42-10-9-12; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/129.0.6668.31 Mobile Safari/537.36",
            "Connection": "close"
        }
        url = f"{protocolo.get(opcion)}{i}"
        resp = session.get(url, timeout=timeout, allow_redirects=False, headers=headers)
        codigo = resp.status_code
        data = dict(resp.headers)
        data["HOST"] = i
        try:
            data["Codigo"] = f"HTTP/1.1 {codigo} {codigos[codigo]}"
        except:
            data["Codigo"] = f"HTTP/1.1 {codigo}"
    except Exception:
        data = None

    try:
        if data is not None:
            loc = data.get("Location", "") or ""
            if "filter-gt.portal-universal.com" in loc or "internet.tigo.com.gt" in loc:
                data = None
    except Exception:
        pass

    if data is not None:
        persistencia(i, data)

def host_print(host):
    ips_list = IP(host["HOST"])
    #ips_list = []
    print(f"{Fore.GREEN}Host: {Fore.YELLOW}{host['HOST']}")
    for ip in ips_list:
        try:
            IPv4Address(ip)
            ipv = "IPv4"
        except:
            ipv = "IPv6"
        print(f"{Fore.GREEN}{ipv}: {Fore.YELLOW}{ip}")
    print(f"{Fore.GREEN}Code: {Fore.CYAN}{host['Codigo']}")
    del host["HOST"]
    del host["Codigo"]
    for clave, valor in host.items():
        if "Server" in clave or "Via" in clave or "x-azure-ref" in clave:
            print(f"{Fore.RED}{clave}: {Fore.CYAN}({valor})")
        else:
            print(f"{Fore.GREEN}{clave}: {Fore.YELLOW}{valor}")

def color_aleatorio_y_banner():
    nr = random.randint(1, 125)
    if nr <= 50:
        print(Fore.CYAN, Style.BRIGHT)
    elif nr <= 100:
        print(Fore.RED, Style.BRIGHT)
    else:
        print(Fore.YELLOW, Style.BRIGHT)
    os.system("clear")
    fuente = Figlet(font="slant")
    print(fuente.renderText("    _CHECKER_"), Fore.GREEN)
    print(f"𝐷𝐸𝑉𝐸𝐿𝑂𝑃𝐸𝐷 𝐵𝑌: {Fore.CYAN}𝑆𝑈𝐵-𝑍𝐸𝑅𝑂")
    print(f"{Fore.GREEN}𝑉𝐸𝑅𝑆𝐼𝑂𝑁: 4.0")

def worker(queue, opcion, codigos, timeout, pbar):
    session = requests.Session()
    while True:
        host = queue.get()
        if host is None:
            queue.task_done()
            break
        try:
            solicitud(opcion, host, codigos, session, timeout)
        except Exception:
            # ignore per-host errors
            pass
        finally:
            pbar.update(1)
            queue.task_done()

def run():
    color_aleatorio_y_banner()
    menu = f"""{Style.BRIGHT}{Fore.CYAN}\t\t      [1] - HTTP 80,8080        
\t\t      [2] - HTTPS 443,8443"""
    print(menu)

    while True:
        try:
            opcion = int(input(">> "))
            if 1 <= opcion <= 2:
                break
            else:
                print(f"{Fore.RED}¡ERROR!\n{Fore.CYAN}")
        except:
            print(f"{Fore.RED}¡ERROR!\n{Fore.CYAN}")

    print(f"{Fore.GREEN}\t\t         𝐼𝑁𝐺𝑅𝐸𝑆𝐴𝑅-𝐻𝑂𝑆𝑇𝑆\n\n")
    host = []
    while True:
        h = input("")
        host.append(h)
        if host[-1] == "":
            host.pop()
            break

    color_aleatorio_y_banner()

    codigos = {
        101: "Switching Protocols",
        200: "OK",
        204: "No Content",
        301: "Moved Permanently",
        302: "Found",
        401: "Unauthorized",
        403: "Forbidden",
        404: "Not Found",
        405: "Method Not Allowed"
    }

    host = tuple(set(host))
    total = len(host)
    q = Queue()
    for h in host:
        q.put(h)

    pbar = tqdm(total=total, ncols=80)
    threads = []
    for _ in range(DEFAULT_THREADS):
        t = threading.Thread(target=worker, args=(q, opcion, codigos, DEFAULT_TIMEOUT, pbar), daemon=True)
        t.start()
        threads.append(t)

    q.join()
    for _ in threads:
        q.put(None)
    for t in threads:
        t.join()
    pbar.close()

    print()
    for dato in datos:
        print(f"{Fore.RED}{'*'*70}")
        host_print(dato)
        print(f"{Fore.RED}{'*'*70}")
        print("\n")

    print(f"{Fore.WHITE}{'*'*70}")
    for h in host_fount:
        print(f"{Fore.CYAN}{h}")
    print(f"{Fore.WHITE}{'*'*70}")
    print(f"\n{Fore.GREEN}𝐻𝑜𝑠𝑡: {Fore.RED}{len(host_fount)}")

if __name__ == "__main__":
    run()