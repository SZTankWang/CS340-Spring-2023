# Part 1: A Simple Curl Clone
import socket, sys
# code from external sources:
# constructing http send, http response, received help from
# http://www.coolpython.net/python_senior/network/socket_send_http_request.html


def default_url(url):
    url_sep = url.split('/')
    url_sep = [i for i in url_sep if i != '']
    if len(url_sep) < 3:
        GET = ""
    else:
        GET = url_sep[2]
    if url_sep[0] == 'https:':
        print('visit a https page', file = sys.stderr)
        # sys.exit('visit a https page')
        sys.exit(1)
    port = ""
    for i in url_sep:
        if ":" in i:
            for j in range(len(i)):
                if i[j] == ":":
                    port += i[j+1:len(i)]
                    break
    host = url_sep[1]
    host = host.strip(port)
    host = host.strip(":")
    if port == "":
        port = 80
    return host, port, GET

def getHTML(host, port, GET, count):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, int(port)))
    request_url = 'GET /' + GET + ' HTTP/1.1\r\nHost:' + host + '\r\nConnection:close\r\n\r\n'
    sock.send(request_url.encode())
    response = b''
    rec = sock.recv(1024)
    while rec:
        response += rec
        rec = sock.recv(1024)
    # print(request_url.encode())

    index = response.find(b'\r\n\r\n')
    head = response[:index]
    body = response[index+4:]
    headers = head.split(b'\r\n')

    body_output = ''
    for header in headers:
        if header.startswith(b'HTTP/1.1'):
            response_code = int(header.split(b' ')[1])
        if header.startswith(b'Content-Type'):
            tmp = header.split(b': ')[1].split(b' ')
            encode_text = ''
            if len(tmp) > 1:
                encode_text = tmp[1].split(b'=')[1]
            body_type = tmp[0]
            if body_type == b'text/html' or body_type == b'text/html;':
                body_output = body
                tmp = header.split(b': ')[1].split(b' ')
                if encode_text == '':
                    encode_type = 'utf-8'
                else:
                    encode_type = encode_text.decode()

    if response_code == 301 or response_code == 302:
        count += 1
        if count == 10:
            sys.exit('redirect more than 10 times')
            return 1
        for header in headers:
            if header.startswith(b'Location'):
                Location = header.split(b' ')[1]
                print('Redirected to:', Location.decode())
                host1, port1, GET1 = default_url(Location.decode())
                getHTML(host1, port1, GET1, count)
    elif response_code == 200:
        if body_output == '':
            sys.exit('not text/html')
            # return 1
        else:
            # print(body_output.decode(), file = sys.stdout)
            print(body_output.decode(encode_type), file = sys.stdout)
            sys.exit(0)
            # return 0
    elif response_code >= 400:
        if body_output != '':
            # print(body_output.decode(), file = sys.stdout)
            print(body_output.decode(encode_type), file = sys.stdout)
            sys.exit('response code greater than 400')
            # return 0

def curl(url):
    host, port, GET = default_url(url)
    getHTML(host, port, GET, 0)
    
if __name__ == '__main__':
    try:
        http_url = sys.argv[1]
        curl(http_url)

    except Exception as e:
        # sys.exit('not enough args')
        print(e)