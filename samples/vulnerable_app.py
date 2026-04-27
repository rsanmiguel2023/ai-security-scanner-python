import os
import subprocess

password = "admin123"

def run_command(user_input):
    os.system(user_input)

def unsafe_subprocess(cmd):
    subprocess.call(cmd, shell=True)

run_command("ls")
unsafe_subprocess("echo hello")