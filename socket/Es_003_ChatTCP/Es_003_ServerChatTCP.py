#La sequenza di operazioni da svolgere per gestire un socket TCP è:
#creazione del socket;
#assegnazione dell'indirizzo;
#connessione o attesa di connessione;
#invio o ricezione dei dati;
#chiusura del socket.


import socket
from threading import Thread
def get_key(val,dizioIPNome): 
    for key, value in dizioIPNome.items():
        if val == value:return key
    return None
def letturaFilePerIP():
    f = open("dati.txt","r")
    righe = f.readlines()
    f.close()
    dizioIPNome={}
    for x in righe[1:]:
        nomeIP = x.split(",")
        dizioIPNome[nomeIP[0]] = nomeIP[1][:-1]
    return dizioIPNome
class MyThread(Thread):
    def __init__(self,s,connection,address,nick):
        Thread.__init__(self)
        self.s = s
        self.running = True
        self.connection =connection
        self.address = address
        self.nick = nick
    def run(self):
        while self.running:
            print(f"{self.nick} sto ascoltando")
            dati = self.connection.recv(4096)
            print(f"\n{dati.decode()}\t inviato da: {self.address}")
            if "|" not in dati.decode():
                self.connection.sendall("Errore di scrittura del messaggio".encode())
            else:
                stringa = dati.decode().split("|")
                if stringa[1] not in dizioIPNome:
                    self.connection.sendall("Destinatario non trovato".encode())
                else:
                    if get_key(self.address[0],dizioIPNome) != None:
                        nome = get_key(self.address[0],dizioIPNome)
                        mex = f"{nome}-->{stringa[0]}"
                        #connection.sendall(mex.encode(),(dizioIPNome[stringa[1]],5000))
                        self.dizio[dizioIPNome[stringa[1]]].sendall(mex.encode())
                    else: 
                        mex = f"sconosciuto -->{stringa[0]}"
                        self.connection.sendall(mex.encode())
    def stop(self):
        self.running = False
thread,dizio,dizioIPNome = [],{},letturaFilePerIP()
def main():
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind(("0.0.0.0",5000)) #La funzione per l'assegnazione di un indirizzo ad un socket
    s.listen() #pone il socket in attesa di una connessione;

    while 1:
        print("In attesa di conessione...")
        connection,address = s.accept() #accetta una connessione sul socket
        if get_key(address[0],dizioIPNome) != None:
            print(f"{get_key(address[0],dizioIPNome)},{address[0]} sono connesso")
            dizio[address[0]] = connection
            thread.append(MyThread(s,connection,address,get_key(address[0],dizioIPNome)))
            thread[-1].start()
        else:
            connection.sendall("Errore".encode())
    for i in thread: i.close()

if __name__=="__main__":
    main()