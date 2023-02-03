import os                                             import subprocess                                                                                           def ssh_keygen(path, bits=4096):                          try:                                                      if not os.path.exists(path):                              os.makedirs(path)                         
        private_key = os.path.join(path, 'id_rsa')
        public_key = os.path.join(path, 'id_rsa.pub')

        cmd = f"ssh-keygen -t rsa -b {bits} -f {private_key} -N ''"
        subprocess.run(cmd, shell=True, check=True)

        print(f'Private key saved at: {private_key}')
        print(f'Public key saved at: {public_key}')

        # Add the public key to the authorized_keys file
        authorized_keys_file = os.path.join(path, 'authorized_keys')
        with open(public_key, 'r') as pub_key_file:
            pub_key = pub_key_file.read().strip()
            with open(authorized_keys_file, 'a') as auth_file:
                auth_file.write(pub_key + '\n')

        print(f'Public key added to authorized keys file: {authorized_keys_file}')
    except subprocess.CalledProcessError as e:
        print(f'Error generating key: {e}')

if __name__ == '__main__':
    ssh_keygen('/home/Kali/viruse')
