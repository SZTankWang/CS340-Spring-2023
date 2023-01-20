import socket
import sys
import select
import urllib3
import os
import signal
import re

# code from external sources:
# constructing http response, the response_header, response status line, received help from
# https://stackoverflow.com/questions/10114224/how-to-properly-send-http-response-with-python-using-socket-library-only

# the code for using select, received help from https://pymotw.com/3/select/#using-select



def send_data(socket,data,connections):
    #see the request method
    data = data.decode("utf-8").split("\r\n")
    request_info = data[0].split(" ")

    method = request_info[0]

    proto = "HTTP/1.1"

    response_header = {
        'Content-Type': 'text/html; encoding=utf8',
        "Connection":"close"
    }
    if method == "GET":
        file = None
        dir_path = os.path.dirname(os.path.realpath(__file__))
        #ready to serve content
        try:
            file = dir_path+request_info[1]
        except:
            print("no file requested")
        print("file is",file)
        valid_type = file.endswith("html") or file.endswith("htm")
        if file and os.path.isfile(file) and valid_type:
            status = "200"
            response_text = "OK"
            f = open(file,"r")
            text_body = f.read()
            response_header["Content-Length"] = len(text_body)


            response_header = "".join("%s:%s\n"% (key,value) for (key,value) in response_header.items())
            socket.send(str.encode("%s %s %s\n" % (proto,status,response_text),"utf-8"))
            socket.send(str.encode(response_header,"utf-8"))
            socket.send(str.encode("\n"))
            socket.send(str.encode(text_body,"utf-8"))
            print("finished, closing socket")
            socket.close()
            connections.remove(socket)
        else:
            if not os.path.isfile(file):
                status = "404"
                response_text = "NOT FOUND"
            if not valid_type:
                status = "403"
                response_text = "FORBIDDEN"
            socket.send(str.encode("%s %s %s" % (proto, status, response_text), "utf-8"))
            response_header["Content-Length"] = 0
            response_header = "".join("%s:%s\n" % (key, value) for (key, value) in response_header.items())
            socket.send(str.encode(response_header, "utf-8"))
            socket.send(str.encode("\n"))
            socket.close()
            connections.remove(socket)

if __name__ == "__main__":
    port = int(sys.argv[1])
    host = ""
    connections = []
    outputs = []


    #create server socket
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    #add server to the conneciton list
    connections.append(s)

    #listen to the designated port and all IP
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    s.bind((host,port))
    s.listen(5)

    print("server begins to listen on ",host,port)
    while len(connections) > 0:
        readable, writable, exceptional = select.select(connections,
                                                        outputs,
                                                        connections)
        for i in readable:
            #if s is server, that means we have an incoming connection
            if i is s:
                conn,addr = i.accept()
                print("connection from ",addr)
                conn.setblocking(0)
                #add this new socket to connections
                connections.append(conn)
            else:
                #prepare to send data
                data = i.recv(1024)
                if data:
                    print("data received from ",i.getpeername())
                    # print(data)
                # parse data
                    send_data(i,data,connections)

                else:
                    #data is empty, remove it from connections
                    print("closing ",i.getpeername)
                    connections.remove(i)
                    i.close()
