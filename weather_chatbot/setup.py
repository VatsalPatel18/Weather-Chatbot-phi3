import os
import subprocess
import sys

def install_requirements():
    print("Installing requirements...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "--upgrade"])

def install_package():
    print("Installing the weather-chatbot-phi3 package...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", ".", "--upgrade"])

if __name__ == "__main__":
    install_requirements()
    install_package()
    print("Setup completed successfully.")
