import serverwrapper.server
import time
import threading
import colorama

if __name__ == "__main__":
    colorama.init()
    server = serverwrapper.server.Server(
        "/projects/MC/Server/1.15.2/spigot-1.15.2.jar", 1024, 2048)

    server.start()

    threading.Thread(target=server.readloop).start() # start readloop for output and 

    input()  # wait for newline in console to stop the server
    server.stop()
