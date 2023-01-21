PARTICIPANTS: Xining Yuan (Part 1 & 2) and Zhenming Wang(Part 3 & 4)

PART 1: a simple curl clone
FUNCTIONS:
default_url(url): 
-- description:
---- a function parse url, to get hostname, port and subpath after GET.
-- input:
---- url: input url
getHTML(host, port, GET, count): 
-- description:
---- a function sending http request, and receiving http response. This function also split http response into header and body. Print the text body to stdout and error message to stderr.
-- input:
---- host: host name
---- port: port name (80 by default)
---- GET: subpath name
---- count: number of redirections (0 by initial)
curl(url):
-- description: a curl clone function to print the body of html.
-- input:
---- url: input url

PART 2: a simple web server
FUNCTIONS:
get_path(data): 
-- description:
---- get path of request html file
-- input:
---- html request message
-- output:
---- path and filename of request html
check_requested_file(path):
-- description:
---- find if the request file exists in current web server folder
-- input:
---- path: path and filename of request html file
-- output:
---- exit code indicating if file exists or not found or in incorrected format
construct_response(status, content):
-- description:
---- status: status code for response
---- content: content of existing html file
-- output:
---- return html response strings
http_server(SERVER_HOST, SERVER_PORT):
-- description:
---- main function to create TCP socket, license to the request, check http request, construct and send http response.
-- input:
---- SERVER_HOST: given host IP (0.0.0.0 by default)
---- SERVER_PORT: given port number


Part 3: Multi-connection HTTP server
to run: python http_server2.py [port]
File Structure: 
- main function: initialize accept socket, listen to incoming connections
- send data: parse the request, check validity, send data 

Part 4: Dynamic HTTP server
to run: python http_server3.py [port] 
File Structure:
- main function: initialize socket, listen to incoming connections
- parse request: parse the request, check validity, do operation, send data 
