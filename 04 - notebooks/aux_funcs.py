import os                                                            # To navigate in our project folders.
import time                                                          # To measure performance of our functions.
import pandas as pd                                                  # To create a dataframe of our results.
import matplotlib.pyplot as plt                                      # Generating graphs.
import seaborn as sns                                                # Improving graph visualization.

def measure_performance_time(func, args = None):                     # Executes function func given as a parameter, and returns its execution time
    start_time = time.perf_counter()
    result = func(args) if args else func()                          # Execute func with its corresponding arguments as the list args
    end_time = time.perf_counter()
    duration = end_time - start_time
    return duration, result                                          # Returns execution time and whatever values the function func might return

def xor_bytes(b1, b2):                                               # Returns the XOR operation between two byte sequences b1 and b2
    return bytes(a ^ b for a, b in zip(b1, b2))                      # Zip guarantees the XOR works for different sized byte sequences

def results_path(dir, mode):                                         # Returns the path of our results folder, to store the encrypted or decrypted files
    if (mode == "Encrypting"): return os.path.join(dir, "03 - data", "results")
    return os.path.join(dir, "03 - data", "results_decrypted")

def files_path(dir, mode):                                           # Returns the path of our source files that will be encrypted/decrypted                     
    if mode == "Encrypting": return os.path.join(dir, "03 - data", "inputs by size")
    return os.path.join(dir, "03 - data", "results")

def get_files(file, file_size, mode):                                # Returns the files that will be used for encryption or decription
    script_dir = os.path.dirname(os.path.abspath(file))
    folder_path = os.path.join(files_path(script_dir, mode), file_size)

    if os.path.exists(folder_path):
        all_files = [file for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))]
        return all_files, folder_path                                # Returns list with each file, as well as the path to their parent folder
    else:
        print(f"Path not found: {folder_path}")                      # Handles cases where, for some reason, the selected folder is empty
        return None
    
def save_in_results(ciphertext, file, file_size, file_name, mode):   # Writes back in the results folder our changed file, in a new file with similar name.
    script_dir = os.path.dirname(os.path.abspath(file))
    output_dir = os.path.join(results_path(script_dir, mode), file_size)
    os.makedirs(output_dir, exist_ok=True)
    file_ext = ".enc" if mode == "Encrypting" else ".dec"
    output_path = os.path.join(output_dir, file_name + file_ext)
    with open(output_path, "wb") as f_enc:
        f_enc.write(ciphertext)

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