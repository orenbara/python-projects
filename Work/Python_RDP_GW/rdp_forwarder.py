"""
Main Code:
- create a new thread for listening purpose - this design will allow managing stuff from main
- join the threads

def listeting_server:
- will create new server socket - and start listening
- TODEL: define a list of IP addresses for destinations
- will accept connections for client on pre-defined port (WHILE LOOP)
    - will create a client socket for a client request.
    - will define 2 threads for client communication and send the client sockets to these threads
        - the threads will call the forward function will connect the client to the destination server.

def forward(source, destination, description):
The design is using 2 threads wich will read from source and send to destination
- will receive 2 sides of a connection (forward_server and destination
  server and the other whey around on the corresponding thread)
- will run a while loop and read from the source - send all to the destination
"""
import socket
import threading
import logging

# VARS:
gw_listen_tcp_port = 33890  # PORT to listen for incoming requests
gw_listen_tcp_ip = "5.100.253.143"
target_list = ["63.250.63.51"]  # Temporal list of IPs which are target RDP servers - this is for testing
target_server_tcp_port = 3389  # The port in which all the target servers are listening for in RDP.

# Max TCP connections allowed in queue
# These connections are in queue since the server could not deal with them
max_conns = 5

def main():
    ##### Logging #####
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.DEBUG, datefmt="%H:%M:%S")

    # Create a new thread - so it would be easy to operate stuff outside the gateway operations
    listening_thread = threading.Thread(target=listening_func)
    listening_thread.start()
    listening_thread.join()


def listening_func():
    try:
        # Create new socket which will serve as listening socket
        listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind listening socket to relevant host:port using tuple
        listening_socket.bind((gw_listen_tcp_ip, gw_listen_tcp_port))
        logging.info("Listening socket was bound to %s:%s" %(gw_listen_tcp_ip, gw_listen_tcp_port))

        # Make the listening socket listen
        listening_socket.listen(max_conns)
        logging.info("Listening socket started listening on %s:%s" % (gw_listen_tcp_ip, gw_listen_tcp_port))

        while True:
            # Accept client request for connecting a target server
            client_socket, client_address = listening_socket.accept()

            logging.info("Accepted client request by the GW:\n"
                         "Client Host: %s\n"
                         "Client Port: %s" % (client_address[0], client_address[1]))

            # Create another client side socket which will connect to the target server
            target_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # TODO: implement capturing of target server from RDP cookie
            # Connect the socket to the target server
            destination_rdp_server = target_list[0]     # This is temporal for testing
            logging.info("Client %s will be forwarded to target RDP server:\n"
                         "Target Host: %s" % (client_address[0], destination_rdp_server))

            target_server_socket.connect((destination_rdp_server, target_server_tcp_port))

            # Create 2 threads for bidirectional TCP conversation
            # Thread 1 job: receive data from CLIENT and forward to TARGET
            # Thread 2 job: receive data from TARGET and forward to CLIENT
            threading.Thread(target=start_client_target_communication,
                             args=(client_socket, target_server_socket, "Client Data Puller")).start()
            threading.Thread(target=start_client_target_communication,
                             args=(target_server_socket,client_socket,  "Target RDP Server Data Puller")).start()


    except Exception as e:
        logging.exception("listening_func caught an exception: %s", e)
        threading.Thread(target=listening_func).start()


def start_client_target_communication( source, destination, info):

    try:
        pulled_data = ' '
        while pulled_data:
            pulled_data = source.recv(1024)
            logging.info("start_client_target_communication: "
                         "info: %s"
                         "data pulled: %s" % (info, pulled_data))
            if pulled_data:
                destination.sendall(pulled_data)
            else:
                # Client\target killed the communication
                source.shutdown(socket.SHUT_RD)
                destination.shutdown(socket.SHUT_WR)

    except Exception as e:
        logging.exception("start_client_target_communication func caught an exception: %s", e)
        logging.info("Closing communication sockets client and target")
        source.close()
        destination.close()


if __name__ == '__main__':
    main()
