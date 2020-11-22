import threading

from server import start_server
from worker import start_worker

if __name__ == "__main__":
    # clever cloud need an http server to consider this app as healthy
    # start the server in a background thread
    threading.Thread(target=start_server).start()
    start_worker()
