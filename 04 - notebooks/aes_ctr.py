import os                                                            # To generate random key and nonce.
import timeit                                                        # To measure performance of our functions.
from plot_functions import *                                         # Plotting functions for AES, RSA and SHA.
from cryptography.hazmat.primitives.ciphers import Cipher            # To create a cipher for the AES.
from cryptography.hazmat.primitives.ciphers import algorithms, modes # To define the algorithm and mode of our cipher.

def my_encrypt_aes_ctr(plaintext, key, nonce):
    alg = algorithms.AES(key)                                        # Defines algorithm as AES
    mode = modes.CTR(nonce)                                          # Uses nonce for CTR mode
    cypher = Cipher(alg,mode)                                        # Creates cipher
    encrypt = cypher.encryptor()  
    return encrypt.update(plaintext) + encrypt.finalize() 

def my_decrypt_aes_ctr(ciphertext, key, nonce):
    alg = algorithms.AES(key) 
    mode = modes.CTR(nonce) 
    cypher = Cipher(alg,mode) 
    decrypt = cypher.decryptor()
    return decrypt.update(ciphertext) + decrypt.finalize()

def AES_execution(base_path, sizes, repetitions, key, nonce):
    results = {size: {} for size in sizes}                           # Dict with results organized by size
    for size in sizes:
        folder_path = os.path.join(base_path, size)                  # Finds the 10 .txt files of the current size
                                                                     # Then, creates a list with all those files
        filenames = sorted([f for f in os.listdir(folder_path) if f.endswith('.txt')], key=lambda x: int(x.split('_')[1].split('.')[0]))
        for fname in filenames:
            file_path = os.path.join(folder_path, fname)             # Path of the current file
            
            with open(file_path, 'rb') as f:                         # Reads content in bytes
                content = f.read()

                                                                     # Measures encryption
            t_enc = timeit.repeat(lambda: my_encrypt_aes_ctr(content, key, nonce), repeat=repetitions, number=1)
            
            ciphertext = my_encrypt_aes_ctr(content, key, nonce)     # Generates ciphertext to desencrypt it
            
                                                                     # Measures desencryption
            t_dec = timeit.repeat(lambda: my_decrypt_aes_ctr(ciphertext, key, nonce), repeat=repetitions, number=1)
            
                                                                     # Saves time list for both operations
            results[size][fname] = {'AES Encryption': t_enc, 'AES Decryption': t_dec}
    return results