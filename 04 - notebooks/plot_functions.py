import matplotlib.pyplot as plt                                      # Generating graphs.
import seaborn as sns                                                # Improving graph visualization.
import pandas as pd                                                  # To create a dataframe of our results.

# ======================================================================== #
# PLOT FUNCTIONS FOR AES-CTR (default usage: 32768 Bytes and 'file_1.txt') #
# ======================================================================== #

def create_dataframe_AES(data):      
    data_pd = []                                                     # For creating the dataframe.
    for size, files in data.items():
        for fname, metrics in files.items():
            for operation, times in metrics.items():
                for t in times:
                    data_pd.append({
                        "Size_Bytes": int(size),                     # First column of our dataframe is the file size.
                        "Filename": fname,                           # For each file size, we have 10 different file names.
                        "Execution_Time": t,                         # Each execution originates different execution times.
                        "Operation": operation                       # Separates encrypting and decrypting as different operations.
                    })
    return pd.DataFrame(data_pd)                                     # Dataframe with all of our time measurements.

def plot_variation_same_file(df_data, size=32768, filename='file_1.txt'):
                                                                     # 
    file_test = df_data[(df_data['Size_Bytes'] == size) & (df_data['Filename'] == filename)]
    plt.figure(figsize=(8, 4))
    sns.histplot(data=file_test, x='Execution_Time', hue='Operation', kde=False, element="step")
    plt.title(f"Time Variability: Same File ({size} bytes, {filename})")
    plt.xlabel("Execution Time (seconds)")
    plt.ylabel("Frequency")
    plt.ticklabel_format(style='plain', axis='x')
    plt.show()

def plot_variation_fixed_file_categorical(df_data, filename='file_1.txt'):
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
    size_test = df_data[df_data['Size_Bytes'] == size]
    
    plt.figure(figsize=(12, 5))
    sns.boxplot(data=size_test, x='Filename', y='Execution_Time', hue='Operation', palette='magma')
    plt.title(f"Consistency Check: 10 Different Files (Size: {size} bytes)")
    plt.ylabel("Execution Time (seconds)")
    plt.xticks(rotation=45)
    plt.show()

def plot_consistency_all_sizes_us(df_data):
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

# ============================================================== #
# PLOT FUNCTIONS FOR RSA, SHA and final comparison with AES-CTR  #
# ============================================================== #

def create_dataframe_RSA(data):      
    data_pd = []                                                     # For creating the dataframe.
    for size, files in data.items():
        for index, metrics in files.items():
            for operation, times in metrics.items():
                data_pd.append({
                    "Size_Bytes": int(size),                         # First column of our dataframe is the file size.
                    "Filename": "file_" + str(index+1) + ".txt",     # For each file size, we have 10 different file names.
                    "Execution_Time": times,                         # Each execution originates different execution times.
                    "Operation": operation                           # Separates encrypting, decrypting, RSA and SHA as different operations.
                })
    df_data = pd.DataFrame(data_pd)                                  # Dataframe with all of our time measurements.
    df_data['Size_Bytes'] = pd.to_numeric(df_data['Size_Bytes'])
    df_data['Execution_Time'] = pd.to_numeric(df_data['Execution_Time'])
    return df_data

def show_plot(dataframe, title):                                     # Standard plot to compare execution times by file size in a dataframe
    plt.figure(figsize=(10, 6))                                      # Plot design configurations for cleaner display.
    sns.set_theme(style="whitegrid")

    ax = sns.lineplot(
        data=dataframe,
        x='Size_Bytes',                                              # The x grid of our plot is the size of the files.
        y='Execution_Time',                                          # The y grid is the execution time for each of the file sizes.
        hue='Operation',                                             # We distinguish different operations by colors,
        style='Operation',                                           # and by different line styles as well.
        markers=True,     
        dashes=False,
        linewidth=2,
        markersize=8
    )

    ax.set_xscale('log', base=2)                                     # For better visualization, we set the scale of the x grid to log (base 2),
    ax.set_yscale('log', base=10)                                    # and we set the y grid scale to log (base 10).

                                                                     # Adding labels to our plot
    plt.xlabel('File Size (Bytes) - Log2 Scale', fontsize=12, fontweight='bold')
    plt.ylabel('Execution Time (\u00B5s)', fontsize=12, fontweight='bold') 
    plt.title(title, fontsize=14, fontweight='bold')

    sizes = [8, 64, 512, 4096, 32768, 262144, 2097152]               # Configure x grid to mark the exact values of our file sizes
    plt.xticks(sizes, sizes, rotation=45)

    plt.tight_layout()
    plt.show()

def plot_exec_time_by_file_size(dataframe):                          # Shows the plot that compares RSA and SHA Encryption and Decryption times by file size
    title = 'Execution Times for RSA and SHA by File Size'
    show_plot(dataframe, title)

def plot_comparison_AES_RSA(data_AES, data_RSA):                     # Compares AES vs RSA by execution times
    df_data = pd.concat([data_AES, data_RSA], ignore_index=True)     # Combines the dataframes into one
    title = 'Performance Comparison: RSA vs AES - CTR Operations'
    show_plot(df_data, title)

def plot_comparison_AES_SHA(data_AES, data_SHA):                     # Compares AES vs SHA by execution times
    df_data = pd.concat([data_AES, data_SHA], ignore_index=True)     # Combines the dataframes into one
    title = 'Performance Comparison: SHA vs AES - CTR Operations'
    show_plot(df_data, title)