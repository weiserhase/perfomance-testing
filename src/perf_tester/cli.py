#!/usr/bin/env python3
import os
import subprocess


def compile_c_files_in_current_directory():
    current_dir = os.getcwd()
    print(f"Scanning directory: {current_dir}")
    for filename in os.listdir(current_dir):
        if filename.endswith(".c"):
            filepath = os.path.join(current_dir, filename)
            # Create output name by removing the .c extension
            executable = os.path.splitext(filename)[0]
            output_path = os.path.join(current_dir, executable)
            command = ["gcc", filepath, "-o", output_path, "-O0"]
            
            print(f"Compiling {filename} -> {executable}")
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            if result.returncode != 0:
                print(f"Error compiling {filename}:\n{result.stderr}")
            else:
                print(f"Successfully compiled {filename} to {executable}")

if __name__ == "__main__":
    compile_c_files_in_current_directory()