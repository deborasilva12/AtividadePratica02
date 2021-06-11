from random import randint
import rpyc
from socket import gethostbyname,gethostname
from constRPYC import *
from rpyc.utils.server import ThreadedServer


class ServerCrypt(rpyc.Service): 
    priv_key = 1
    def __encrypt(self, mensagem, pub_key):
        value = ''
        for item in mensagem:
            value = value + chr((ord(item) + pub_key + self.priv_key))
        return value
    
    def __decrypt(self, mensagem, pub_key):
        value = ''
        for item in mensagem:
            value = value + chr((ord(item) - int(pub_key) - self.priv_key))
        return value

    def exposed_encrypt(self, text):
        pub_key = randint(1, 25)
        enc_message = self.__encrypt(text, pub_key)
        return (enc_message, pub_key)

    def exposed_decrypt(self, message, pub_key):
        return self.__decrypt(message, pub_key)


if __name__ == "__main__":
    server = ThreadedServer(ServerCrypt, port = 20203) 
    conn = rpyc.connect(host=DIR_SERVER, port=DIR_PORT)
    my_address = gethostbyname(gethostname())
    (reg, token) = conn.root.exposed_register("ServerCrypt", my_address, 20203)
    if reg:
        print(f"Primeira conexao. Token: {token}")
        server.start()
    else:
        print("Reiniciando")
        option = str(input("1)Atualizar servico.\n 2)Remover servico.\n 3)Cancelar servico\n"))
        if option == "1" or option == "2":
            if option == "1" : 
                token = str(input("Token: "))
                update = conn.root.exposed_update_register("ServerCrypt", my_address, 20203, token)
                if update:
                    print("Atualizado! Inicializando ...")
                    server.start()
                else: 
                    print("Token nao permitido")
            else:
                token = str(input("Token: "))
                remove = conn.root.exposed_unregister("ServerCrypt", token)
                if remove: 
                    print("Servico removido")
                else:
                    print("Token nao permitido")
        else:
            print("Tchauzinho!")