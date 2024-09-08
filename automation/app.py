import os
import time
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
from pyngrok import ngrok

# Get the current script's directory
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Define paths relative to the current directory
BUILD_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '..', 'webclient', 'build'))
SERVE_DIR = os.path.join(CURRENT_DIR, 'serve')
SERVER_PORT = 3000

class BuildFolderHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        print(f"Detected change in {event.src_path}. Updating serve directory...")
        update_serve_directory()

def update_serve_directory():
    if os.path.exists(SERVE_DIR):
        shutil.rmtree(SERVE_DIR)
    shutil.copytree(BUILD_DIR, SERVE_DIR)

def run_http_server():
    os.chdir(SERVE_DIR)
    httpd = HTTPServer(('localhost', SERVER_PORT), SimpleHTTPRequestHandler)
    httpd.serve_forever()

def main():
    # Ensure the serve directory is up-to-date before starting the server
    update_serve_directory()

    server_thread = threading.Thread(target=run_http_server)
    server_thread.daemon = True
    server_thread.start()

    public_url = ngrok.connect(SERVER_PORT).public_url
    print(f"ngrok tunnel established at: {public_url}")

    event_handler = BuildFolderHandler()
    observer = Observer()
    observer.schedule(event_handler, BUILD_DIR, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    ngrok.kill()

if __name__ == "__main__":
    main()
