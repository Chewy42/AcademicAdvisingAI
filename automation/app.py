import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
from pyngrok import ngrok

BUILD_DIR = '/home/matt/Desktop/Startups/AcademicAdvisingAI/webclient/build'
SERVER_PORT = 3000

class BuildFolderHandler(FileSystemEventHandler):
    def __init__(self, server):
        self.server = server

    def on_any_event(self, event):
        print(f"Detected change in {event.src_path}. Restarting server...")
        self.server.shutdown()

def run_http_server():
    os.chdir(BUILD_DIR)
    httpd = HTTPServer(('localhost', SERVER_PORT), SimpleHTTPRequestHandler)
    httpd.serve_forever()

def main():
    server_thread = threading.Thread(target=run_http_server)
    server_thread.daemon = True
    server_thread.start()

    public_url = ngrok.connect(SERVER_PORT).public_url
    print(f"ngrok tunnel established at: {public_url}")

    event_handler = BuildFolderHandler(server_thread)
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
