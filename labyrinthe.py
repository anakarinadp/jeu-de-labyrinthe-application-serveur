# -*-coding:Utf-8 -*

"""Ce module contient la classe Labyrinthe."""

class Labyrinthe:

	"""Classe représentant un labyrinthe."""
	
	def __init__(self, robot, obstacles, portes, sortie, longueur, hauteur, joueurs, vides):
		self.robot = robot
		self.obstacles = obstacles
		self.portes = portes
		self.sortie = sortie
		self.longueur = longueur
		self.hauteur = hauteur
		self.joueurs = joueurs
		self.vides = vides
	
	