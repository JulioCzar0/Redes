import socket


def edit_list(words, func):
    'Toma una lista y le aplica una función a cada uno de sus elementos'
    words_size = len(words)
    for word in range(words_size):
         words[word] = func(word)

def client_connection(server_name,port):
    'Crea un socket y una dirección de servidor necesaria para\
    conectarse a un servidor'
    # Creando un socket TCP/IP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (server_name, port)
    return sock, server_address

def split_without_blanks(a_string, a_separator):
    '''Divide los elementos en una lista
     y elimina los elementos vacíos'''
    a_list = a_string.split(a_separator)
    a_list = list(filter(None,a_list)) #Se eliminan los vacíos
    return a_list
