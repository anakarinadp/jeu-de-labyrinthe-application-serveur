# -*-coding:Utf-8 -*

"""Ce fichier contient les fonctions principales 
qui vont être apelées pour les autres fichiers"""

import os
import pickle
import random
from labyrinthe import Labyrinthe

def creer_labyrinthe_depuis_chaine(chaine):
	"""Cette fonction crée un objet de type labyrinthe
	et ajoute les eléments principales à partir de chaine"""
	obstacles = []
	portes = []
	joueurs = []
	vides = []

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
			longueur = x
			y += 1
			x = 0
		else: # Space
			x += 1
			if coord != (10,10):
				vides.append(coord)
		i += 1
	
	hauteur  = y + 1
	
	obstacles.sort()
	portes.sort()
	vides.sort()
	
	labyrinthe = Labyrinthe(robot, obstacles, portes, sortie, longueur, hauteur, joueurs, vides)
	return labyrinthe

def creer_robot(labyrinthe):
	"""Fonction permettant de créer le robot de forme aleatorire"""
	labyrinthe.joueurs.append(labyrinthe.robot)
	robot = random.choice(labyrinthe.vides)
	labyrinthe.robot = robot
	labyrinthe.vides.remove(robot)	
	return labyrinthe

def convertir_labyrinthe_en_chaine(labyrinthe):
	"""Cette fonction reçoi un labyrinthe et fait la transformation
	en chaine de caractères pour pouvoir lui envoyer au client"""
	
	x = 0
	y = 0
	chaine = ""
	
	#print("Sortie: {}".format(labyrinthe.sortie))
	
	while y < labyrinthe.hauteur:
		while x < labyrinthe.longueur + 1:
			coord = (x,y)
			if coord in labyrinthe.obstacles:
				symbole = "O"
			elif coord in labyrinthe.portes:
				symbole = "."
			elif coord == labyrinthe.sortie:
				symbole = "U"
			elif coord in labyrinthe.joueurs:
				symbole = "x"
			elif coord == labyrinthe.robot:
				symbole = "X"
			elif coord in labyrinthe.vides:
				symbole = " "
			else: 
				symbole = "\n"
			chaine += symbole
			x += 1		
		x = 0
		y += 1
		
	return chaine
		
	
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
