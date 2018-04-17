#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter.ttk import *
from Board import *
from math import *
import time


class BoardGui(object):
    """
    Class qui va soccuper de crée l'interface graphique est de soccuper de l'éxacution des différents algorithme
    """

    def __init__(self):

        self.board = None

        #                                        _________
        # ______________________________________/PARTIE UI\______________________________________

        font9 = "-family {Segoe UI} -size 9 -weight normal -slant roman -underline 0 -overstrike 0"

        # Liste des algos disponible a la selection
        algo = ["Iteration Politique", "Iteration Valeur"]

        self.top = Tk()
        self.select_set = IntVar()

        # Fenêtres principale
        self.top.geometry("923x771+500+167")
        self.top.title("IA Maze")
        self.top.configure(background="#d9d9d9")
        self.top.configure(highlightbackground="#d9d9d9")
        self.top.configure(highlightcolor="black")
        self.top.resizable(width=False, height=False)

        # Canvas pour le dessin
        self.canvas = Canvas(self.top)
        self.canvas.place(relx=0.01, rely=0.01, relheight=0.79, relwidth=0.98)
        self.canvas.configure(background="white")
        self.canvas.configure(borderwidth="2")
        self.canvas.configure(highlightbackground="#d9d9d9")
        self.canvas.configure(highlightcolor="black")
        self.canvas.configure(insertbackground="black")
        self.canvas.configure(relief=RIDGE)
        self.canvas.configure(selectbackground="#c4c4c4")
        self.canvas.configure(selectforeground="black")
        self.canvas.configure(width=906)
        self.canvas.bind("<Button-1>", lambda event: self.__click_event(event))
        self.canvas.bind("<Button-3>", lambda event: self.__click_event_del(event))

        # Input pour la largeur du plateau
        self.largeur = Spinbox(self.top, from_=1.0, to=100.0)
        self.largeur.place(relx=0.07, rely=0.86, relheight=0.03, relwidth=0.15)
        self.largeur.configure(activebackground="#f9f9f9")
        self.largeur.configure(background="white")
        self.largeur.configure(buttonbackground="#d9d9d9")
        self.largeur.configure(disabledforeground="#a3a3a3")
        self.largeur.configure(font=font9)
        self.largeur.configure(foreground="black")
        self.largeur.configure(from_="4")
        self.largeur.configure(highlightbackground="black")
        self.largeur.configure(highlightcolor="black")
        self.largeur.configure(insertbackground="black")
        self.largeur.configure(selectbackground="#c4c4c4")
        self.largeur.configure(selectforeground="black")
        self.largeur.configure(to="100.0")

        # Input pour la hauteur du plateau
        self.hauteur = Spinbox(self.top, from_=1.0, to=100.0)
        self.hauteur.place(relx=0.22, rely=0.86, relheight=0.03, relwidth=0.15)
        self.hauteur.configure(activebackground="#f9f9f9")
        self.hauteur.configure(background="white")
        self.hauteur.configure(buttonbackground="#d9d9d9")
        self.hauteur.configure(disabledforeground="#a3a3a3")
        self.hauteur.configure(font=font9)
        self.hauteur.configure(foreground="black")
        self.hauteur.configure(from_="3")
        self.hauteur.configure(highlightbackground="black")
        self.hauteur.configure(highlightcolor="black")
        self.hauteur.configure(insertbackground="black")
        self.hauteur.configure(selectbackground="#c4c4c4")
        self.hauteur.configure(selectforeground="black")
        self.hauteur.configure(to="100.0")

        # Input pour la selection de l'algo a éxécuter
        self.ia_select = Combobox(self.top, values=algo, state='readonly')
        self.ia_select.place(relx=0.74, rely=0.86, relheight=0.03, relwidth=0.24)
        self.ia_select.configure(takefocus="")
        self.ia_select.set(algo[0])

        # Botton pour générer le plateau
        self.generate = Button(self.top)
        self.generate.place(relx=0.07, rely=0.9, height=44, width=417)
        self.generate.configure(command=self.__new_board)
        self.generate.configure(text='''Generate''')
        self.generate.configure(width=417)

        # Boutton pour start l'algo
        self.start = Button(self.top)
        self.start.place(relx=0.74, rely=0.9, height=44, width=227)
        self.start.configure(command=self.__start)
        self.start.configure(text='''Start''')

        self.Label1 = Label(self.top)
        self.Label1.place(relx=0.07, rely=0.82, height=21, width=46)
        self.Label1.configure(text='''Largeur''')

        self.Label2 = Label(self.top)
        self.Label2.place(relx=0.22, rely=0.82, height=21, width=49)
        self.Label2.configure(text='''Hauteur''')

        self.Label3 = Label(self.top)
        self.Label3.place(relx=0.74, rely=0.82, height=21, width=64)
        self.Label3.configure(text='''Algo select''')

        self.Labelframe1 = LabelFrame(self.top)
        self.Labelframe1.place(relx=0.53, rely=0.80, relheight=0.2, relwidth=0.2)
        self.Labelframe1.configure(relief=GROOVE)
        self.Labelframe1.configure(text='''Placer élément''')
        self.Labelframe1.configure(width=180)

        # Radio pour choisire si on veut replacer le joueur dans le canvas
        self.joueur = Radiobutton(self.Labelframe1, variable=self.select_set, value=1)
        self.joueur.place(relx=0.06, rely=0.19, relheight=0.16, relwidth=0.35, y=-12, h=12)
        self.joueur.configure(text='''Joueur''')

        # Radio pour choisire si on veut replacer l'objectif dans le canvas
        self.objectif = Radiobutton(self.Labelframe1, variable=self.select_set, value=2)
        self.objectif.place(relx=0.06, rely=0.39, relheight=0.16, relwidth=0.39, y=-12, h=12)
        self.objectif.configure(text='''Objectif''')

        # Radio pour choisire si on veut rajouter ou enlever des obstacles
        self.obstacle = Radiobutton(self.Labelframe1, variable=self.select_set, value=3)
        self.obstacle.place(relx=0.06, rely=0.58, relheight=0.16, relwidth=0.39, y=-12, h=12)
        self.obstacle.configure(text='''Obstacle''')

        # Radio pour choisire si on veut rajouter ou enlever des danger
        self.danger = Radiobutton(self.Labelframe1, variable=self.select_set, value=4)
        self.danger.place(relx=0.06, rely=0.76, relheight=0.16, relwidth=0.44, y=-12, h=12)
        self.danger.configure(text='''Danger''')

        self.select_set.set(1)

        self.top.mainloop()

    def delete_shape_board(self, y, x):
        """

        :param y:
        :param x:
        :return:
        """
        if self.board.mat[y][x].shape is not None:
            self.canvas.delete(self.board.mat[y][x].shape)
            self.board.mat[y][x].shape = None

    def delete_shape_board_text(self, y, x):
        """

        :param y:
        :param x:
        :return:
        """
        if self.board.mat[y][x].text_shape is not None:
            self.canvas.delete(self.board.mat[y][x].text_shape)
            self.board.mat[y][x].text_shape = None

    def draw_rec(self, y, x, color):
        """

        :param y:
        :param x:
        :param color:
        :return:
        """
        self.delete_shape_board(y, x)
        can_largeur = self.canvas.winfo_width()
        can_hauteur = self.canvas.winfo_height()

        #  + 2 car il y a les bords
        colomne_space = can_largeur / self.board.width
        ligne_space = can_hauteur / self.board.height

        self.board.mat[y][x].shape = self.canvas.create_rectangle(colomne_space * x, ligne_space * y,
                                                                  (colomne_space * x) + colomne_space,
                                                                  (ligne_space * y) + ligne_space,
                                                                  fill=color)
        self.canvas.update_idletasks()

    def draw_char_at(self, y, x, char):
        """

        :param y:
        :param x:
        :param char
        :return:
        """
        self.delete_shape_board_text(y, x)
        can_largeur = self.canvas.winfo_width()
        can_hauteur = self.canvas.winfo_height()

        #  + 2 car il y a les bords
        colomne_space = can_largeur / self.board.width
        ligne_space = can_hauteur / self.board.height

        self.board.mat[y][x].text_shape = self.canvas.create_text(colomne_space * x + 20, ligne_space * y + 20,
                                                                  fill="darkblue",
                                                                  font="Times 20 italic bold",
                                                                  text=char)
        self.canvas.update_idletasks()

    def draw_player(self, y, x):
        """
        Fonction qui supprime le dessin du joueur est le re dessine a la position donnée
        :param y:
        :param x:
        :return:
        """
        self.draw_rec(y, x, "#0433FF")

    def draw_target(self, y, x):
        """
        Fonction qui supprime le dessin de l'objectif est le re dessine a la position donnée
        :param y:
        :param x:
        :return:
        """
        self.draw_rec(y, x, "#00F900")

    def draw_obstacle(self, y, x):
        """
        Fonction qui dessine un obstacle a la position donnée
        :param y:
        :param x:
        :return:
        """
        self.draw_rec(y, x, "#FF2700")

    def draw_danger(self, y, x):
        """

        :param y:
        :param x:
        :return:
        """
        self.draw_rec(y, x, "#FF9300")

    def __click_event_del(self, event):
        """
        Fonction click droit pour suprimer des element
        :param event:
        :return:
        """
        if self.board is None:
            return

        largeur = self.canvas.winfo_width()
        hauteur = self.canvas.winfo_height()

        colomne_space = largeur / self.board.width
        ligne_space = hauteur / self.board.height

        # on recupaire le position dans la grille
        grid_pos_x = floor(event.x / colomne_space)
        grid_pos_y = floor(event.y / ligne_space)
        try:
            if self.board.mat[grid_pos_y][grid_pos_x].type != Case.START \
                    and self.board.mat[grid_pos_y][grid_pos_x].type != Case.FIN:
                print("Delete")
                self.delete_shape_board(grid_pos_y, grid_pos_x)
                self.board.mat[grid_pos_y][grid_pos_x] = Case(Case.VIDE, self.board.recompence[Board.VIDE])
        except IndexError:
            print("delet index error")

    def __click_event(self, event):
        """
        Fonction appeler quand on click sur la canvas
        :param event:
        :return:
        """

        if self.board is None:
            return

        largeur = self.canvas.winfo_width()
        hauteur = self.canvas.winfo_height()

        colomne_space = largeur / self.board.width
        ligne_space = hauteur / self.board.height

        # on recupaire le position dans la grille
        grid_pos_x = floor(event.x / colomne_space)
        grid_pos_y = floor(event.y / ligne_space)
        try:
            # Si on a fait un click gauche et que on a choisi de placer un joueur
            if self.select_set.get() == 1:
                print("player")
                self.delete_shape_board(self.board.player_pos[0], self.board.player_pos[1])
                self.board.mat[self.board.player_pos[0]][self.board.player_pos[1]] = \
                    Case(Case.VIDE, self.board.recompence[Board.VIDE])

                self.delete_shape_board(grid_pos_y, grid_pos_x)
                self.board.mat[grid_pos_y][grid_pos_x] = Case(Case.START)
                self.board.player_pos[0] = grid_pos_y
                self.board.player_pos[1] = grid_pos_x
                self.draw_player(grid_pos_y, grid_pos_x)

            # Si on a fait un click gauche et que on a choisi de placer la cible
            elif self.select_set.get() == 2:
                print("target")
                self.delete_shape_board(self.board.target_pos[0], self.board.target_pos[1])
                self.board.mat[self.board.target_pos[0]][self.board.target_pos[1]] = \
                    Case(Case.VIDE, self.board.recompence[Board.VIDE])

                self.delete_shape_board(grid_pos_y, grid_pos_x)
                self.board.mat[grid_pos_y][grid_pos_x] = Case(Case.FIN, self.board.recompence[Board.FIN])
                self.board.target_pos[0] = grid_pos_y
                self.board.target_pos[1] = grid_pos_x
                self.draw_target(grid_pos_y, grid_pos_x)

            elif self.select_set.get() == 3:
                print("Obstacle")
                self.delete_shape_board(grid_pos_y, grid_pos_x)
                self.board.mat[grid_pos_y][grid_pos_x] = Case(Case.OBSTACLE)
                self.draw_obstacle(grid_pos_y, grid_pos_x)

            elif self.select_set.get() == 4:
                print("Danger")
                self.delete_shape_board(grid_pos_y, grid_pos_x)
                self.board.mat[grid_pos_y][grid_pos_x] = Case(Case.DANGER, self.board.recompence[Board.DANGER])
                self.draw_danger(grid_pos_y, grid_pos_x)
        except IndexError:
            print("Error index")

    #                                        __________
    # ______________________________________/ALGO DU TP\______________________________________

    def __simulation_iteration_valeur(self):
        """

        :return:
        """
        start = time.time()
        politique = self.board.iteration_valeur()
        end = time.time()
        print("Temps éxécution = ", end - start)
        for y in range(len(politique)):
            for x in range(len(politique[y])):
                self.draw_char_at(y, x, politique[y][x])

    def __simulation_iteration_politique(self):
        """

        :return:
        """
        start = time.time()
        politique = self.board.iteration_politique()
        end = time.time()
        print("Temps éxécution = ", end - start)
        for y in range(len(politique)):
            for x in range(len(politique[y])):
                self.draw_char_at(y, x, politique[y][x])

    # ______________________________________FIN ALGO DU TP______________________________________

    def __start(self):
        """
        Fonction appeler quand on apuiy sur start
        :return:
        """
        if self.board is None:
            self.__new_board()

        # on fait un dico event pour faciliter l'apelle au differente fonction
        func = {"Iteration Valeur": self.__simulation_iteration_valeur,
                "Iteration Politique": self.__simulation_iteration_politique}
        try:
            # on appele l'algo
            func[self.ia_select.get()]()
        except KeyError:
            print("Error exe algorithm")

    def __new_board(self):
        """
        Fonction qui cree un nouveaux plateau et le dessine
        :return:
        """
        # on supprime tout les dessine du canvas
        self.canvas.delete("all")
        try:
            hauteur = int(self.hauteur.get())
            largeur = int(self.largeur.get())
        except ValueError as e:
            print("Error get dimention: ", e)
            return

        can_largeur = self.canvas.winfo_width()
        can_hauteur = self.canvas.winfo_height()

        #  + 2 car il y a les bords
        colomne_space = can_largeur / largeur
        ligne_space = can_hauteur / hauteur

        # dessine les colomne
        for i in range(1, largeur):
            x = colomne_space * i
            self.canvas.create_line(x, 0, x, can_hauteur)

        # dessine les ligne
        for i in range(1, hauteur):
            y = ligne_space * i
            self.canvas.create_line(0, y, can_largeur, y)

        self.board = Board(height=hauteur, width=largeur)

        for y in range(hauteur):
            for x in range(largeur):
                case = self.board.mat[y][x]
                if case.type == Case.OBSTACLE:
                    self.draw_obstacle(y, x)
                elif case.type == Case.DANGER:
                    self.draw_danger(y, x)
                elif case.type == Case.START:
                    self.draw_player(y, x)
                elif case.type == Case.FIN:
                    self.draw_target(y, x)


if __name__ == "__main__":
    n = BoardGui()
