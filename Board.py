#!/usr/bin/env python
# -*- coding: utf-8 -*-

from copy import deepcopy
from Case import Case
import numpy as np
from matplotlib import pyplot as plt


class Board(object):

    VIDE = 0
    DANGER = 1
    FIN = 2

    def __init__(self, height=None, width=None, recompence=None, move_proba=None, board=None):
        """

        :param height: Largeur du plateur
        :param width: hauteur du plateru
        :param recompence: Liste des recompence posible. Sous la forme [case vide, case dangereur, fin]
        :param move_proba: probabiliter de réusite pour chaque move. Sous le forme
                            {'n': {'n': proba d'aller au nord, 's': proba daller au sud sachant le nord, ...},
                            's': idem que n, 'e': ..., 'w': ...}
        :param board: Plateaux du robot
        """

        self.height = height if height is not None else 3
        self.width = width if width is not None else 4
        self.recompence = recompence if recompence is not None else [-0.04, -1, 1]
        self.move_proba = move_proba if move_proba is not None else {"n": {"n": 0.8, "s": 0, "w": 0.1, "e": 0.1},
                                                                     "s": {"n": 0, "s": 0.8, "w": 0.1, "e": 0.1},
                                                                     "e": {"n": 0.1, "s": 0.1, "w": 0, "e": 0.8},
                                                                     "w": {"n": 0.1, "s": 0.1, "w": 0.8, "e": 0}}

        # r est si le robot rebon sur un bord ou obstacle
        self.move_pattern = {"n": [-1, 0], "s": [1, 0], "e": [0, 1], "w": [0, -1], "r": [0, 0]}
        # position sous la forme [y, x]
        self.player_pos = None
        self.target_pos = None

        if board is None:

            self.mat = list()

            for _ in range(self.height):
                self.mat.append([Case(Case.VIDE, self.recompence[Board.VIDE]) for _ in range(self.width)])

            self.mat[0][3].type = Case.FIN
            self.mat[0][3].recompense = self.recompence[Board.FIN]

            self.mat[2][0].type = Case.START
            self.mat[2][0].recompense = self.recompence[Board.VIDE]

            self.mat[1][3].type = Case.DANGER
            self.mat[1][3].recompense = self.recompence[Board.DANGER]

            self.mat[1][1].type = Case.OBSTACLE

            self.player_pos = [2, 0]
            self.target_pos = [0, 3]
        else:
            self.mat = deepcopy(board)
            # recharche du depart est de l'ariver
            for y in range(self.height):
                for x in range(self.width):
                    if self.mat[y][x].type == Case.START:
                        self.player_pos = [y, x]
                    elif self.mat[y][x].type == Case.FIN:
                        self.player_pos = [y, x]

                    if self.player_pos is not None and self.target_pos is not None:
                        break

    def get_dim(self, dim, mat):
        """
        Focntion qui recupaire une dimention donnée dans une matrice 3D
        exemple: mat = [[[1, 2, 3], [4, 5, 6]], [[10, 20, 30], [40, 50, 60]]]
                dim = 1
                return = [[2, 5], [20, 50]]
        :param dim: dimention a recuperer
        :param mat:
        :return:
        """
        res_mat = list()
        for ligne in mat:
            res_ligne = list()
            for colomne in ligne:
                try:
                    res_ligne.append(colomne[dim])
                except IndexError:
                    res_ligne.append(None)
            res_mat.append(res_ligne)
        return res_mat

    def get_politique(self, mat_utiliter):
        """
        En fonction de l'utiliter donnée on renvoie la politique
        :param mat_utiliter: matrice d'utiliter qui est de la dimention du tableau
        :return: une matrice de politique sous la forme [['w', 'w', ..., 'w'],
                                                         ['s', ...]
                                                         ...
        """
        mat_politique = [['n'] * self.width for _ in range(self.height)]
        for y in range(len(mat_utiliter)):
            for x in range(len(mat_utiliter[0])):
                # liste argument qui contient le calcule max pour chaque direction souhaiter
                # en position 0 la valeur de largument. En position 1 la valeur de la politique
                arg_list = [[], []]
                possible_move = self.get_move([y, x])
                for wanted_move in possible_move:
                    arg_list[0].append(0)
                    arg_list[1].append(wanted_move)
                    for prob_move in possible_move[wanted_move]:
                        # on deplasse le joueur
                        new_x = x + self.move_pattern[prob_move][1]
                        new_y = y + self.move_pattern[prob_move][0]
                        # On regarde que le déplasement est possible (donc sa proba n'est pas = 0)
                        if possible_move[wanted_move][prob_move] != 0:
                            arg_list[0][-1] += possible_move[wanted_move][prob_move] * mat_utiliter[new_y][new_x]
                # on recupaire la molitique assotier au plus grands argument
                mat_politique[y][x] = arg_list[1][arg_list[0].index(max(arg_list[0]))]
        return mat_politique

    def iteration_valeur(self, escompte=1, err_conv=0.1):
        """
        calcule les utiliter de la matrice mat
        :param escompte: Facteur d'escompte sur
        :param err_conv: taux erreur entre chaque iteration
        :return: une matrice utiliter pour chaque case
        """
        # on cree une matrice utiliter ou chaque case est une liste qui va contenir l'historique des utiliter calculer
        utility_mat = list()
        for y in range(self.height):
            utility_mat.append([[self.mat[y][x].recompense] for x in range(self.width)])
        # Var n pour rajouter une puissance
        n = 0
        while True:
            n += 1
            # on parcour tout le plateau
            for y in range(len(self.mat)):
                for x in range(len(self.mat[0])):
                    # On calcule que les case vide
                    if self.mat[y][x].type == Case.FIN or \
                            self.mat[y][x].type == Case.DANGER or \
                            self.mat[y][x].type == Case.OBSTACLE:
                        # Si c'est une case qui ne dois pas êtres modifier on cree une case dans notre historique
                        # qui contien juste la récompense de la dite case
                        utility_mat[y][x].append(self.mat[y][x].recompense)
                        continue
                    # Liste temporaire qui va contenir tout les calcule de l'utiliter
                    val_utility = list()
                    # On recupaire tout les moves possible a partire de la position donnée
                    possible_move = self.get_move([y, x])
                    # on parcour tout les moves possible
                    for wanted_move in possible_move:
                        # on cree notre compteur utiliter
                        val_utility.append(0)
                        # on regard qu'elle move je peut aller sachant que je vais a wanted_move
                        for prob_move in possible_move[wanted_move]:
                            # on deplasse le joueur
                            new_x = x + self.move_pattern[prob_move][1]
                            new_y = y + self.move_pattern[prob_move][0]
                            # On regarde que le déplasement est possible (donc sa proba n'est pas = 0)
                            if possible_move[wanted_move][prob_move] != 0:
                                # on mais a jours la derrnière case du tableau
                                val_utility[-1] += possible_move[wanted_move][prob_move] * \
                                                   utility_mat[new_y][new_x][-1] * pow(escompte, n)
                    # une fois tout les utiliter calculer on recupaire la plus intérésente
                    utility_mat[y][x].append(self.mat[y][x].recompense + max(val_utility))
            # on recupaire notre mat utiliter la derrnière est l'avent derrnière
            m1 = np.asarray(self.get_dim(-1, utility_mat))
            m2 = np.asarray(self.get_dim(-2, utility_mat))
            # on fait une soustraction de c'est deux mat
            m_diff = m1 - m2
            # on regarde si la différense est supèrieur a un coef donnée
            temp = np.amax(m_diff)
            if temp < err_conv:
                break
        # une fois tout calculer on recupaire la meilleur utiliter est on trouve sa politique
        return self.get_politique(self.get_dim(-1, utility_mat))

    def get_utility(self, mat_politique, escompte=1):
        """

        :param mat:
        :return:
        """

        a_mat = list()
        b_vector = list()
        # on parcour tout le plateau
        for y in range(len(self.mat)):
            for x in range(len(self.mat[0])):
                a_vector = [0] * (self.height * self.width)
                # On calcule que les case vide
                if self.mat[y][x].type == Case.FIN or \
                        self.mat[y][x].type == Case.DANGER or \
                        self.mat[y][x].type == Case.OBSTACLE:
                    # position dans le vecteur a
                    pos_vector = (y * self.width) + x
                    # si on ne touche pas l'equation est juste eguale a la recompense
                    a_vector[pos_vector] = 1
                    a_mat.append(a_vector)
                    b_vector.append(self.mat[y][x].recompense)
                    continue

                # -1 car comme on passe la recompensse de l'autre cotée de l'égaliter on inverse le signe
                b_vector.append(self.mat[y][x].recompense * -1)
                # On recupaire tout les moves possible a partire de la position donnée
                possible_move = self.get_move([y, x])
                wanted_move = mat_politique[y][x]
                # on regard qu'elle move je peut aller sachant que je vais a wanted_move
                for prob_move in possible_move[wanted_move]:
                    # on deplasse le joueur
                    new_x = x + self.move_pattern[prob_move][1]
                    new_y = y + self.move_pattern[prob_move][0]
                    # position dans le vecteur a
                    pos_vector = (new_y * self.width) + new_x
                    if possible_move[wanted_move][prob_move] != 0:
                        # On regarde si c'est un rebon on retir 1
                        if prob_move == 'r':
                            # -1 car on passe lui maime de l'autre cotée de l'égaliter
                            a_vector[pos_vector] = round(possible_move[wanted_move][prob_move] - 1, 2)
                        else:
                            a_vector[pos_vector] = possible_move[wanted_move][prob_move]
                # on rajoute une nouvelle ligne pour notre equation
                a_mat.append(a_vector)

        print("**A**\n", np.asarray(a_mat))
        print("**B**\n", b_vector)
        utility_vec = np.linalg.solve(np.array(a_mat), np.array(b_vector))
        print("res = ", utility_vec)
        return np.reshape(utility_vec, (self.height, self.width)).tolist()

    def iteration_politique(self, escompte=1):
        """

        :return:
        """
        # on init une politique que au nord attention maime les cases qui ne doive pas boujet
        histori_mat_politique = [[['n'] * self.width for _ in range(self.height)]]
        while True:
            # calcule de l'utiliter pour chaque case
            mat_utiliter = self.get_utility(histori_mat_politique[-1], escompte)
            # Avec utiliter trouver on regarde la nouvelle politique
            histori_mat_politique.append(self.get_politique(mat_utiliter))
            # Si il n'y a pas de changement avec la derrnière politique on stop
            if histori_mat_politique[-1] == histori_mat_politique[-2]:
                break

        return histori_mat_politique[-1]

    def get_move(self, point):
        """

        :param point: point de recharche sous la forme [pos y, pos x]
        :return:
        """
        move_possible = dict()
        for wanted_move in self.move_proba:
            move_possible[wanted_move] = dict()
            move_possible[wanted_move]["r"] = 0
            for prob_move in self.move_proba[wanted_move]:
                try:
                    # Si c'est un obstacle on raise une erreur comme quoi le movement n'est pas possible
                    new_x = point[1] + self.move_pattern[prob_move][1]
                    new_y = point[0] + self.move_pattern[prob_move][0]
                    if self.mat[new_y][new_x].type == Case.OBSTACLE or new_y < 0 or new_x < 0:
                        raise IndexError
                    else:
                        move_possible[wanted_move][prob_move] = self.move_proba[wanted_move][prob_move]
                except IndexError:
                    # Si le movement n'est pas possible
                    # on incre la proba qui n'est pas possible dans le rebond
                    move_possible[wanted_move]["r"] += self.move_proba[wanted_move][prob_move]
                    move_possible[wanted_move][prob_move] = 0
        return move_possible


if __name__ == "__main__":

    # mat = [[Case(Case.VIDE, -0.04), Case(Case.FIN, 1)],
    #        [Case(Case.START, -0.04), Case(Case.DANGER, -1)]]
    #
    # b = Board(2, 2, None, None, mat)
    # print(np.array(b.iteration_politique()))

    b = Board()
    print("valeur")
    print(np.array(b.iteration_valeur()))
    print("politique")
    print(np.array(b.iteration_politique()))
