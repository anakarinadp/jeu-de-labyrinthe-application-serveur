# -*-coding:Utf-8 -*

"""Ce fichier contient le code principal du jeu coté serveur
Le serveur est qui gère les déplacements et commandes des clients
et envoi le nouveau labyrinthe a chaque client après avoir joué
Il envoie le nouveu labyrinthe a tous les clients connectés après chaque tour
Exécutez-le avecPython pour lance le jeu. (python serveur.py)

"""

import os
import socket
import select

from carte import Carte
from fonctions import *

hote = ''
port = 12800

connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_principale.bind((hote, port))
connexion_principale.listen(5)
print("Le serveur écoute à présent sur le port {}".format(port))

serveur_lance = True
clients_connectes = []
commence = False
msg_recu = ""

# On charge les cartes existantes
cartes = []
for nom_fichier in os.listdir("cartes"):
	if nom_fichier.endswith(".txt"):
		chemin = os.path.join("cartes", nom_fichier)
		nom_carte = nom_fichier[:-3].lower()
		
		with open(chemin, "r") as fichier:
			contenu = fichier.read()
			# Création d'une carte	
			carte = Carte(nom_carte, contenu)
			cartes.append(carte)
			
# On affiche les cartes existantes
print("\nLabyrinthes existants :")
for i, carte in enumerate(cartes):
	print(" {} - {}".format(i + 1, carte.nom))

# On demande à l'utilisateur de saisir une option
choix = input("\nEntrez un número de labyrinthe pour commencer à jouer : ")
while not choix.isnumeric() or len(choix) != 1:
	print("Vous n'avez pas choisie une option valide")
	choix = input("\nEntrez un número de labyrinthe pour commencer à jouer : ")

# L'option choisie est un nombre mais n'est pas dans les options
while int(choix) > len(cartes) or int(choix) < 1:
	print("Vous devez choisir une des options presentées")
	choix = input("\nEntrez un número de labyrinthe pour commencer à jouer : ")

choix = int(choix)

while serveur_lance:
	if not commence:
		connexions_demandees, wlist, xlist = select.select([connexion_principale], [], [], 0.05)
		
		for connexion in connexions_demandees:
			connexion_avec_client, infos_connexion = connexion.accept()
			clients_connectes.append(connexion_avec_client)
		
	clients_a_lire = []
	try:
		clients_a_lire, wlist, xlist = select.select(clients_connectes, [], [], 0.05)
	except select.error:
		pass
	else:
		for client in clients_a_lire:
			msg_recu =client.recv(1024)
			msg_recu = msg_recu.decode()
			print("Reçu {}".format(msg_recu))
			client.send(b"5 / 5")
			if msg_recu == "c":
				print("La partie a commencé")
				commence = True
				#serveur_lance = False

print("Fermeture des connexions")
for client in clients_connectes:
	client.close()
	
connexion_principale.close()