import logging
import socket
import sys
import select
import MyTools
from time import sleep 

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
exit = 'e'

while exit == 'E' or exit == 'e':
    window_size = int (input("Tamaño de la ventana:"))
    destination_port = int (input("Puerto destino:"))
    file_name = open(input("Nombre del archivo a enviar:"),"r")
    timeout = float (input("Timeout:"))
    #logging.debug(' ventana: %d, archivo: %s, puerto: %d, timeout: %f' %(window_size, file_name, destination_port, timeout))
    #...TO DO Hacer validaciones de los datos.  
   
    #Establece la conexion entre cliente e intermediario    
    sock_output, server_address = MyTools.client_connection('localhost',10000)
    sock_output.connect(server_address)

    
    #Se crean los paquetes que se van a enviar con un tamaño fijo.
    BARRERA = int (input("Todo listo, ingrese un numero"))
    packets = list(file_name.read())
    #...TO DO hacerlo vía archivo    
    message_size = len(packets)
    for number in range(message_size):
        packet_payload = '0000'+str(number)+':'+packets[number] 
        packets[number] = packet_payload[-6:]    
    logging.debug(' Creación de paquetes: '+str(packets))

    
    
    acks = set()    #se declara un set vacío donde se guardan los acks
    next_ack = 0    #se declara el primer ack que se espera

    #Se revisa si la ventana es mayor que el tamaño del mensaje
    if window_size > len(packets):  
        window_size = len(packets)
        logging.debug('Se cambió el tamaño de ventana a %d debido a que el mensaje a enviar es menor' %window_size)
                          

    #Ciclo de envío de mensajes   
    while next_ack < message_size: 

        previous_ack = next_ack #Se utiliza para saber si llegaron otros ACK.

        for packet_pos in range(window_size):   #envía los mensajes dentro de la ventana
            sock_output.sendall(str.encode(packets[next_ack+packet_pos]))
            logging.debug('Enviando ' +packets[next_ack+packet_pos])

            

        #Recibe los acks
        sock_output.settimeout(2) #Esto es el timeout

        try :
            data = sock_output.recv(5*window_size).decode("utf-8")

            #guarda los acks en el set. USE UN SET XQ NO PERMITE REPETIDOS
            data = data.split('-')
            data = list(filter(None,data)) #Se eliminan los vacíos
            MyTools.edit_list(data, lambda msg_chunk: int(data[msg_chunk]))  
            acks.update(data)
            logging.debug(" ack's recibidos: "+str(acks))

            #Si se encuentra el proximo ACK se corre la ventana
            while next_ack in acks:
                next_ack = next_ack+1

            #Si la ventana es mayor que los paquetes que quedan se reduce su tamaño
            if len(packets)-next_ack < window_size :
                window_size = len(packets)-next_ack
                
            #Se verifica si se movió la ventana o no 
            if previous_ack == next_ack:
                logging.debug('No llegó el ACK esperado. Se reenviará la ventana.')
            
                
        except socket.timeout:
            logging.debug('Timeout vencido. No se recibió nada. Se reenviará la ventana.')
        except Exception as other:
            logging.debug('Error, ocurrió: %s' % other)
        #input('Presione para continuar')#QUITAR esto una vez esté listo todo, ÚTIL PARA DEBUGGEAR
        
        
    print('Mensaje enviado correctamente')
    exit = input('Mensaje entregado. Presione: "e" para enviar otro mensaje | "q"  para salir.\n>>')	
input('Fin')

#Eliminados ESTO NO CREO QUE LO USEMOS ESTÁ AQUÍ X SI ACASO PERO SE PRETENDE ELIMINAR:
#logging.basicConfig(filename = 'debugSession.log', format='%(levelname)s:%(message)s', level=logging.DEBUG)
#packet_payload = '0000'+'#:'+str(message_size)
#packets.append(packet_payload[-6:])
#Pone el timeout y revisa actualiza el ACK                
#sleep(2.0)
#ready = select.select(sock_output,None,None,2)
#if ready[0] :
