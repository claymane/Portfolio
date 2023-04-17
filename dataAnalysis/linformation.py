#!/usr/bin/env python3

import csv
import sys

total_disk = 0
total_disk_free = 0
total_ram = 0
total_ram_free = 0
total_swap = 0
total_swap_free = 0
host_count = 0

file = sys.argv[1]
logfile = 'linformation.log'

def log_host_info(host_info):
    with open(logfile, 'a') as f:
        f.write("Host: {}\n".format(host_info['Host']))

        f.write("Diagnostics:\n")
        for diagnostic in host_info['Diagnostics']:
            f.write("  {}\n".format(diagnostic))

        f.write("Messages:\n")
        for message in host_info['Messages']:
            f.write("  - {}\n".format(message))
        f.write("\n")

with open(file, mode='r') as csvfile:
    csvreader = csv.DictReader(csvfile)

    for row in csvreader:
        # Check if all fields are present
        if all(field in row and row[field] is not None for field in ['Host', 'Disk', 'Free', 'RAM', 'Free', 'SWAP', 'Free']):
            
            host = row['Host']
            disk = round(float(row['Disk']), 2)
            disk_free = round(float(row['Free']), 2)
            ram = round(float(row['RAM']), 2)
            ram_free = round(float(row['Free']), 2)
            swap = round(float(row['SWAP']), 2)
            swap_free = round(float(row['Free']), 2)

            total_disk += disk
            total_disk_free += disk_free
            total_ram += ram
            total_ram_free += ram_free
            total_swap += swap
            total_swap_free += swap_free
            host_count += 1

            host_info = {
            'Host': host,
            'Diagnostics' : [],
            'Messages': []
            }

            host_info['Diagnostics'].append(f"""
            "Disk: Size: {disk} GB, Free: {disk_free} GB
            "RAM: {ram} GB, RAM Free: {ram_free} GB, Swap: {swap} GB, Swap Free: {swap_free} GB
            """)

            threshold = 0.05
            if disk_free / disk < threshold:
                host_info['Messages'].append(f"Less than five percent of the disk is free.")

            if ram_free / ram < threshold:
                host_info['Messages'].append("Less than five percent of RAM is free.")

            if swap_free / swap < threshold:
                host_info['Messages'].append("Less than five percent of SWAP is free.")

            log_host_info(host_info)
            print(host_info)

average_disk = total_disk / host_count
average_disk_free = total_disk_free / host_count
average_ram = total_ram / host_count
average_ram_free = total_ram_free / host_count
average_swap = total_swap / host_count
average_swap_free = total_swap_free / host_count

print(f"Average disk size: {average_disk:.2f} GB, Average disk free: {average_disk_free:.2f} GB")
print(f"Average RAM: {average_ram:.2f} GB, Average RAM free: {average_ram_free:.2f} GB")
print(f"Average swap: {average_swap:.2f} GB, Average swap free: {average_swap_free:.2f} GB")

