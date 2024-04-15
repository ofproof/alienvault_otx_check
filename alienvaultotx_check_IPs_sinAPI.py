import requests
import csv
import time

API_KEY = 'YOUR_API_KEY_HERE'
OTX_API_URL = 'https://otx.alienvault.com/api/v1/indicators/IPv4/'

def get_ip_info(ip,section):
    headers = {'X-OTX-API-KEY': API_KEY}
    url = OTX_API_URL + ip  + section

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print ("Error: "+response.status_code+" obtaining info about "+ip+". Waiting 1min due to request limit...")
        time.sleep(60)
        return None
    

def main():
    input_file = 'ip_list.txt'
    output_file = 'ip_info.csv'

    with open(input_file, 'r') as file:
        ip_list = file.read().splitlines()

    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['IP', 'Pulses', 'Malware',])
        print("Starting to obtain info...")
        contador = 0
        contador_total = 0
        for ip in ip_list:
            contador_total += 1
            print(str(contador_total)+" Info obtained: " + ip)
            #comprobar si es privada
            if ip.startswith('10.') or ip.startswith('192.168.') or (ip.startswith('172.') and (int(ip.split('.')[1]) >= 16 and int(ip.split('.')[1]) <= 31)):
                print("--The IP " + ip + " is private.")
                writer.writerow([ip, 'Private', 'Private'])
                continue
            try:
                pulses = get_ip_info(ip,'/general')['pulse_info']['count']
                malware = get_ip_info(ip,'/malware')['count']
                contador += 2 #2 peticiones por IP
                print("|__Pulses: " + str(pulses)  +" Malware: "+ str(malware)+".\n")
                writer.writerow([ip, pulses, malware])
            except:
                writer.writerow([ip, 'Error', 'Error',])
                print("--Error obtaining info about the IP")
            if contador == 1000:
                print("Waiting 1 min to limit requests...")
                time.sleep(60)
                contador = 0

    print(f"The info about the IPs was saved to '{output_file}'.")

if __name__ == '__main__':
    main()