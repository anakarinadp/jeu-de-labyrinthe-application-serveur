# -*- coding:utf-8 -*

import socket

hote = "localhost"
port = 12800

print("On tente de se connecter au serveur...")
connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_avec_serveur.connect((hote, port))
print("Connexion établie avec le serveur.")

commencer = b""
while commencer != b"c":
	commande = input("> ")
	commande = commande.encode()
	connexion_avec_serveur.send(commande)
	commencer = connexion_avec_serveur.recv(1024)
	print(commencer.decode())
	
print("Fermeture de la connexion")
connexion_avec_serveur.close()