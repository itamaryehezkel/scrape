import requests
import socket


def scrape(host="https://www.linkedin.com", uri="/search/results/companies/?keywords=AI%20size:50-500"):

    try:
        headers = {
            "referer": host,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36",
            "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            # "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7",
            "Cache-Control" : "max-age=0"
        }
        # Send a GET request
        response = requests.get(host + uri, headers=headers)

        # Raise an exception for bad status codes (4xx or 5xx)
        response.raise_for_status()

        # Print the status code
        print(f"Status Code: {response.status_code}")

        # Print the response text (e.g., JSON data)
        # print("Response Content:")
        # print(response.text) #.json()) # If the response is JSON, parse it
        return response.text #.encode('utf-16').decode('utf-16')

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")


HOST = '0.0.0.0'  # Listen on all available interfaces
PORT = 8080      # Port to listen on


def parse(data):
    headers_and_body = data.decode().split('\r\n\r\n')
    first_line = []
    headers = {}
    body = headers_and_body[1] if len(headers_and_body) > 1 else ""

    for i, line in enumerate(headers_and_body[0].split('\r\n')):
        if i == 0:
            first_line = line.split(' ')
        else:
            headers[line.split(': ')[0]] = line.split(': ')[1]
    if len(first_line) < 3:
        return {'method': '', 'uri': '', 'version': '', 'body': body, 'headers':headers}
    return {'method': first_line[0], 'uri': first_line[1], 'version': first_line[2], 'body': body, 'headers':headers}


def start_server():
    # Create a TCP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # Enable address reuse
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen()

        print(f"Listening on {HOST}:{PORT}")

        while True:
            client_socket, client_address = server_socket.accept()
            with client_socket:
                print(f"Connection from {client_address}")
                while True:
                    data = client_socket.recv(1024)
                    if not data:
                        break
 
                    
                    req = parse(data)
                 


                    print (req['method'], req['uri'])

                    scraped = scrape(uri=req['uri'])

                    default_type = 'text/html'
                    response = f"HTTP/1.1 200 OK\r\nContent-Type: {default_type}\r\nContent-Length: {len(scraped)}\r\n\r\n{scraped}".encode('utf-8')
                    
                    client_socket.sendall(response)
                    #print (req['headers']['Host'])
                    #print (req['body'])

                  
start_server()