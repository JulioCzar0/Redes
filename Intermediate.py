import sys
import logging
import socket
import threading
import random
import MyTools

try:
    client_port = int(sys.argv[1])
    server_port = int(sys.argv[2])
    lost_probability = float(sys.argv[3])
    mode = sys.argv[4]
    

except:
    print('Datos erróneos en los argumentos...Ingresando al modo interactivo')
    client_port = int (input("Puerto de escucha cliente:"))
    server_port = int (input("Puerto de escucha servidor:"))
    lost_probability = float (input("Probabilidad de pérdida:"))
    mode = input("Para modo debug ingrese 'd' o presione enter para modo normal: ")
    #TO DO Hacer validaciones de los datos.

#Activa el modo DEBUG de ser necesario    
if  mode == 'd':
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

logging.debug(' client_port: %d, server_port: %d, lost_probability %f' %(client_port, server_port, lost_probability))



#--------------Conexion entrante-----------------
# Creando el socket TCP/IP
sock_input = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Enlace de socket y puerto conexion entrante
server_address = ('localhost', client_port)
logging.debug ('Empezando a levantar %s puerto %s' % server_address)
sock_input.bind(server_address)
# Escuchando conexiones entrantes
sock_input.listen(1)
input_connection, client_address = sock_input.accept()


#Establece la conexion entre intermediario y server.  
sock_output, server_address = MyTools.client_connection('localhost',server_port)
sock_output.connect(server_address)


def client_to_server():
    connection_active = True
    while connection_active:
        try:
            data = input_connection.recv(6).decode("utf-8")
            #if data == 'END'
             #   sock_input.shutdown()
              #  sock_input.close()
                #sock_output.sendall(str.encode(data))
               # connection_active = False
            if random.uniform(0,1) > lost_probability:
                logging.debug('Cliente-Servidor: recibiendo  %s, enviando a servidor...' %data)
                sock_output.sendall(str.encode(data))
            else :
                logging.debug('Cliente-Servidor: se perdió el paquete %s' %data)

        except Exception as other:
            logging.debug('Cliente-Servidor: conexión terminada %s' %other)
            connection_active = False
            

def server_to_client():
    connection_active = True
    while connection_active:
        try:            
            data = sock_output.recv(5).decode("utf-8")
            
            if random.uniform(0,1) > lost_probability:
                logging.debug('Servidor-Cliente: recibiendo  ACK%s, enviando a cliente...' %data)
                input_connection.sendall(str.encode(data))
            else:
                logging.debug('Servidor-Cliente: se perdió el paquete %s' %data)

        except Exception as other:
            logging.debug('Servidor-Cliente: conexión terminada %s' %other)
            connection_active = False
            break
    

client2server = threading.Thread(None,client_to_server, 'client2server')
server2client = threading.Thread(None,server_to_client, 'server2client')
client2server.start()
server2client.start()
server2client.join()
client2server.join()
input('Fin')


