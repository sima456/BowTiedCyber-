import argparse
import hashlib
import os

def hash_calculator(data, algorithm='sha256'):
    # Create a new hash object based on the specified algorithm
    if algorithm == 'sha256':
        hash_object = hashlib.sha256()
    elif algorithm == 'sha384':
        hash_object = hashlib.sha384()
    elif algorithm == 'sha512':
        hash_object = hashlib.sha512()
    else:
        raise ValueError(f'Unsupported hash algorithm: {algorithm}')

    # Update the hash object with the data
    hash_object.update(data)

    # Return the hexadecimal representation of the hash
    return hash_object.hexdigest()

def hash_file(file_path, algorithm='sha256'):
    # Open the file in binary mode
    with open(file_path, 'rb') as f:
        # Read the contents of the file
        data = f.read()

        # Calculate the hash of the file contents
        return hash_calculator(data, algorithm)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Calculate the hash of a string or file.')
    parser.add_argument('input', help='The input string or file path')
    parser.add_argument('-a', '--algorithm', default='sha256', choices=['sha256', 'sha384', 'sha512'],
                        help='The hash algorithm to use (default: sha256)')
    args = parser.parse_args()

    # Determine whether the input is a file or a string
    if os.path.isfile(args.input):
        result = hash_file(args.input, args.algorithm)
    else:
        result = hash_calculator(args.input, args.algorithm)

    print(result)
