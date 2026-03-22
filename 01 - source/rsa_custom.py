'''Code that implements RSA, no AI was used unless to explain about the RSA Implementations and libraries to use.'''

#Libraries to import.

import os         # For navegation inside the folders of the project.
import time       # To measura time.
import secrets    # Use entropy for TRUE randoness.
from cryptography.hazmat.primitives.asymmetric import rsa # Keys generation
from cryptography.hazmat.primitives import hashes         # Function H(n, r)

#Custom functions.
''' Chave pública = (n, e)
    Chave privada = (n, d)
    n é público!, ele nasce da multiplicação entre dois primos secretos (p x q), a biblioteca RSA já nos gera uma chave privada, com:
    chave pública associada, d, e'''

def rsa_trapdoor_permutation(public_key, r_int): #Pure RSA, with the private key, it takes it's public numbers and calculate the R.
    '''Explicação por Aly para Sílvia e Amanda entenderam o código.
    Quando geramos uma chave pública com a função RSA, ela possui 2 números associados: n, e. Sim isso são atributos do objeto chave.
    Em uma RSA comum, passaríamos esses valores para nosso amiguinho mas o professor pede para adicionarmos uma cada de proteção, então utilizamos
    o número R cálculado anteriormente (r_int). Nós fazemos n^e (mod r), ou seja, o resto da divisão de (n^e) por r.
    Isso é feito para que possamos permutar o nosso número r em outro número, de modo que sem a chave privada é impossível saber que o número
    utlizou esse r em específico.'''
    e = public_key.public_numbers().e
    n = public_key.public_numbers().n
    return pow(r_int, e, n)
''' Para reverter nossa função e eventualmente encontrar o número r, a fórmula é: pow(r_int, e, n) ^ d (mod n), onde pow(r_int, e, n) é o que
    essa função nos retorna, d = número associado a chave privada, n = número público associado as chaves. Isso resulta no nosso r_int utilizado
    nesta permutação!!'''

def rsa_inverse_trapdoor(private_key, c_r): #Inverse function of the function above. f^-1(c_r) = c_r^d mod n
    '''A função anterior gera um número "mascarado", já essa função é responsável por pegar esse número mascarado em conjunto com o número d
    da chave privada local. Antes tinhamos r -> X(resultado da função anterior), agora essa função transforma nosso X -> r. Mas para isso acontecer
    ela utiliza a seguinte fórmula: r = X ^ d (mod n), onde n é público.'''
    d = private_key.private_numbers().d
    n = private_key.private_numbers().public_numbers.n
    return pow(c_r, d, n)

def xor_bytes(b1, b2):
    '''Não tem mt o que falar aqui, ^ é o operador XOR em python, ele pega dois objetos do tipo bytes, e aplica um XOR entre eles.
    Essa função não tem como objetivo transformar nada em bytes, é literalmente só um XOR entre 2 sequências binárias.
    b1 = bloco de bytes da mensagem, b2 = bloco da função SHA. A função ZIP garante que o código acabe quando fim do comprimento do menor
    objeto for atingido, b1 tem no máximo 32 bytes e b2 sempre tem 32 bytes.'''
    return bytes(a ^ b for a, b in zip(b1, b2))

