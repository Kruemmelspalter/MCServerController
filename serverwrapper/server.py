import subprocess
import os.path
import os
import time
import re
import colorama


class Server:
    def __init__(self, jarlocation, minheap, maxheap):
        if not os.path.exists(jarlocation):
            raise ValueError("The jar doesn't exist")
        self.jarlocation = jarlocation
        self.minheap = minheap  # in mebibytes
        self.maxheap = maxheap  # in mebibytes
        self.done = False

    def start(self):
        os.chdir(os.path.dirname(self.jarlocation))
        self.popen = subprocess.Popen(["java", f"-Xms{self.minheap}m", f"-Xmx{self.maxheap}m", "-jar",  # launch the server with heap args
                                       self.jarlocation, "nogui"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    def readloop(self):
        for line in iter(self.popen.stdout.readline, ''):
            if self.popen.poll() is not None:
                break

            line_args = re.match(
                br"^\[(\d\d:\d\d:\d\d)\] \[([\w \-]+)\/([A-Z]+)\]: (.*)$", line)
            if line_args is None:
                print(colorama.Fore.CYAN + line.decode(), end="")
                continue
            line_args = line_args.groups()

            if re.match(br"Done \(\d.\d{3}s\)! For help, type \"help\"", line_args[3]) is not None:
                self.done = True
            if line_args[2] == b"WARN":
                print(colorama.Fore.YELLOW + line.decode(), end="")
            elif line_args[2] == b"INFO":
                print(colorama.Fore.GREEN + line.decode(), end="")
            elif line_args[2] == b"ERROR":
                print(colorama.Fore.RED + line.decode(), end="")

    def send_command(self, command: bytes):
        self.popen.stdin.write(command)

    def stop(self):
        self.popen.communicate(b"stop")
