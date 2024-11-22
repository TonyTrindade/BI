#env_utils.py
from dotenv import load_dotenv
import os

def set_env_variable(key, value, env_file='.env'):
    if os.path.exists(env_file):
        with open(env_file, 'r') as file:
            lines = file.readlines()
        with open(env_file, 'w') as file:
            found = False
            for line in lines:
                if line.startswith(f"{key}="):
                    file.write(f"{key}={value}\n")
                    found = True
                else:
                    file.write(line)
            if not found:
                file.write(f"{key}={value}\n")
    else:
        with open(env_file, 'w') as file:
            file.write(f"{key}={value}\n")
    
    load_dotenv()
