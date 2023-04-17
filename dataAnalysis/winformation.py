#!/usr/bin/env python3

import csv
import sys

total_drive1_size = 0
total_drive1_free = 0
total_drive2_size = 0
total_drive2_free = 0
total_ram = 0
total_ram_free = 0
total_swap = 0
total_swap_free = 0
total_swap_peak = 0
host_count = 0

file = sys.argv[1]
logfile = 'winformation.log'

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
        if all(field in row and row[field] is not None for field in ['Host', 'DRIVE1', 'DRIVE1_size', 'DRIVE1_free', 'DRIVE1_health1', 'DRIVE2', 'DRIVE2_size', 'DRIVE2_free', 'DRIVE2_health', 'RAM', 'RAM_Free', 'SWAP', 'SWAP_Free', 'SWAP_Peak']):

            host = row['Host']
            drive1 = row['DRIVE1']
            drive1_size = round(float(row['DRIVE1_size']) / (1024**3), 2)
            drive1_free = round(float(row['DRIVE1_free']) / (1024**3), 2)
            drive1_health = row['DRIVE1_health1']
            drive2 = row['DRIVE2']
            drive2_size = round(float(row['DRIVE2_size']) / (1024**3), 2)
            drive2_free = round(float(row['DRIVE2_free']) / (1024**3), 2)
            drive2_health = row['DRIVE2_health']
            ram = round(float(row['RAM']) / 1024, 2)
            ram_free = round(float(row['RAM_Free']) / 1024, 2)
            swap = round(float(row['SWAP']) / 1024, 2)
            swap_free = round(float(row['SWAP_Free']) / 1024, 2)
            swap_peak = round(float(row['SWAP_Peak']) / 1024, 2)

            total_drive1_size += drive1_size
            total_drive1_free += drive1_free
            total_drive2_size += drive2_size
            total_drive2_free += drive2_free
            total_ram += ram
            total_ram_free += ram_free
            total_swap += swap
            total_swap_free += swap_free
            total_swap_peak += swap_peak
            host_count += 1

            host_info = {
                'Host': host,
                'Diagnostics' : [],
                'Messages': []
            }

            host_info['Diagnostics'].append(f""" 
            "Drive 1: {drive1}, Size: {drive1_size} GB, Free: {drive1_free} GB, Health: {drive1_health}
            "Drive 2: {drive2}, Size: {drive2_size} GB, Free: {drive2_free} GB, Health: {drive2_health}
            "RAM: {ram} GB, RAM Free: {ram_free} GB, Swap: {swap} GB, Swap Free: {swap_free} GB, Swap Peak: {swap_peak} GB
            """)

            threshold = 0.05
            if drive1_free / drive1_size < threshold:
                host_info['Messages'].append(f"Less than five percent of drive {drive1} is free.")

            if drive2_free / drive2_size < threshold:
                host_info['Messages'].append(f"Less than five percent of drive {drive2} is free.")
            
            if ram_free / ram < threshold:
                host_info['Messages'].append("Less than five percent of RAM is free.")

            if swap_free / swap < threshold:
                host_info['Messages'].append("Less than five percent of SWAP is free.")

            if swap_peak / swap < 0.20:
                host_info['Messages'].append("less than twenty percent of SWAP is being utilized.")

            if drive1_health != 'Healthy':
                host_info['Messages'].append(f"Drive {drive1} health is not 'healthy'.")

            if drive2_health != 'Healthy':
                host_info['Messages'].append(f"Drive {drive2} health is not 'healthy'.")

            log_host_info(host_info)
            print(host_info)

average_drive1_size = total_drive1_size / host_count
average_drive1_free = total_drive1_free / host_count
average_drive2_size = total_drive2_size / host_count
average_drive2_free = total_drive2_free / host_count
average_ram = total_ram / host_count
average_ram_free = total_ram_free / host_count
average_swap = total_swap / host_count
average_swap_free = total_swap_free / host_count
average_swap_peak = total_swap_peak / host_count


print(f"Average drive 1 size: {average_drive1_size:.2f} GB, Average drive 1 free: {average_drive1_free:.2f} GB")
print(f"Average drive 2 size: {average_drive2_size:.2f} GB, Average drive 2 free: {average_drive2_free:.2f} GB")
print(f"Average RAM: {average_ram:.2f} GB, Average RAM free: {average_ram_free:.2f} GB")
print(f"Average swap: {average_swap:.2f} GB, Average swap free: {average_swap_free:.2f} GB, Average swap peak: {average_swap_peak:.2f} GB")
