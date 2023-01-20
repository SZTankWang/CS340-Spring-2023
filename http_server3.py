import socket
import sys
import re
import json

def parse_request(data):
    #get the first line of the request, with method, url
    data = data.decode("utf-8").split("\r\n")[0].split(" ")
    try:
        url = data[1]
    except IndexError:
        print("no data available, exiting")
        return
    #check if requesting product
    match = re.search(r"(/\w+)",url)
    status = 400
    phrase = None
    operands = []
    if match is not None and match.group(1) == "/product":
        print("valid request")
        #get the operands. get everything after ?
        params = re.search(r"^.*\?(.*)$",url)
        if params is not None:
            params = params.group(1).split("&")
            print(params)
            #use a loop to calculate result, keep an eye on invalid operand
            result = 1
            success = True
            overflow = False

            for i in params:
                operand = re.search(r"^.*=(.*)",i)
                if operand is not None:
                    operand = operand.group(1)
                    try:
                        operand = float(operand)
                        operands.append(operand)
                        result *= operand
                        if abs(result) == float("inf"):
                            raise OverflowError
                    except ValueError:
                        # print("invalid operand")
                        success = False
                        break
                    except OverflowError:
                        success = False
                        overflow = True
                        result = "inf"
                        break

                else:
                    # print("no operand found")
                    success = False
                    break
            if success:
                status = 200
                phrase = "OK"
                # print("result",result)

            else:
                #there exists invalid params
                status = 400
                phrase = "Bad Request"
                result = None if not overflow else "inf"
        else:
            #no params
            # print("no params")
            status = 400
            result = None
            phrase = "Bad Request"

    else:
        # print("invalid")
        status = 404
        phrase = "Not Found"
        result = None
    return status, phrase, result, operands

if __name__ == "__main__":
    host = ""
    port = int(sys.argv[1])

    proto = "HTTP/1.1"

    response_header = {
        'Content-Type': 'Content-Type: application/json',
        "Connection":"close"
    }

    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    s.bind((host,port))
    s.listen(5)

    while True:
        conn,addr = s.accept()
        data = conn.recv(1024)
        status, phrase, result, operands = parse_request(data)
        print(status,phrase,result,operands)

        conn.send(str.encode("%s %s %s\n" % (proto, status, phrase), "utf-8"))

        header = "".join("%s:%s\n" % (key, value) for (key, value) in response_header.items())

        conn.send(str.encode(header, "utf-8"))

        conn.send(str.encode("\n"))
        response_body = json.dumps(({"operation":"product","operands":operands,"result":result}))
        conn.send(bytes(response_body,encoding="utf-8"))
        conn.close()


