import os
import subprocess
import argparse

def find_lost_clusters_live():
    # Find unallocated clusters using fsstat
    output = subprocess.check_output(['fsstat', '-o', '4096', '-f', 'ntfs', '/dev/sda1'])
    lines = output.decode().split('\n')
    clusters = []
    for line in lines:
        if 'Unalloc' in line:
            parts = line.split()
            for part in parts:
                if ':' in part:
                    cluster = int(part.split(':')[0])
                    clusters.append(cluster)

    # Print results
    if len(clusters) > 0:
        print('Found the following lost clusters:')
        for cluster in clusters:
            print(cluster)
    else:
        print('No lost clusters found.')

def find_lost_clusters_on_image_file(image_file):
    # Find unallocated clusters using fsstat
    output = subprocess.check_output(['fsstat', '-o', '4096', '-f', 'ntfs', image_file])
    lines = output.decode().split('\n')
    clusters = []
    for line in lines:
        if 'Unalloc' in line:
            parts = line.split()
            for part in parts:
                if ':' in part:
                    cluster = int(part.split(':')[0])
                    clusters.append(cluster)

    # Print results
    if len(clusters) > 0:
        print('Found the following lost clusters:')
        for cluster in clusters:
            print(cluster)
    else:
        print('No lost clusters found.')

def find_bad_sectors_live():
    # Find bad sectors using badblocks
    output = subprocess.check_output(['sudo', 'badblocks', '-v', '/dev/sda'])
    lines = output.decode().split('\n')
    sectors = []
    for line in lines:
        if 'bad' in line:
            parts = line.split()
            for part in parts:
                if ':' in part:
                    sector = int(part.split(':')[0])
                    sectors.append(sector)

    # Print results
    if len(sectors) > 0:
        print('Found the following bad sectors:')
        for sector in sectors:
            print(sector)
    else:
        print('No bad sectors found.')

def find_bad_sectors_on_image_file(image_file):
    # Find bad sectors using badblocks
    output = subprocess.check_output(['sudo', 'badblocks', '-v', image_file])
    lines = output.decode().split('\n')
    sectors = []
    for line in lines:
        if 'bad' in line:
            parts = line.split()
            for part in parts:
                if ':' in part:
                    sector = int(part.split(':')[0])
                    sectors.append(sector)

    # Print results
    if len(sectors) > 0:
        print('Found the following bad sectors:')
        for sector in sectors:
            print(sector)
    else:
        print('No bad sectors found.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Find lost clusters and bad sectors.')
    parser.add_argument('--image', metavar='IMAGE_FILE', help='path to disk image file')
    args = parser.parse_args()
    
    if args.image:
        image_file = args.image
    else:
        image_file = None
    
    find_lost_clusters(image_file=image_file)
    find_bad_sectors(image_file=image_file)
