import logging
import socket
import threading
import random
import MyTools

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
#client_port = int (input("Puerto de escucha cliente:"))
#server_port = int (input("Puerto de escucha servidor:"))
#lost_probability = float (input("Probabilidad de pérdida:"))

#logging.debug(' client_port: %d, server_port: %d, lost_probability %f' %(client_port, server_port, lost_probability))
#TO DO Hacer validaciones de los datos.

#def start_server():
#'Recibe datos de un  cliente y los envía a un servidor'
#-Conexion entrante---del Cliente--------------
# Creando el socket TCP/IP
sock_input = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Enlace de socket y puerto conexion entrante
server_address = ('localhost', 10000)
logging.debug ('Empezando a levantar %s puerto %s' % server_address)
sock_input.bind(server_address)
# Escuchando conexiones entrantes
sock_input.listen(1)
input_connection, client_address = sock_input.accept()

#Establece la conexion entre intermediario y server.  
sock_output, server_address = MyTools.client_connection('localhost',10001)
sock_output.connect(server_address)


def client_to_server():
    connection_active = True
    while connection_active:
        try:
            data = input_connection.recv(6).decode("utf-8")
            #if data = 'END'
            #    sock_input.shutdown()
            #    sock_input.close()
            #    connection_active = False
            if random.uniform(0,1) < 0.5:
                print(client_address)
                print(data)
                sock_output.sendall(str.encode(data))
            else :
                print('Se perdió %s' %data)

        except Exception as other:
            logging.debug('Conexion con cliente terminada %s' %other)
            connection_active = False
            break

def server_to_client():
    connection_active = True
    while connection_active:
        try:
            data = sock_output.recv(5).decode("utf-8")
            print('Servidor dice: %s' %data)
            input_connection.sendall(str.encode(data))

        except Exception as other:
            logging.debug('Conexion con server terminada %s' %other)
            connection_active = False
            break
    

client2server = threading.Thread(None,client_to_server, 'client2server')
server2client = threading.Thread(None,server_to_client, 'server2client')
client2server.start()
server2client.start()
server2client.join()
client2server.join()
input('Fin')


