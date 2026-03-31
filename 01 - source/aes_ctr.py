import os #para gerar as k e nonce aleatórios
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes #para configurar o tipo de algoritmo AES
import timeit #para medir o temp-o
import pandas as pd #para gerar dataframe e organizar dados
import numpy as np #para calculos de desvio padrao e intervalos de confiança previsos
import matplotlib.pyplot as plt #para gerar graficos
import seaborn as sns #para gerar melhor visualizaçao nos gráficos

'''Aqui vou só codar 2 funções, uma pra encriptar e outra pra decriptar, então
vou chamar essas funções no notebook para fazer a análise e plotagem '''

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

#chaves globais para o teste
key = os.urandom(32)
nonce = os.urandom(16) 

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__)) #descobre a pasta exata onde este arquivo (aes_ctr.py) está salvo
base_path = os.path.join(SCRIPT_DIR, "../03 - data/inputs by size") # constrói o caminho até a pasta de dados baseando-se no local do script
sizes = ["8", "64", "512", "4096", "32768", "262144", "2097152"] #tamanhos sugeridos no assignment

repetitions = 30 #de acordo com central limit theory

results = {size: {} for size in sizes} #dict com resultados por tamanho

for size in sizes:
    folder_path = os.path.join(base_path, size) #filtra apenas os arquivos .txt (file_1.txt até file_10.txt)
    filenames = sorted([f for f in os.listdir(folder_path) if f.endswith('.txt')], key=lambda x: int(x.split('_')[1].split('.')[0])) #nomeia os arquivos    
    for fname in filenames:
        file_path = os.path.join(folder_path, fname)
        
        #LER O ARQUIVO COMO BYTES (essencial para criptografia)
        with open(file_path, 'rb') as f:
            content = f.read()
        
        #1. Medir encriptação
        t_enc = timeit.repeat(lambda: my_encrypt_aes_ctr(content, key, nonce), 
                              repeat=repetitions, number=1)
        
        #Gerar o texto encriptado para testar a decriptação
        ciphertext = my_encrypt_aes_ctr(content, key, nonce)
        
        #2. Medir decriptação
        t_dec = timeit.repeat(lambda: my_decrypt_aes_ctr(ciphertext, key, nonce), 
                              repeat=repetitions, number=1)
        
        #salva a lista de tempos de ambas as operações
        results[size][fname] = {'Encryption': t_enc, 'Decryption': t_dec}

data_pd = [] #cria o dataframe para pandas

for size, files in results.items(): #loop de tamanhos e arquivos
    for fname, metrics in files.items(): #loop das metricas por aquivo
        for operation, times in metrics.items(): # faz tanto para encriptar quando decriptar
            for t in times: #coloca o tempo de execuçao de cada
                data_pd.append({
                    "Size_Bytes": int(size),
                    "Filename": fname,
                    "Execution_Time": t,
                    "Operation": operation # Coluna nova para separar no gráfico
                })

df = pd.DataFrame(data_pd) #DataFrame final para exportação no pandas

# =====================================================================
# FUNÇÕES DE PLOTAGEM (são essas as funções chamadas no notebook - por padrão usam 32768Bytes e 'file_1.txt)
# =====================================================================

def plot_variation_same_file(df_data, size=32768, filename='file_1.txt'):
    """Responde à Question B.1) Do results change if you run a fixed algorithm over the same file multiple times?"""
    file_test = df_data[(df_data['Size_Bytes'] == size) & (df_data['Filename'] == filename)]
    
    plt.figure(figsize=(8, 4))
    sns.histplot(data=file_test, x='Execution_Time', hue='Operation', kde=False, element="step")
    plt.title(f"Time Variability: Same File ({size} bytes, {filename})")
    plt.xlabel("Execution Time (seconds)")
    plt.ylabel("Frequency")
    plt.ticklabel_format(style='plain', axis='x')
    plt.show()

def plot_variation_fixed_file_categorical(df_data, filename='file_1.txt'):
    """
    Responde à B.1 com X sendo EXATAMENTE os 7 tamanhos de arquivo.
    X = File Size (Categorical Labels), Y = Execution Time (us).
    """
    # 1. Filtrar apenas o arquivo fixo e converter para microssegundos
    df_plot = df_data[df_data['Filename'] == filename].copy()
    df_plot['Execution_Time_us'] = df_plot['Execution_Time'] * 1_000_000
    
    # 2. Garantir que o tamanho seja tratado como "texto" para o eixo X não virar uma régua
    # E ordenar para que o gráfico siga do menor para o maior
    df_plot = df_plot.sort_values('Size_Bytes')
    df_plot['Size_Label'] = df_plot['Size_Bytes'].astype(str)

    plt.figure(figsize=(12, 6))
    
    # 3. Usar o lineplot com os rótulos exatos
    # 'marker="o"' coloca a bolinha em cada um dos 7 tamanhos
    sns.lineplot(
        data=df_plot, 
        x='Size_Label', 
        y='Execution_Time_us', 
        hue='Operation', 
        marker='o',
        estimator='mean', 
        errorbar='sd'
    )
    
    # 4. Formatação Final
    plt.title(f"Time Variability vs Specific File Sizes (Fixed File: {filename})", fontsize=14)
    plt.xlabel("File Size (Bytes)")
    plt.ylabel("Execution Time (µs)")
    plt.grid(True, axis='y', ls="--", alpha=0.3)
    
    # Isso garante que os números no Y fiquem limpos
    plt.ticklabel_format(style='plain', axis='y')
    
    plt.show()

