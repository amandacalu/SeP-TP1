from os import urandom #para gerar as k e nonce aleatórios
from binascii import hexlify #para passar pra hex
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes #para configurar o tipo de algoritmo AES
from cryptography.hazmat.primitives import padding #para preencher o tamanho caso necessário

'''Aqui vou só codar 2 funções, uma pra encriptar e outra pra decriptar, então
vou chamar essas funções no notebook para fazer a análise e plotagem '''

key = urandom(32)
nonce = urandom(16) #perguntar tamanho do nonce pq so relatório só tem da key

def my_encrypt_aes_ctr(plaintext, key, nonce):
    alg = algorithms.AES(key) #define o algortimo como o AES
    mode = modes.CTR(nonce) #usa o nonce para o mode counter
    cypher = Cipher(alg,mode) #define a cifra escolhida para encriptação

    encrypt = cypher.encryptor() #encripta 
    
    return encrypt.update(plaintext) + encrypt.finalize() #retorna o c - texto encriptado

def my_decrypt_aes_ctr(ciphertext, key, nonce):
    alg = algorithms.AES(key) #define o algortimo como o AES
    mode = modes.CTR(nonce) #usa o nonce para o mode counter
    cypher = Cipher(alg,mode) #define a cifra escolhida para encriptação

    decrypt = cypher.decryptor() #descripta

    return decrypt.update(ciphertext) + decrypt.finalize() #retorna o m - texto original





