#!/usr/bin/env python3

import csv
import sys

file = sys.argv[1]

with open(file, mode='r') as csvfile:
    csvreader = csv.DictReader(csvfile)

    for row in csvreader:
        # Check if all fields are present
        if all(field in row and row[field] is not None for field in ['Host', 'DRIVE1', 'DRIVE1_size', 'DRIVE1_free', 'DRIVE1_health1', 'DRIVE2', 'DRIVE2_size', 'DRIVE2_free', 'DRIVE2_health', 'RAM', 'RAM_Free', 'RAM_SWAP', 'SWAP_Free', 'SWAP_Peak']):
            host = row['Host']
            drive1 = row['DRIVE1']
            drive1_size = round(float(row['DRIVE1_size']) / (1024**3), 2)
            drive1_free = round(float(row['DRIVE1_free']) / (1024**3), 2)
            drive1_health = row['DRIVE1_health1']
            drive2 = row['DRIVE2']
            drive2_size = round(float(row['DRIVE2_size']) / (1024**3), 2)
            drive2_free = round(float(row['DRIVE2_free']) / (1024**3), 2)
            drive2_health = row['DRIVE2_health']
            ram = float(row['RAM'])
            ram_free = round(float(row['RAM_Free']) / 1024, 2)
            ram_swap = round(float(row['RAM_SWAP']) / 1024, 2)
            swap_free = round(float(row['SWAP_Free']) / 1024, 2)
            swap_peak = round(float(row['SWAP_Peak']) / 1024, 2)

            # Perform operations on the data as needed
            # Example: print the host and its drive, RAM, and SWAP information
            print(f"""Host: {host} 
            + "Drive 1: {drive1}, Size: {drive1_size} GB, Free: {drive1_free} GB, Health: {drive1_health}
            + "Drive 2: {drive2}, Size: {drive2_size} GB, Free: {drive2_free} GB, Health: {drive2_health}
            + "RAM: {ram} GB, RAM Free: {ram_free} GB, RAM Swap: {ram_swap} GB, Swap Free: {swap_free} GB, Swap Peak: {swap_peak} GB
            """)
