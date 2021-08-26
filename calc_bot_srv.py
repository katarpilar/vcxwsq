#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

import socket
import random
import sys
from threading import Timer


class Server:
    server=""
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    global calcStr, rand1, op, rand2, res
    calcStr = ""
    rand1 = ""
    op = ""
    rand2 = ""
    res = ""

    def __init__(self,server,port):
        self.server=server
        try:
            self.s.bind((server,port))
            print("Server binding complete \n")
        except:
            print("Binding server error")
            sys.exit(2)


    def recvstr(self,socket):
        result=socket.recv(1024)
        while len(result)>0:
            try:
                self._check(str(result.decode()))
                result=socket.recv(1024)
            except:
                print("Connection CLOSED BY CLIENT \n")
                break;
        socket.close()


    def genRandCalc(self,calcType):
        if calcType == 1:
            ran1 = random.randint(0,100)
            ran2 = random.randint(0,100)

            res1 = (ran1 + ran2)
            return ran1, "+", ran2, res1

        elif calcType == 2:
            ran3 = random.randint(0,100)
            ran4 = random.randint(0,100)

            res2 = (ran3 - ran4)
            return ran3, "-", ran4, res2

        elif calcType == 3:
            ran5 = random.randint(0,100)
            ran6 = random.randint(0,100)

            res3 = (ran5 * ran6)
            return ran5, "*", ran6, res3


    def sendHelp(self,output):
        print("[", addr, "] valeur inconnue reçue ! : ", output, "len : ", len(output))
        helpStr = "Je n'ai pas compris, voici mon vocabulaire :\nMerci ! : Je vous envoie un calcul à résoudre mais j'ai la mémoire courte ! Vous devez me répondre le résultat en moins de 3 secondes. \nn1 : Je vous envoie le premier nombre du calcul. \nn2 : Je vous envoie le deuxième nombre du calcul. \nop : Je vous envoie l'opérateur à utiliser (+, -, *)\n\n"
        conn.send(helpStr.encode())


    def _check(self,output):
        global calcStr, rand1, op, rand2, res
        def calcReset():
            global calcStr, rand1, op, rand2, res
            calcStr = ""
            rand1 = ""
            op = ""
            rand2 = ""
            res = ""
            print("[", addr, "] calcul effacé")

        if output == "Merci !\n":
            print("[", addr, "] Merci ! reçu, len : ", len(output))
            randCalcType = random.randint(1,3)
            rand1, op, rand2, res = self.genRandCalc(randCalcType)
            calcStr = str(rand1) + op + str(rand2) + "\n"
            conn.send(calcStr.encode())
            print("[", addr, "] calcul envoyé : ", calcStr)
            t = Timer(interval=3.0, function=calcReset)
            t.start()

        elif output == "n1\n":
            if rand1 != "":
                conn.send(str(rand1).encode())
                print("[", addr, "] nombre 1 envoyé : ", rand1)
            else:
                polisStr = "Vous n'avez pas appris la politesse ?\n"
                conn.send(polisStr.encode())

        elif output == "n2\n":
            if rand2 != "":
                conn.send(str(rand2).encode())
                print("[", addr, "] nombre 2 envoyé : ", rand2)
            else:
                polisStr = "Vous n'avez pas appris la politesse ?\n"
                conn.send(polisStr.encode())

        elif output == "op\n":
            if op != "":
                conn.send(str(op).encode())
                print("[", addr, "] opérateur envoyé : ", op)
            else:
                polisStr = "Vous n'avez pas appris la politesse ?\n"
                conn.send(polisStr.encode())

        elif res != "":
            if output == (str(res) + "\n"):
                with open('/var/www/root.txt', 'r') as file:
                    flag = file.read().replace('\n', '')
                #flag = "87ez74ds12"
                flagStr = ("Bravo ! Voici le flag : " + flag)
                conn.send(flagStr.encode())
                print("[", addr, "] flag envoyé : ", flag)
            else:
                self.sendHelp(output)

        else:
            self.sendHelp(output)


print("Server Starting\n")
sock=Server("0.0.0.0",54321)
print("Server STARTED")
while True:
    sock.s.listen(1)
    conn,addr=sock.s.accept()
    print("Connexion de : {0}:{1} \n".format(addr[0],str(addr[1])))
    conn.send("Bienvenue ! (Les gens polis répondent 'Merci !')\n".encode())
    sock.recvstr(conn)
