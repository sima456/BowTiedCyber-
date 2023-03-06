import argparse

HEADER_SIZES = {
    1024: {
        'magic_number': slice(0, 2),
        'version': slice(2, 4),
        'page_size': slice(4, 8),
        'num_pages': slice(8, 12)
    },
    2048: {
        'magic_number': slice(0, 2),
        'version': slice(2, 4),
        'page_size': slice(4, 8),
        'num_pages': slice(8, 12),
        'checksum': slice(12, 16),
        'timestamp': slice(16, 24),
        'uuid': slice(24, 40),
        'reserved': slice(40, 2048)
    },
    4096: {
        'magic_number': slice(0, 2),
        'version': slice(2, 4),
        'page_size': slice(4, 8),
        'num_pages': slice(8, 16),
        'checksum': slice(16, 20),
        'timestamp': slice(20, 28),
        'uuid': slice(28, 44),
        'reserved': slice(44, 4096)
    }
}

def parse_swapfile(filename, header_size, verbose=False):
    if header_size not in HEADER_SIZES:
        raise ValueError("Invalid header size")
    
    with open(filename, 'rb') as f:
        header_data = f.read(header_size)
        
        # extract data from the header
        header = {}
        for field, slice_ in HEADER_SIZES[header_size].items():
            header[field] = header_data[slice_]
        
        # print the extracted data
        print("Magic Number: {}".format(header['magic_number']))
        print("Version: {}".format(header['version']))
        print("Page Size: {}".format(header['page_size']))
        print("Number of Pages: {}".format(header['num_pages']))
        
        if verbose:
            print("Checksum: {}".format(header['checksum']))
            print("Timestamp: {}".format(header['timestamp']))
            print("UUID: {}".format(header['uuid']))
            print("Reserved: {}".format(header['reserved']))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parse swapfile.')
    parser.add_argument('filename', help='the path to the swapfile')
    parser.add_argument('--header-size', '-s', type=int, choices=HEADER_SIZES.keys(), default=1024,
                        help='the size of the header to parse')
    parser.add_argument('--verbose', '-v', action='store_true', help='print verbose output')
    args = parser.parse_args()

    parse_swapfile(args.filename, args.header_size, args.verbose)
