import socket
from app.dnsmessage import create_dns_response

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this block to pass the first stage
    #
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(("127.0.0.1", 2053))
    #
    while True:
        try:
            buf, source = udp_socket.recvfrom(512)
            print(f"Received data from {source} with length {len(buf)}: {buf}")

            question_section = buf[12:]
            response = create_dns_response(1)
            response += question_section
    
            udp_socket.sendto(response, source)
            print(f"Sent response with length {len(response)}")


        except Exception as e:
            print(f"Error receiving data: {e}")
            break


if __name__ == "__main__":
    main()
