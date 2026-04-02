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

                                                                     # Shows encryption and decryption variability for a file over many executions
def plot_variation_same_file(df_data, size=32768, filename='file_1.txt'):
    file_test = df_data[(df_data['Size_Bytes'] == size) & (df_data['Filename'] == filename)]
    plt.figure(figsize=(8, 4))
    sns.histplot(data=file_test, x='Execution_Time', hue='Operation', kde=False, element="step")
    plt.title(f"Time Variability: Same File ({size} bytes, {filename})")
    plt.xlabel("Execution Time (seconds)")
    plt.ylabel("Frequency")
    plt.ticklabel_format(style='plain', axis='x')
    plt.show()

                                                                     # Shows encryption and decryption variability for all file sizes, with fixed file
def plot_variation_fixed_file_categorical(df_data, filename='file_1.txt'):
                                                                     # Filters one file for each size and converts to microsseconds
    df_plot = df_data[df_data['Filename'] == filename].copy()
    df_plot['Execution_Time_us'] = df_plot['Execution_Time'] * 1_000_000
    df_plot = df_plot.sort_values('Size_Bytes')
    df_plot['Size_Label'] = df_plot['Size_Bytes'].astype(str)        # Size treated as text to keep x axis categorical
    plt.figure(figsize=(10, 5))

    sns.lineplot(
        data=df_plot, 
        x='Size_Label',                                              
        y='Execution_Time_us', 
        hue='Operation', 
        marker='o',
        estimator='mean', 
        errorbar='sd'
    )
                                                                    # Final formatting
    plt.title(f"Time Variability vs Specific File Sizes (Fixed File: {filename})", fontsize=14)
    plt.xlabel("File Size (Bytes)")
    plt.ylabel("Execution Time (µs)")
    plt.grid(True, axis='y', ls="--", alpha=0.3)
    plt.ticklabel_format(style='plain', axis='y')
    plt.show()

                                                                     # Encryption and decryption performance for 10 files with same size
def plot_comparison_fixed_size(df_data, size=32768):
    size_test = df_data[df_data['Size_Bytes'] == size]
    plt.figure(figsize=(12, 5))
    sns.boxplot(data=size_test, x='Filename', y='Execution_Time', hue='Operation', palette='magma')
    plt.title(f"Consistency Check: 10 Different Files (Size: {size} bytes)")
    plt.ylabel("Execution Time (seconds)")
    plt.xticks(rotation=45)
    plt.show()

                                                                     # Shows execution time accross all files of all sizes
def plot_consistency_all_sizes_us(df_data):
    df_plot = df_data.copy()
    df_plot['Execution_Time_us'] = df_plot['Execution_Time'] * 1_000_000
    df_plot = df_plot.sort_values('Size_Bytes')
    plt.figure(figsize=(14, 7))
    
    sns.boxplot(
        data=df_plot, 
        x='Size_Bytes', 
        y='Execution_Time_us', 
        hue='Operation',
        palette='magma',
        linewidth=1.2,
        showfliers=False,                                            # Removes outliers which might pollute the graph
        width=0.6
    )
    
    plt.yscale('log')                                                # Log scale allows comparing 8B with 2MB in the same graph
    plt.title("Performance Consistency: All Files across All Sizes (Outliers Hidden)", fontsize=14)
    plt.xlabel("File Size (Bytes)")
    plt.ylabel("Execution Time (µs) - Log Scale")
    plt.grid(True, which="both", axis='y', ls="--", alpha=0.3)       # Grid on both axis for easier reading in log scale
    plt.tight_layout()
    plt.show()

                                                                     # All performances times by file size side by side in a log scale graphic
def plot_final_scalability(df_data):
    df_plot = df_data.copy()
                                                                     # Conversion to microsseconds (us)
    df_plot["Execution_Time_us"] = df_plot["Execution_Time"] * 1_000_000
    unique_sizes = sorted(df_plot['Size_Bytes'].unique())            # Defines exact sizes for x axis labels
    plt.figure(figsize=(10, 5))

    sns.lineplot(
        data=df_plot, 
        x="Size_Bytes", 
        y="Execution_Time_us", 
        hue="Operation", 
        marker="o", 
        errorbar="sd"
    )
    
    plt.xscale('log')                                                # Logarithmic scale for better visualization
    plt.xticks(unique_sizes, labels=[str(s) for s in unique_sizes])
    plt.title("Symmetry & Scalability: Encryption vs Decryption Performance", fontsize=14)
    plt.xlabel("File Size (Bytes)")
    plt.ylabel("Execution Time (µs)")
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
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(8, 5))                                      # Plot design configurations for cleaner display.


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