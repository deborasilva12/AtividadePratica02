import rpyc
from constRPYC import *

class Client:
    conn_directory = rpyc.connect(DIR_SERVER, DIR_PORT)
    (address, port) = conn_directory.root.exposed_lookup("ServerCrypt")
    if address == 'error':
        print(port)
    else:
        print(f"Conexao: {address}:{port}")
        conn_server = rpyc.connect(address, port)
        operation = str(input("1)Criptografar \n 2)Descriptografar \n 3) Cancelar\n"))
        if operation == "1" or operation == "2":
            if operation == "1":
                text = input("Mensagem: ")
                (encText, pub_key) = conn_server.root.exposed_encrypt(text)
                print(f"Criptografada: {encText}\n Public Key {pub_key}")
                file = open("enc_message.txt", 'w')
                file.write(encText)
                file.close()
            else:
                file = open("enc_message.txt", 'r')
                enc_message = file.read()
                file.close()
                print(f"Mensagem criptografada: {enc_message}")
                pub_key = input("Public Key: ")
                text = conn_server.root.exposed_decrypt(enc_message, pub_key)
                print(f"Mensagem: {text}")
        else:
            print("Tchauzinho!")
