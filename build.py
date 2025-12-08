import os
import sys
import subprocess
import platform
import time

def main():
    print("--- Secure Auth Project Build System ---")
    
    # 1. Detect OS
    system = platform.system()
    print(f"Detected OS: {system}")
    
    # 2. Determine Compiler Command
    src_file = "auth_core.cpp"
    
    if system == "Windows":
        out_file = "auth_lib.dll"
        # Ensure we use g++
        cmd = ["g++", "-shared", "-o", out_file, src_file]
    elif system == "Linux" or system == "Darwin": # Darwin is Mac
        out_file = "auth_lib.so"
        cmd = ["g++", "-shared", "-o", out_file, "-fPIC", src_file]
    else:
        print(f"Unsupported OS: {system}")
        sys.exit(1)
        
    print(f"Compiling {src_file} -> {out_file}...")
    print(f"Command: {' '.join(cmd)}")
    
    # 3. Execute Compilation
    try:
        # Run in the script's directory
        cwd = os.path.dirname(os.path.abspath(__file__))
        subprocess.check_call(cmd, cwd=cwd)
        print("Compilation Successful!")
    except subprocess.CalledProcessError as e:
        print("Error: Compilation failed.")
        sys.exit(1)
    except FileNotFoundError:
        print("Error: 'g++' not found. Please ensure MinGW (Windows) or GCC (Linux/Mac) is installed and in PATH.")
        sys.exit(1)

    # 4. Check if library exists
    lib_path = os.path.join(cwd, out_file)
    if os.path.exists(lib_path):
        print(f"Library verified at: {lib_path}")
    else:
        print("Error: Library file not found after compilation.")
        sys.exit(1)

    # 5. Launch GUI
    print("Launching GUI...")
    gui_script = "main_gui.py"
    try:
        # Use the same python interpreter
        subprocess.check_call([sys.executable, gui_script], cwd=cwd)
    except subprocess.CalledProcessError as e:
        print(f"GUI exited with error: {e}")

if __name__ == "__main__":
    main()
