import os
import subprocess
import time
import webbrowser
import signal

def run_django():
    venv_path = os.path.join(os.getcwd(), "venv", "Scripts", "activate")

    # Start the Django server
    command = f'cmd.exe /k "{venv_path} & python manage.py runserver"'
    server_process = subprocess.Popen(command, shell=True)

    # Wait a moment for the server to start
    time.sleep(3)

    # Open the app in the default web browser
    browser = webbrowser.open("http://127.0.0.1:8000")

    try:
        print("Django server is running. Close the browser to exit.")

        # Keep the script running while checking for user input
        while True:
            time.sleep(2)  # Polling interval
            if not is_browser_open():
                print("Browser closed. Shutting down the server...")
                server_process.terminate()
                break

    except KeyboardInterrupt:
        print("Exiting...")

    finally:
        server_process.terminate()  # Ensure the server is killed
        print("Django server stopped.")

def is_browser_open():
    """Checks if the browser process is running (Windows-only method)."""
    try:
        output = subprocess.check_output('tasklist', shell=True).decode()
        return "chrome.exe" in output or "firefox.exe" in output or "msedge.exe" in output
    except Exception:
        return False

if __name__ == "__main__":
    run_django()
