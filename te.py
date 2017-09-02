import os
import socket
import subprocess
import sys

import time

TCP_PORT = 55550

# Check for root
euid = os.geteuid()
if euid != 0:
    print("Script not started as root. Running sudo..")
    # Specify root args
    args = ['sudo', sys.executable] + sys.argv + [os.environ]
    # the next line replaces the currently-running process with the sudo
    os.execlpe('sudo', *args)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('127.0.0.1', TCP_PORT))

print("Running as root")
while 1:

    s.listen(1)
    conn, addr = s.accept()
    conn.recv(4096)

    conn.send(bytes("HTTP/1.0 200 OK\r\n", "utf-8"))
    conn.send(bytes("Content-Length:", "utf-8"))

    CommentByte = subprocess.getoutput("sudo nmap -sP 192.168.1.1-254")

    NewCommentByte = CommentByte.replace('\n', "<br/>")

    if NewCommentByte.__contains__("C0:EE:FB:47:16:15"):
        NewCommentByte = "{} {}<br/>".format("Domi is at Home<br/>", NewCommentByte)

    if NewCommentByte.__contains__("C0:EE:FB:42:C8:16"):
        NewCommentByte = "{} {}<br/>".format("Taku is at Home<br/>", NewCommentByte)

    if NewCommentByte.__contains__("C0:EE:FB:42:C8:16"):
        NewCommentByte = "{} {}".format("Marcel is at Home<br/>", NewCommentByte)

    stdoutdata = "<html>" + NewCommentByte + "</html>"

    conn.send(bytes(str(sys.getsizeof(stdoutdata)), "utf-8"))
    conn.send(bytes("\r\nContent-Type: text/html; charset=UTF-8\r\nConnection: close\r\n\r\n", "utf-8"))

    conn.send(bytes(stdoutdata, 'utf-8'))

    conn.close()
    print("stdoutdata: " + stdoutdata)
