import os                                                            # To navigate in our project folders.
import time                                                          # To measure performance of our functions.

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