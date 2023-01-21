import os, socket, sys
# code from external sources:
# constructing http server, received help from
# http://www.coolpython.net/python_senior/network/tcp_web_server.html

def get_path(data):
    index = data.find("\r\n")
    if index == -1:
        return ""
    first_line = data[:index]
    arrs = first_line.split()
    if len(arrs) != 3:
        return ""
    path = arrs[1]
    return path

def check_requested_file(path):
    if path == '/':
        return -1
    else:
        requested_file = path[1:]
        if os.path.exists(requested_file):
            tmp = requested_file.split('.')
            if len(tmp) > 1:
                if tmp[-1] == 'htm' or tmp[-1] == 'html':
                    return 200
                else:
                    return 403
            else:
                return 404

def construct_response(status, content):
    head_string = "HTTP/1.1 %s \r\nServer: simple server \r\n"\
        "Content-Type: text/html; charset=utf-8\r\n"\
            "Content-Length: %d\r\nConnection: close\r\n\r\n"%(status, len(content.encode('utf-8')))
    return head_string + content

def http_server(SERVER_HOST, SERVER_PORT):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(1)
    print('Listening on port %s ...' % SERVER_PORT)

    while True:
        client_connection, client_address = server_socket.accept()
        request = client_connection.recv(1024).decode()
        path = get_path(request)

        exist_flag = check_requested_file(path)
        if exist_flag == 200:
            fin = open(path[1:])
            content = fin.read()
            fin.close()
            message = construct_response('200 OK', content)
        if exist_flag == 404:
            message = 'HTTP/1.0 404 Not Found\n\nFile Not Found'
        if exist_flag == 403:
            message = 'HTTP/1.0 403 Forbidden\n\nForbidden'

        client_connection.sendall(message.encode())
        client_connection.close()

    server_socket.close()

if __name__ == '__main__':
    try:
        http_server('0.0.0.0', int(sys.argv[1]))
    except Exception as e:
        print(e)
