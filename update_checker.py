import requests
import webbrowser

LOCAL_VERSION = "1.0"
VERSION_URL = "https://github.com/AK-Up/quickqr-update/blob/main/version.txt"
INSTALLER_URL = "https://github.com/AK-Up/quickqr-update/blob/main/QuickQR_Installer.exe"  # Or Google Drive/Dropbox link

def check_for_update():
    try:
        response = requests.get(VERSION_URL, timeout=5)
        latest_version = response.text.strip()

        if latest_version != LOCAL_VERSION:
            print(f"New version {latest_version} available. You are using {LOCAL_VERSION}.")
            confirm = input("Download and install latest version? (y/n): ").lower()
            if confirm == "y":
                webbrowser.open(INSTALLER_URL)
        else:
            print("You are using the latest version.")
    except Exception as e:
        print("Update check failed:", e)

if __name__ == "__main__":
    check_for_update()
