import sys
import os

def generate_files(count, file_size):

    for i in range(1, count + 1):
        filename = f"file_{i}.txt"
        random_data = os.urandom(file_size)
        with open(filename, "wb") as f:
            f.write(random_data)
        print(f"Created: {filename} ({file_size} bytes)")

if __name__ == "__main__":
    print("\n **Carefull where you execute this code! It may overlap files already created!**\n")
    text = """Select the size of the files (in bytes):
1- 8
2- 64
3- 512
4- 4096
5- 32768
6- 262144
7- 2097152
Option: """
    inp = int(input(text))
    match inp:
        case 1:
            size = 8
        case 2:
            size = 64
        case 3:
            size = 512
        case 4:
            size = 4096
        case 5:
            size = 32768
        case 6:
            size = 262144
        case 7:
            size = 2097152
        case _:
            print("Invalid Option. Terminanting de program...")
            sys.exit()
    generate_files(count=10, file_size=size)