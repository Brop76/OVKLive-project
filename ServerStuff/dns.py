import socket
from dnslib import DNSRecord, QTYPE
from dnslib.dns import RCODE, A, AAAA

# Set the IP and port for the DNS server
DNS_SERVER_HOST = '127.0.0.1'
DNS_SERVER_PORT = 53

# Create a UDP socket for DNS requests
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((DNS_SERVER_HOST, DNS_SERVER_PORT))

print(f"DNS Server started on {DNS_SERVER_HOST}:{DNS_SERVER_PORT}")

# Function to handle incoming DNS requests
def handle_request(data, address):
    try:
        # Parse the DNS request
        request = DNSRecord.parse(data)
        
        # Create a response record
        response = request.reply()

        # Check the type of DNS query (A or AAAA)
        for question in request.questions:
            qname = str(question.qname)
            qtype = QTYPE[question.qtype]

            # Handle A records (IPv4)
            if qtype == 'A':
                if qname == 'example.com.':
                    response.add_answer(*RR.fromZone("example.com. 60 A 93.184.216.34"))
                else:
                    response.header.rcode = RCODE.NXDOMAIN  # No such domain

            # Handle AAAA records (IPv6)
            elif qtype == 'AAAA':
                if qname == 'example.com.':
                    response.add_answer(*RR.fromZone("example.com. 60 AAAA 2606:2800:220:1:248:1893:25c8:1946"))
                else:
                    response.header.rcode = RCODE.NXDOMAIN  # No such domain

        # Send the response back to the client
        server_socket.sendto(response.pack(), address)
        print(f"Sent response to {address}")

    except Exception as e:
        print(f"Error processing request: {e}")

# Main loop to listen for DNS requests
while True:
    try:
        # Receive DNS request from client
        data, address = server_socket.recvfrom(512)  # DNS message max size is 512 bytes
        print(f"Received request from {address}")
        
        # Handle the incoming request
        handle_request(data, address)

    except KeyboardInterrupt:
        print("\nServer shutdown")
        break
    except Exception as e:
        print(f"Error receiving data: {e}")

# Close the socket on exit
server_socket.close()