def plot_comparison_fixed_size(df_data, size=32768):
    """Responde à Question B.2) And what if you run an algorithm over multiple randomly generated files of fixed size?"""
    size_test = df_data[df_data['Size_Bytes'] == size]
    
    plt.figure(figsize=(12, 5))
    sns.boxplot(data=size_test, x='Filename', y='Execution_Time', hue='Operation', palette='magma')
    plt.title(f"Consistency Check: 10 Different Files (Size: {size} bytes)")
    plt.ylabel("Execution Time (seconds)")
    plt.xticks(rotation=45)
    plt.show()

def plot_consistency_all_sizes_us(df_data):
    """
    Gera um Boxplot comparativo de todos os arquivos em todos os tamanhos.
    X = File Size (Bytes), Y = Execution Time (us) em escala Logarítmica.
    Melhoria: Outliers removidos visualmente para clareza (showfliers=False).
    """
    # 1. Preparação dos dados
    df_plot = df_data.copy()
    df_plot['Execution_Time_us'] = df_plot['Execution_Time'] * 1_000_000
    
    # Ordenar numericamente pelos tamanhos
    df_plot = df_plot.sort_values('Size_Bytes')
    
    plt.figure(figsize=(14, 7))
    
    # 2. Criar o Boxplot
    # showfliers=False: Remove os pontos (outliers) que poluem o gráfico
    # width=0.6: Dá mais respiro entre as barras de tamanhos diferentes
    sns.boxplot(
        data=df_plot, 
        x='Size_Bytes', 
        y='Execution_Time_us', 
        hue='Operation',
        palette='magma',
        linewidth=1.2,
        showfliers=False, 
        width=0.6
    )
    
    # 3. Formatação do Gráfico
    # Escala logarítmica é O SEGREDO para comparar 8B com 2MB no mesmo gráfico
    plt.yscale('log')
    
    plt.title("Performance Consistency: All Files across All Sizes (Outliers Hidden)", fontsize=14)
    plt.xlabel("File Size (Bytes)")
    plt.ylabel("Execution Time (µs) - Log Scale")
    
    # Grade em ambos os eixos para facilitar leitura na escala log
    plt.grid(True, which="both", axis='y', ls="--", alpha=0.3)
    
    plt.tight_layout()
    plt.show()

def plot_final_scalability(df_data):
    """
    Gera o gráfico de Escalabilidade e Simetria com as unidades solicitadas.
    X = Tamanhos específicos (Bytes), Y = Tempo (µs).
    """
    # 1. Preparação: Cópia dos dados e conversão para microssegundos (us)
    df_plot = df_data.copy()
    df_plot["Execution_Time_us"] = df_plot["Execution_Time"] * 1_000_000
    
    # 2. Definir os tamanhos exatos para os rótulos do eixo X
    unique_sizes = sorted(df_plot['Size_Bytes'].unique())
    
    plt.figure(figsize=(12, 6))
    
    # 3. Criar o gráfico de linha
    # O lineplot com errorbar="sd" calcula a média dos 10 arquivos e mostra a variação
    sns.lineplot(
        data=df_plot, 
        x="Size_Bytes", 
        y="Execution_Time_us", 
        hue="Operation", 
        marker="o", 
        errorbar="sd"
    )
    
    # 4. Ajuste dos Eixos
    # Usamos escala logarítmica para que o 8 não fique "esmagado" perto do zero,
    # mas forçamos os labels a serem EXATAMENTE os seus 7 tamanhos.
    plt.xscale('log')
    plt.xticks(unique_sizes, labels=[str(s) for s in unique_sizes])
    
    # 5. Títulos e Legendas
    plt.title("Symmetry & Scalability: Encryption vs Decryption Performance", fontsize=14)
    plt.xlabel("File Size (Bytes)")
    plt.ylabel("Execution Time (µs)")
    
    # Grade e formatação numérica limpa no Y
    plt.grid(True, which="both", ls="-", alpha=0.2)
    plt.ticklabel_format(style='plain', axis='y')
    
    plt.show()
