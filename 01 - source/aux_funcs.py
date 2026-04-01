import os 
import time

def measure_performance_time(func, args = None):
    start_time = time.perf_counter()
    result = func(args) if args else func()
    end_time = time.perf_counter()
    duration = end_time - start_time
    return duration, result

def xor_bytes(b1, b2):
    return bytes(a ^ b for a, b in zip(b1, b2))

""" def choose_size(base_path):
    print(f"Searching in: {base_path}")
    print("Available sizes: 8, 64, 512, 4096, 32768, 262144, 2097152")
    size_choice = input("Write file size to encrypt the 10 files: ").strip()
    return size_choice """

def results_path(dir, mode):
    if (mode == "Encrypting"): return os.path.join(dir, "03 - data", "results")
    return os.path.join(dir, "03 - data", "results_decrypted")

def files_path(dir, mode):
    if mode == "Encrypting": return os.path.join(dir, "03 - data", "inputs by size")
    return os.path.join(dir, "03 - data", "results")

def get_files(file, file_size, mode):
    script_dir = os.path.dirname(os.path.abspath(file))
    folder_path = os.path.join(files_path(script_dir, mode), file_size)

    if os.path.exists(folder_path):
        all_files = [file for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))]

        if (all_files): return all_files, folder_path
        return None
    else:
        print(f"Path not found: {folder_path}")
        return None
    
def save_in_results(ciphertext, file, file_size, file_name, mode):
    script_dir = os.path.dirname(os.path.abspath(file))
    output_dir = os.path.join(results_path(script_dir, mode), file_size)
    os.makedirs(output_dir, exist_ok=True)
    file_ext = ".enc" if mode == "Encrypting" else ".dec"
    output_path = os.path.join(output_dir, file_name + file_ext)
    with open(output_path, "wb") as f_enc:
        f_enc.write(ciphertext)
    return output_dir