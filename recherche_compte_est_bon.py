#! /usr/bin/env python3

""" Implémentation des parcours de l’arbre de calculs à la volée :
- parcours en profondeur d’abord itératif
- parcours en profondeur d’abord récursif
- parcours en largeur d’abord itératif """

from TAD.piles_listes_python import Pile
from TAD.files_listes_python import File
from notation_polonaise_inverse import *

OPS = ['+', '-', '*', '/']

def enfants(choisis, restants) :
    # un fils par valeur de carton restante (doublons ignorés)
    fils = [(choisis + [c], restants[:i] + restants[i+1:])
            for i, c in enumerate(restants) if c not in restants[:i]]
    # un opérateur n'est ajouté que s'il y a au moins 2 valeurs à combiner
    if len(choisis) - 2 * sum(t in OPS for t in choisis) >= 2 :
        fils += [(choisis + [o], restants) for o in OPS]
    return fils

def visiter(choisis, cible, meilleur) :
    # meilleur = [écart, expression] ; renvoie False si l'expression est invalide
    valide, valeur = eval_NPI_liste(choisis)
    if valide and valeur is not None and abs(cible - valeur) < meilleur[0] :
        meilleur[:] = [abs(cible - valeur), choisis]
        eval_NPI_liste(choisis, True)
    return valide

def parcours_DFS(cartons, cible) : 
    nb_noeuds = 0
    meilleur = [float('inf'), []]
    pile = Pile()
    pile.empiler(([], cartons))
    while not pile.est_vide() :
        choisis, restants = pile.depiler()
        nb_noeuds += 1
        if not visiter(choisis, cible, meilleur) : continue
        if meilleur[0] == 0 : break
        for noeud in reversed(enfants(choisis, restants)) :
            pile.empiler(noeud)
    return meilleur[1], nb_noeuds

def parcours_BFS(cartons, cible) : 
    nb_noeuds = 0
    meilleur = [float('inf'), []]
    file = File()
    file.enfiler(([], cartons))
    while not file.est_vide() :
        choisis, restants = file.defiler()
        nb_noeuds += 1
        if not visiter(choisis, cible, meilleur) : continue
        if meilleur[0] == 0 : break
        for noeud in enfants(choisis, restants) :
            file.enfiler(noeud)
    return meilleur[1], nb_noeuds 

def parcours_DFS_recursif(cartons, cible) :
    meilleur = [float('inf'), []]
    nb_noeuds = 0

    def parcours_DFSR_aux(choisis, restants) :
        nonlocal nb_noeuds
        nb_noeuds += 1
        if not visiter(choisis, cible, meilleur) : return
        for fils_choisis, fils_restants in enfants(choisis, restants) :
            if meilleur[0] == 0 : return
            parcours_DFSR_aux(fils_choisis, fils_restants)

    parcours_DFSR_aux([], cartons)
    return meilleur[1], nb_noeuds


if __name__ == "__main__":
    parcours_DFS([3,5, 7, 9, 25, 50], 859)
    parcours_BFS([3,5, 7, 9, 25, 50], 859)
    parcours_DFS_recursif([3,5, 7, 9, 25, 50], 859)