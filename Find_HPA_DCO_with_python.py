import argparse
import os
import psutil
import subprocess

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Get information about a hard drive image file.')
parser.add_argument('image', type=str, help='path to the hard drive image file')
args = parser.parse_args()

# Check if the image file exists
if not os.path.exists(args.image):
    print(f"Error: image file '{args.image}' does not exist.")
    exit()

# Get information about the hard drive image
partitions = psutil.disk_partitions(args.image)
for partition in partitions:
    # Get disk usage statistics for the partition
    usage = psutil.disk_usage(partition.mountpoint)

    # Print the number of tracks and sectors
    print(f"Partition {partition.mountpoint} has {usage.total//(255*63)} tracks and {usage.total%(255*63)} sectors per track.")

    # Check if HPA exists
    output = subprocess.check_output(["hdparm", "-Np", partition.device], universal_newlines=True)
    if "max sectors   = " in output:
        max_sectors = int(output.split("max sectors   = ")[1].split("\n")[0])
        total_sectors = usage.total // 512
        if max_sectors < total_sectors:
            print("Host Protected Area (HPA) detected.")

    # Check if DCO exists
    output = subprocess.check_output(["hdparm", "-I", partition.device], universal_newlines=True)
    if "DCO is" in output:
        print("Device Configuration Overlay (DCO) detected.")
