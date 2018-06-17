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

# Les commandes a utiliser
commandes = ["Q", "N", "E", "S", "O", "m", "p"]

connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_principale.bind((hote, port))
connexion_principale.listen(5)
print("Le serveur écoute à présent sur le port {}".format(port))

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
# isnumeric() renvoie True pour "e" et "g", c'est pour ça que je les ai ajouté dans les conditions
while not choix.isnumeric() or len(choix) != 1 or choix == "e" or choix == "g":
	print("Vous n'avez pas choisie une option valide")
	choix = input("\nEntrez un número de labyrinthe pour commencer à jouer : ")

# L'option choisie est un nombre mais n'est pas dans les options
while int(choix) > len(cartes) or int(choix) < 1:
	print("Vous devez choisir une des options presentées")
	choix = input("\nEntrez un número de labyrinthe pour commencer à jouer : ")

choix = int(choix)

# On affiche le labyrinthe
print("\n")
for i, carte in enumerate(cartes):
	if i+1 == choix:
		labyrinthe = carte.labyrinthe
		afficher_labyrinthe(labyrinthe)
		#print("Hauteur: {}, longueur: {}".format(labyrinthe.hauteur, labyrinthe.longueur))

premier = True
joueur = 0
commence = False
serveur_lance = True
clients_connectes = []
msg_recu = ""

while serveur_lance:
	if not commence:
		connexions_demandees, wlist, xlist = select.select([connexion_principale], [], [], 0.05)
		
	for connexion in connexions_demandees:
		joueur += 1
		connexion_avec_client, infos_connexion = connexion.accept()
		clients_connectes.append(connexion_avec_client)
		
		msg_bienvenue = "Bienvenue, joueur " + str(joueur) + ".\n\n\n"
		#msg_bienvenue = msg_bienvenue.encode()
		#connexion_avec_client.send(msg_bienvenue)
		
		if joueur != 1:
			labyrinthe = creer_robot(labyrinthe)
		chaine_labyrinthe = convertir_labyrinthe_en_chaine(labyrinthe)
	
		#envoyer = chaine.encode()
		#connexion_avec_client.send(envoyer)
		
		chaine_commencer = "\n\nEntrez C pour commencer à jouer :\n "
		
		msg_a_envoyer = msg_bienvenue + chaine_labyrinthe + chaine_commencer
		msg_a_envoyer = msg_a_envoyer.encode()
		connexion_avec_client.send(msg_a_envoyer)
		
		msg_recu = connexion_avec_client.recv(1024)
		msg_recu = msg_recu.decode()
		print("Reçu: {}".format(msg_recu))
		
		"""if  msg_recu == "c":
			msg_a_envoyer = "\n\nLa partie commence\n "
			msg_a_envoyer = msg_a_envoyer.encode()
			connexion_avec_client.send(msg_a_envoyer)
			commence = True
		
		if not commence and joueur > 1:
			msg_recu = connexion_avec_client.recv(1024)
			msg_recu = msg_recu.decode()
			if msg_recu.lower() == "c":
				print("Reçu c, la partie commence")
				commence = True
		
		if commence:
			msg_a_envoyer = "La partie commence !"
			msg_a_envoyer = msg_a_envoyer.encode()
			connexion_avec_client.send(msg_a_envoyer)
			
	clients_a_lire = []
	try:
		clients_a_lire, wlist, xlist = select.select(clients_connectes, [], [], 0.05)
	except select.error:
		pass
	else:
		for client in clients_a_lire:
			if not commence:
				chaine = convertir_labyrinthe_en_chaine(labyrinthe)
				envoyer = chaine.encode()
				client.send(envoyer)
			#msg_recu =client.recv(1024)
			#msg_recu = msg_recu.decode()
			#print("Reçu {}".format(msg_recu))
		#for client in clients_connectes:
			client.send(b"5 / 5")
			#print("Clients connectés: {}".format(len(clients_connectes)))
			if msg_recu == "c" and len(clients_connectes) > 1:
				print("La partie a commencé")
				commence = True
				#serveur_lance = False
	"""
print("Fermeture des connexions")
for client in clients_connectes:
	client.close()
	
connexion_principale.close()