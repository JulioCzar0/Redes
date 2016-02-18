import logging
import socket
import sys
import select
import MyTools


try:
    window_size = int(sys.argv[1])
    file_name = open(sys.argv[2],'r') #Abre el archivo y crea los paquetes
    packets = list(file_name.read())
    file_name.close() #Cierra el archivo  
    destination_port = int(sys.argv[3])
    timeout = float(sys.argv[4])
    mode = sys.argv[5]

except:
    print('Datos erróneos en los argumentos...Ingresando al modo interactivo')
    window_size = int (input("Tamaño de la ventana: "))
    destination_port = int (input("Puerto destino: "))
    file_name = None
    packets = list(input("Ingrese el mensaje que desea enviar: "))
    timeout = float (input("Timeout: "))
    mode = input("Para modo debug ingrese 'd' o presione enter para modo normal: ")
    print(mode)






#...TO DO Hacer validaciones de los datos.  

#Activa el modo DEBUG de ser necesario    
if  mode == 'd':
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    
logging.debug(' ventana: %d, archivo: %s, puerto: %d, timeout: %f' %(window_size, file_name, destination_port, timeout))


             
#Establece la conexion entre cliente e intermediario    
sock_output, server_address = MyTools.client_connection('localhost',destination_port)
sock_output.connect(server_address)

input("Todo listo levante el Server, luego, presione enter para comenzar")

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
    sock_output.settimeout(timeout) #Esto es el timeout

    try :
        data = sock_output.recv(5*window_size).decode("utf-8")

        data = MyTools.split_without_blanks(data,'-')
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
        
print('Mensaje enviado correctamente')
	
input('Fin')
