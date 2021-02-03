import serverwrapper.server
import threading
import colorama
import argparse

if __name__ == "__main__":
    colorama.init()

    parser = argparse.ArgumentParser()
    parser.add_argument("serverjar")
    parser.add_argument("--minheap", default=1024, type=int)
    parser.add_argument("--maxheap", default=1024, type=int)

    args = parser.parse_args()

    server = serverwrapper.server.Server(args.serverjar, args.minheap, args.maxheap)

    server.start()

    threading.Thread(target=server.readloop).start()  # start readloop for output and

    input()  # wait for newline in console to stop the server
    server.stop()
