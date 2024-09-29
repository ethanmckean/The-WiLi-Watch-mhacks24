import pyautogui
import pygetwindow as gw
import subprocess
import sys
import time

def open_discord():
    # Command to open Discord (adjust the path if necessary)
    subprocess.Popen("C:\Program Files\Google\Chrome\Application\chrome.exe")  # Update the path to Discord
    time.sleep(2)  # Wait for Discord to open

def open_firefox():
    # Command to open Firefox (adjust the path if necessary)
    subprocess.Popen("C:\\Program Files\\Mozilla Firefox\\firefox.exe")  # Update the path to Firefox
    time.sleep(2)  # Wait for Firefox to open

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python test.py <0 for Discord | 1 for Firefox>")
        sys.exit(1)
    
    arg = sys.argv[1]

    if arg == '0':
        open_discord()
        window_title = "Google Chrome"  # Adjust the title for Discord
    elif arg == '1':
        open_firefox()
        window_title = "Mozilla Firefox"  # Adjust the title for Firefox
    else:
        print("Invalid argument. Use 0 for Discord and 1 for Firefox.")
        sys.exit(1)
