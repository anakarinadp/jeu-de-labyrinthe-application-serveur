# -*-coding:Utf-8 -*

"""Ce fichier contient les fonctions principales 
qui vont être apelées pour les autres fichiers"""

import os
import pickle
from labyrinthe import Labyrinthe

def creer_labyrinthe_depuis_chaine(chaine):
	"""Cette fonction crée un objet de type labyrinthe
	et ajoute les eléments principales à partir de chaine"""
	obstacles = []
	portes = []

	i = 0
	x = 0
	y = 0
	while i < len(chaine):
		coord = (x,y)
		if chaine[i] == "O": # Obstacles
			obstacles.append(coord)
			x += 1
		elif chaine[i] == "X": # Robot
			robot = coord
			x += 1
		elif chaine[i] == ".":
			portes.append(coord)
			x += 1
		elif chaine[i] == "U": # Sortie
			sortie = coord
			x += 1
		elif chaine[i] == "\n": # Saut de ligne
			longueur = x + 1
			y += 1
			x = 0
		else: # Space
			x += 1
		i += 1
	
	hauteur  = y + 1
	
	labyrinthe = Labyrinthe(robot, obstacles, portes, sortie, longueur, hauteur)
	return labyrinthe

def afficher_labyrinthe(labyrinthe):
	"""Cette fonction permet d'afficher le labyrinthe
	Reçoit comme paramétre un objet de la classe Labyrinthe"""
	x = 0
	y = 0
	while y < labyrinthe.hauteur:
		while x < labyrinthe.longueur:
			tuple = (x,y)
			if tuple in labyrinthe.obstacles:
				symbole = "O"
			elif tuple == labyrinthe.robot:
				symbole = "X"
			elif tuple in labyrinthe.portes:
				symbole = "."
			elif tuple == labyrinthe.sortie:
				symbole = "U"			
			else:
				symbole = " "
			print(symbole, end = "")
			x += 1
		y += 1
		x = 0
		print("\n", end = "")
	print("\n")
	
def verifier_pos(labyrinthe, commande):
	"""Cette fonction permet de faire le deplacement du robot
	Reçoit la commande saisie et le labyrinthe avec les positions
	actuelles.
	Renvoie un labyrinthe avec les nouvelles positions"""
	
	(x, y) = labyrinthe.robot
	if commande == "N": # Le robot se déplace vers le nord
		if y > 0:
			if(x,y-1) not in labyrinthe.obstacles:
				y -= 1
	elif commande == "E": # Le robot se déplace vers l'est
		if x < labyrinthe.longueur - 1:
			if(x+1,y) not in labyrinthe.obstacles:
				x += 1
	elif commande == "S": # Le robot se déplace vers le sud
		if y < labyrinthe.hauteur - 1:
			if(x,y+1) not in labyrinthe.obstacles:
				y += 1
	else: # Le robot se déplace vers l'ouest
		if x > 0:
			if(x-1,y) not in labyrinthe.obstacles:
				x -= 1
	labyrinthe.robot = (x,y)
	return labyrinthe

def verifier_longueur(chaine):
	"""Cette méthode vérifie la longueur de la chaine et retourne le nombre de positions que le robot doit avancer
	Si la chaine est de longueur 1, la valeur renvoyé est 1, sinon, renvoie la valeur en deuxième position dans la chaine"""
	
	if len(chaine) == 1:
		return 1
	else:
		return int(chaine[1])
