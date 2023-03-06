import argparse
import time
import psutil

def measure_performance_live():
    # Measure seek time and rotation latency
    start = time.time()
    with open('/dev/zero', 'rb') as f:
        f.seek(1024*1024, 0)
        f.read(4096)
    end = time.time()
    seek_time = end - start
    rotation_latency = seek_time / 2

    # Measure data transfer rate
    start = time.time()
    with open('/dev/zero', 'rb') as f:
        for i in range(1024):
            f.read(1024*1024)
    end = time.time()
    data_transfer_rate = (1024 * 1024 * 1024) / (end - start)

    # Print results
    print(f'Seek time: {seek_time:.6f} s')
    print(f'Rotation latency: {rotation_latency:.6f} s')
    print(f'Data transfer rate: {data_transfer_rate:.2f} MB/s')

def measure_performance_on_image_file(image_file):
    # Measure seek time and rotation latency
    with open(image_file, 'rb') as f:
        start = time.time()
        f.seek(1024*1024, 0)
        f.read(4096)
        end = time.time()
    seek_time = end - start
    rotation_latency = seek_time / 2

    # Measure data transfer rate
    with open(image_file, 'rb') as f:
        start = time.time()
        for i in range(1024):
            f.read(1024*1024)
        end = time.time()
    data_transfer_rate = (1024 * 1024 * 1024) / (end - start)

    # Print results
    print(f'Seek time: {seek_time:.6f} s')
    print(f'Rotation latency: {rotation_latency:.6f} s')
    print(f'Data transfer rate: {data_transfer_rate:.2f} MB/s')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Measure hard disk performance.')
    parser.add_argument('--image', metavar='IMAGE_FILE', help='path to disk image file')
    args = parser.parse_args()

    if args.image:
        measure_performance_on_image_file(args.image)
    else:
        measure_performance_live()
