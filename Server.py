import logging
import socket
import sys

#logging.basicConfig(filename = 'debugSession.log', format='%(levelname)s:%(message)s', level=logging.DEBUG)
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
listening_port = int (input("Puerto de escucha:"))
logging.debug(' puerto: %d' %(listening_port))

#...TO DO Hacer validaciones de los datos.
#...TO DO poner el nombre de archivo como la hora.

#Toma un string de tipo #:caracter y lo almacena en un diccionario 
data_buffer = dict()

#packet = input("Recibiendo mensaje...")

#--------------Conexion entrante-----------------
# Creando el socket TCP/IP
sock_input = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Enlace de socket y puerto conexion entrante
server_address = ('localhost', 10001)
logging.debug ('Empezando a levantar %s puerto %s' % server_address)
sock_input.bind(server_address)

# Escuchando conexiones entrantes
sock_input.listen(1)
input_connection, client_address = sock_input.accept()

#-------------Conexion saliente-------------------
# Creando el socket TCP/IP
#sock_output = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conecta el socket en el puerto cuando el servidor esté escuchando
#server_address = ('localhost', 10001)
#sock_output.connect(server_address)


data_buffer = {}
data_size = 10000
file_recive = open("Results.txt","w")

while len(data_buffer) < data_size <= 10000:
    try:
        
        data = input_connection.recv(6).decode("utf-8")
        print(client_address)
        msg_chunk = data.split(':')

        #Se llena el dictionary data_buffer con key= número secuencia y value=caracter
        if '#' in msg_chunk[0]:
            data_size = int(msg_chunk[1])
            print('llegué')
        elif len(msg_chunk) > 2:
            data_buffer[int(msg_chunk[0])] = ':'
        else:
            data_buffer[int(msg_chunk[0])] = msg_chunk[1]

        #Enviar ACK del paquete
        print(data_size)
        print(data_buffer)
        input_connection.sendall(str.encode(msg_chunk[0]+'-'))
        logging.debug('Enviando ACK'+msg_chunk[0])
        file_recive.write(data_buffer[int(msg_chunk[0])])
    except Exception as other:
        logging.debug('Error inesperado %s' %other)
        break

#...TO DO pasar a archivo
#fout = open('message.txt', 'a')
#fout.write(data_buffer[int(msg_chunk[0])])
#fout.close()
#-----------------------------------------------------------------#
file_recive.close()    
input('Fin')
