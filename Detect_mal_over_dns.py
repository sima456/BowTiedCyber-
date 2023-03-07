#!/usr/bin/env python3

import argparse
import pandas as pd
from scapy.all import *
import tldextract
import requests

VT_API_KEY = 'YOUR_VIRUSTOTAL_API_KEY'

def analyze_dns_packets(pcap_file):
    packets = rdpcap(pcap_file)
    dns_packets = [pkt for pkt in packets if DNS in pkt]

    dns_df = pd.DataFrame(columns=['timestamp', 'src_ip', 'dst_ip', 'query_name', 'response_code', 'is_malware'])

    for pkt in dns_packets:
        timestamp = pkt.time
        src_ip = pkt[IP].src
        dst_ip = pkt[IP].dst
        query_name = pkt[DNSQR].qname.decode('utf-8').lower()

        # Extract top-level domain (TLD) from query name
        tld = tldextract.extract(query_name).suffix

        # Check if TLD is known to be associated with malware domains
        if tld in ['top', 'zip', 'review', 'country', 'cricket']:
            is_malware = True
        else:
            is_malware = False

        # Get DNS response code (e.g. NOERROR, NXDOMAIN, SERVFAIL)
        response_code = pkt[DNS].rcode

        # Add packet information to dataframe
        dns_df = dns_df.append({'timestamp': timestamp, 'src_ip': src_ip, 'dst_ip': dst_ip, 'query_name': query_name, 
                                'response_code': response_code, 'is_malware': is_malware}, ignore_index=True)

    return dns_df

def send_to_virustotal(domain):
    url = 'https://www.virustotal.com/api/v3/domains/{}'.format(domain)
    headers = {'x-apikey': VT_API_KEY}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()['data']
        print("[*] Results for domain {}: detected by {} out of {} engines".format(domain, data['attributes']['last_analysis_stats']['malicious'], data['attributes']['last_analysis_stats']['total']))
    else:
        print("[!] Error fetching results for domain {}: status code {}".format(domain, response.status_code))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Analyze DNS packets to detect potential malware domains')
    parser.add_argument('pcap_file', help='Path to PCAP file to analyze')
    args = parser.parse_args()

    dns_df = analyze_dns_packets(args.pcap_file)
    malware_domains = dns_df[dns_df['is_malware'] == True]['query_name'].unique()
    print("[*] Malware domains found in PCAP file:")
    for domain in malware_domains:
        print(domain)
        send_to_virustotal(domain)