def custom_encrypt(public_key, message): #Hybrid encription is done here! 
    '''Primeiro, geramos um número VERDADEIRAMENTE aleatório abaixo do valor de n associado a chave. O número deve ser menor para que
    quando aplicarmos r^e (mod n), o resultado seja ÚNICO para todo valor de R.
    Por exemplo: se fizermos, 2 (mod 12) = 2, e 14 (mod 12) = 2, nós temos 2 números que dão o mesmo resultado na aritmétrica modular.
    Isso causaria problemas quando fizéssemos o caminho inverso da permutação vista acima, pois não saberíamos de fato qual o nosso R.'''
    # 1. number N and R.
    n = public_key.public_numbers().n
    r = secrets.randbelow(n)

    '''Aqui nós apenas aplicamos a função trapdoor em nosso R, para permuta-lo em outro número. Uhhh agora ele está mascarado.
    Aí, transformamos esse mascarado num número de 256 bytes, afinal, se nossa chave era de 2048 bits, 2048 / 8 = 256, é garantindo que
    nosso número R já mascarado vá ser possível de se representar em 256 bytes. Por fim, o colocamos numa lista chamada ciphertext_blocks
    e o adicionamos como primeiro e único elemento dessa lista.'''
    # 2. RSA(r)
    rsa_r = rsa_trapdoor_permutation(public_key, r)
    rsa_r_bytes = rsa_r.to_bytes(256, 'big') # 2048 bits = 256 bytes
    ciphertext_blocks = [rsa_r_bytes]

    '''A função SHA256 não aceita números inteiros, diferente do RSA, então agora estamos transformando aquele valor R (sem a máscara) em uma
    sequência de 256 bytes. Isso é feito para que o SHA256 use esses bytes de r como a semente para gerar as máscaras da mensagem.
    A função l_size = 32, representa o "corte" que iremos fazer em nossos arquivos para cifra-los. Isso é: se ele tem 64 bytes, ele será divido
    em 2 partes iguais de 32, isso deve ser feito pois o algoritmo SHA256 gera sempre HASHs de 256 bits (32 bytes), logo, para garantir que nossa
    mensagem seja completamente cifrada, é preciso que todos os bytes estejam cobertos por um byte do HASH!'''
    # 3. Hashing and XOR (SHA256 produz blocos de 32 bytes)
    r_bytes = r.to_bytes(256, 'big')
    l_size = 32 # SHA256 output size

    '''Agora iremos cifrar a mensagem que estão nos arquivos de diferentes tamanhos. Considerando que nosso arquivo message é do tipo byte e
    não uma string, o python calcula quantos bytes ele possui ao fazer len(message). Aí ele IDENTIFICA e SEPARA os arquivos em blocos de
    tamanho 32 bytes como haviamos definido antes (block_idx e chunk).'''
    # 4. Cyphing the message or file.
    for i in range(0, len(message), l_size):
        block_idx = i // l_size
        chunk = message[i : i + l_size]
        '''Aqui nós ligamos nosso motor SHA256 para gerar os HASH's. Aí nós inserimos o número do bloco que queremos cifrar + r em bytes.
        Lembrando que nosso SHA256 só aceita inputs em bytes, então tivemos que converter também o número do bloco para bytes. A soma dos dois
        valores é o que garante a eliminação de padrões na cifragem da mensagem, pois para um mesmo R, teremos sempre uma soma com um valor de bloco
        diferente para gerar criptografia mais aleatória. O código digest.finalize() serve para desligar o moto e pegar o resultado na sequência
        de 32 bytes, totalmente aleatória, é a "chave do bloco".'''
        # H(i, r)
        digest = hashes.Hash(hashes.SHA256())
        digest.update(block_idx.to_bytes(4, 'big') + r_bytes)
        h_i_r = digest.finalize()
        '''Aqui, já com nossa chave de bloco produzida, aplicamos um XOR entre a "chave de bloco" e nosso trecho de mensagem. E adicionamos na
        próxima posição de nossa lista de "blocos já cifrados", lembrando que essa lista já possui seu índice 0 ocupado pelo nosso R mascarado
        também em 32 bytes. Por fim, retornamos todo o conteudo de nossa lista de blocos cifrafos, colados um atrás do outro, com um indicador em
        python de que aquele documento se trata de uma sequência de bytes e não uma string.'''
        ciphertext_blocks.append(xor_bytes(chunk, h_i_r))
    return b"".join(ciphertext_blocks)

#Script of the code, "main function"

'''O código gera um par de chaves RSA de 2048 bits apenas uma vez. Public_exponent é utilizado para eficiência e o Key_size é o mínimo aceitável
nos dias de hoje. Esse código gera um objeto do tipo chave, com os atributos: N(módulo), e(expoente público), d(expoente privado), p e q (os
dois primos que geraram N).'''
private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
public_key = private_key.public_key()

'''Caminhos para o código acessar as pastas de input e também colocar os resultados criptografados na pasta correta.'''
#AI helped me with this code. I was frustrated because I couldn't get the file paths right.
script_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(script_dir)
base_path = os.path.join(root_dir, "03 - data", "inputs by size")
results_base_path = os.path.join(root_dir, "03 - data", "results")

#First Input:
print(f"Buscando em: {base_path}")
print("Tamanhos disponíveis: 8, 64, 512, 4096, 32768, 262144, 2097152")
escolha = input("Digite o tamanho da pasta para encriptar todos os 10 arquivos: ").strip()

'''adiciona o input ao caminho anteriormente criado.'''
folder_path = os.path.join(base_path, escolha)

if os.path.exists(folder_path):
    '''Pegamos a lista de todos os arquivos na pasta escolhida'''
    all_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    if all_files:
        print(f"\nProcessando {len(all_files)} arquivos da pasta '{escolha}'...")
        print(f"{'Arquivo':<20} | {'Tamanho':>10} | {'Tempo (s)':>12}")
        print("-" * 50)
        tempo_total = 0
        for file_name in all_files:
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, "rb") as f:
                data = f.read()
            '''Medição individual de cada arquivo e depois somado ao tempo total.'''
            start_time = time.perf_counter()
            ciphertext = custom_encrypt(public_key, data)
            end_time = time.perf_counter()
            duracao = end_time - start_time
            tempo_total += duracao
            
            '''Salvar o resultado na pasta 'results', dentro de uma subpasta com o tamanho'''
            output_dir = os.path.join(results_base_path, escolha)
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, file_name + ".enc")
            with open(output_path, "wb") as f_enc:
                f_enc.write(ciphertext)
            print(f"{file_name:<20} | {len(data):>10}B | {duracao:12.6f}")
        print("-" * 50)
        print(f"Tempo total para a pasta {escolha}: {tempo_total:.6f} segundos")
        print(f"Arquivos salvos em: {output_dir}\n")
    else:
        print("A pasta está vazia.")
else:
    print(f"Caminho não encontrado: {folder_path}")
