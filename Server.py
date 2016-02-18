import logging
import socket
import sys


try:
    listening_port = int(sys.argv[1])
    mode = sys.argv[2]    

except:
    print('Datos erróneos en los argumentos...Ingresando al modo interactivo')
    listening_port = int (input("Puerto de escucha:"))
    mode = input("Para modo debug ingrese 'd' o presione enter para modo normal: ")
#Activa el modo DEBUG de ser necesario    
if  mode == 'd':
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

logging.debug(' puerto: %d' %listening_port)


#...TO DO Hacer validaciones de los datos.

#Toma un string de tipo #:caracter y lo almacena en un diccionario 
data_buffer = dict()



#--------------Conexion entrante-----------------
# Creando el socket TCP/IP
sock_input = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Enlace de socket y puerto conexion entrante
server_address = ('localhost', listening_port)
logging.debug ('Empezando a levantar %s puerto %s' % server_address)
sock_input.bind(server_address)

# Escuchando conexiones entrantes
sock_input.listen(1)
input_connection, client_address = sock_input.accept()

data_buffer = {}
data_size = 10000		

while len(data_buffer) < data_size <= 10000:
    try:
        
        data = input_connection.recv(6).decode("utf-8")
        msg_chunk = data.split(':')

        #Se llena el dictionary data_buffer con key= número secuencia y value=caracter
        if len(msg_chunk) > 2:
            data_buffer[int(msg_chunk[0])] = ':'
        else:
            data_buffer[int(msg_chunk[0])] = msg_chunk[1]

        #Enviar ACK del paquete
        logging.debug(data_buffer)
        input_connection.sendall(str.encode(msg_chunk[0]+'-'))
        logging.debug('Enviando ACK'+msg_chunk[0])
    except Exception as other:
        logging.debug('Error inesperado %s' %other)
        break

#...TO DO pasar a archivo
#fout = open('message.txt', 'a')
#fout.write(data_buffer[int(msg_chunk[0])])
#fout.close()
#-----------------------------------------------------------------#
    
input('Fin')
