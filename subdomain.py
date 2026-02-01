import requests
from colorama import Style,Fore
from pyfiglet import Figlet
import os
import time


def banner(inteructor_security,inteructor_virus):
    os.system("clear")
    print(Style.BRIGHT,Fore.CYAN)
    fuente = Figlet(font="slant")
    print (fuente.renderText(" _SUBDOMAIN_"),Fore.GREEN)
    print (f"𝐷𝐸𝑉𝐸𝐿𝑂𝑃𝐸𝐷 𝐵𝑌: {Fore.CYAN}𝑆𝑈𝐵-𝑍𝐸𝑅𝑂      \t\t\t{Fore.YELLOW}  𝑆𝐸𝐶𝑈𝑅𝐼𝑇𝑌𝑇𝑅𝐴𝐼𝐿𝑆: {inteructor_security}")	
    print (f"{Fore.GREEN}𝑉𝐸𝑅𝑆𝐼𝑂𝑁: 1.0\t\t\t\t\t{Fore.CYAN}  𝑉𝐼𝑅𝑈𝑆_𝑇𝑂𝑇𝐴𝐿:    {inteructor_virus}\n\n{Fore.CYAN}" )

inteructor_rojo   = f"{Fore.WHITE}[{Fore.RED}OFF{Fore.WHITE}]"
inteructor_verde = f"{Fore.WHITE}[{Fore.GREEN}ON{Fore.WHITE}]"


banner(inteructor_rojo,inteructor_rojo)


dominio = input(f"{Fore.GREEN}𝐼𝑁𝐺𝑅𝐸𝑆𝐴𝑅-𝐷𝑂𝑀𝐼𝑁𝐼𝑂: ")


def obtener_subdominios_securitytrails(dominio, api_key):
    url = f"https://api.securitytrails.com/v1/domain/{dominio}/subdomains?children_only=true"
    headers = {
        "APIKEY": api_key
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        subdominios = data.get("subdomains")
        return subdominios
    else:
        return None
        
subdominios_security = []

api_keys = ["lJGR2Q1wcwZd4OrKoUOQw6EYZmThZYPu"]
for api_key in api_keys:
    subdominios = obtener_subdominios_securitytrails(dominio, api_key)
    if subdominios:
        for subdominio in subdominios:
            subdominios_security.append(f"{subdominio}.{dominio}")
        break

if len(subdominios_security) != 0:
    banner(inteructor_verde,inteructor_rojo)



API_KEY = '30c25839d28b2e90f62b47beac3663d32656079cfdd47facd8dc33c21a720340'

def obtener_subdominios(dominio):
    headers = {'x-apikey': API_KEY}
    subdominios = []
    params = {'limit': 40}

    while True:
        response = requests.get(f'https://www.virustotal.com/api/v3/domains/{dominio}/subdomains',headers=headers,params=params)
        print(f'{response.status_code}:OK')
        if response.status_code == 200:
            data = response.json()['data']
            if not data:
                break
            subdominios.extend(data)
            cursor = response.json().get('meta', {}).get('cursor')
            if cursor is None:
                break
            params['cursor'] = cursor
        else:
            return []
            
    subdominios_v = []
    if subdominios:
        for subdominio in subdominios:
            subdominios_v.append(subdominio['id'])
        return subdominios_v


subdominios_virus = obtener_subdominios(dominio)
if subdominios_virus == None:
    subdominios_virus = []
        
if len(subdominios_security) != 0 and len(subdominios_virus) != 0:
    banner(inteructor_verde,inteructor_verde)
    
elif len(subdominios_security) != 0:
    banner(inteructor_verde,inteructor_rojo)

elif len(subdominios_virus) != 0:
    banner(inteructor_rojo,inteructor_verde)
    
else:
    banner(inteructor_rojo,inteructor_rojo)
    
    
    
total_subdominios = set(subdominios_security+subdominios_virus)


if len(total_subdominios) <= 500:
    for dominios in total_subdominios:
        time.sleep(0.01)
        print(dominios)


else:
    for dominios in total_subdominios:
        file = open(f"{dominio}.txt","a")
        file.write(f"{dominios}\n")
    print(f"\nArchivo guardado: {dominio}.txt\n")
    os.system(f"mv {dominio}.txt ~/storage/shared/Subdominios/") 

print(f"\n{Fore.YELLOW}𝑆𝐸𝐶𝑈𝑅𝐼𝑇𝑌𝑇𝑅𝐴𝐼𝐿𝑆: {Fore.GREEN}{len(subdominios_security)}")
print(f"{Fore.CYAN}𝑉𝐼𝑅𝑈𝑆_𝑇𝑂𝑇𝐴𝐿: {Fore.GREEN}{len(subdominios_virus)}")
print(f"{Fore.WHITE}𝑆𝑢𝑏𝑑𝑜𝑚𝑖𝑛𝑖𝑜𝑠: {Fore.GREEN}{len(total_subdominios)}\n")
