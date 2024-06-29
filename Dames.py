from tkinter import *

# ------------------------------------------------- Paramètres importants ----------------------------------------------
colonnes = 8
lignes = 8
carre_taille = 70
pion_diam = 60
decalage_pion = 10
couleur = 'white'
largeur_fenetre = lignes * carre_taille
hauteur_fenetre = colonnes * carre_taille
pions_id = []
carres_id = []
case_select = 0
pion_select = 0
dico_des_prises_pos = {}
pion_precedent = 0
"""liste = [2,1, 0, 3]
print(liste)
liste = sorted(liste)
liste.reverse()
print(liste)"""


# -------------------------------------------- Création du damier (et des pions) ---------------------------------------
class Damier:

    def __init__(self, caneva, nbr_lignes, nbr_colonnes):
        self.lignes = nbr_lignes
        self.nbr_colonnes = nbr_colonnes
        self.caneva = caneva

    def creation(self):

        global couleur
        for i in range(lignes):
            for j in range(colonnes):
                c = cnv.create_rectangle(j * carre_taille, i * carre_taille, j * carre_taille + carre_taille,
                                         i * carre_taille + carre_taille, fill=couleur, width=2)
                carres_id.append(c)
                if cnv.itemcget(c, 'fill') == 'black' and (i < 3 or i > 4):
                    if i < 3:
                        pion_couleur = '#ED7D31'
                    else:
                        pion_couleur = 'white'
                    p = cnv.create_oval(j * carre_taille + decalage_pion, i * carre_taille + decalage_pion,
                                        j * carre_taille + pion_diam, i * carre_taille + pion_diam, fill=pion_couleur,
                                        outline='black')
                    if pion_couleur == '#ED7D31':
                        cnv.itemconfig(p, tags=('Marron', 'Normal'))
                    else:
                        cnv.itemconfig(p, tags=('Blanc', 'Normal'))
                    pions_id.append(p)
                if j != 7:
                    if couleur == 'white':
                        couleur = 'black'
                    else:
                        couleur = 'white'


# ---------------------------------------------- Changement de tour ----------------------------------------------------
def changement_de_tour():
    if Tour.get() == 1:
        Tour.set(2)
        Tour_de_jeu.set("Tour des Marrons")
    else:
        Tour.set(1)
        Tour_de_jeu.set("Tour des Blancs")


# ------------------------------------- Reinitialisation ---------------------------------------------------------------
def reinitialisation(case):
    cnv.itemconfig(case, fill='black')


# ---------------------------------- Trouver coordonnes de la case où se trouve un pion----------------------------------
def find_case(pion):
    global decalage_pion, carre_taille, pion_diam
    case_pion_coords = cnv.coords(pion)
    case_pion_coords[0] -= decalage_pion
    case_pion_coords[1] -= decalage_pion
    case_pion_coords[2] -= pion_diam - carre_taille
    case_pion_coords[3] -= pion_diam - carre_taille
    return case_pion_coords


# --------------------------------------------- Gagnant ----------------------------------------------------------------
def gagnant():
    global pions_id
    nbr_pions = [0, 0]
    for pion in pions_id:
        if cnv.gettags(pion)[0] == 'Blanc':
            nbr_pions[0] += 1
        if cnv.gettags(pion)[0] == 'Marron':
            nbr_pions[1] += 1
    if nbr_pions[0] == 0:
        Gagnant.set("Gagnant:\n" + "Marrons")
    elif nbr_pions[1] == 0:
        Gagnant.set("Gagnant:\n" + "Blancs")


# ----------------------------------------------- Dame_mouvement -------------------------------------------------------

def dame_mouvement(case_select_coords, pion_case_coord):
    diago_elems = []
    x_liste = sorted([pion_case_coord[0], case_select_coords[0]])
    y_liste = sorted([pion_case_coord[1], case_select_coords[1]])
    for elem in carres_id:
        elem_coords = cnv.coords(elem)
        if abs(pion_case_coord[0] - elem_coords[0]) == abs(pion_case_coord[1] - elem_coords[1]):
            if x_liste[0] <= elem_coords[0] <= x_liste[1] and (y_liste[0] <= elem_coords[1] <= y_liste[1]):
                diago_elems.append(elem)
    if len(diago_elems) > 1:
        for i in range(len(diago_elems) - 1):
            for j in range(i + 1, len(diago_elems)):
                if abs(cnv.coords(diago_elems[i])[0] - pion_case_coord[0]) > abs(cnv.coords(
                        diago_elems[j])[0] - pion_case_coord[0]):
                    c = diago_elems[i]
                    diago_elems[i] = diago_elems[j]
                    diago_elems[j] = c
    return diago_elems


# ----------------------------------------- Vérification de prise obligatoire ------------------------------------------
def si_prise_obligatoire(*args):
    global decalage_pion, pion_diam, carre_taille, carres_id, pions_id, cnv, Tour, dico_des_prises_pos
    dico_des_prises_pos.clear()
    for pion in pions_id:
        if (cnv.gettags(pion)[0] == 'Marron' and Tour.get() == 2) or (
                cnv.gettags(pion)[0] == 'Blanc' and Tour.get() == 1):
            case_pion_coords = find_case(pion)
            case_pion = cnv.find_closest(case_pion_coords[0] + 1, case_pion_coords[1] + 1)
            cases_possible = []
            for case in carres_id:
                case_coords = cnv.coords(case)
                if (prise(case_pion_coords, case, pion, "test", cnv.gettags(pion)[1]) and
                        cnv.itemcget(case, 'fill') != 'white' and len(
                            cnv.find_overlapping(case_coords[0] + 1,
                                                 case_coords[1] + 1, case_coords[2] - 1,
                                                 case_coords[3] - 1)) == 1):
                    cases_possible.append(case)
                    cnv.itemconfig(case_pion[0], fill='green')
                    cnv.after(1000, reinitialisation, case_pion[0])
            if len(cases_possible) > 0:
                dico_des_prises_pos[pion] = cases_possible
                """if cnv.gettags(pion)[1] == 'Dame':
                    dame_case_pos = []
                    for carre in cases_possible:
                        carre_coords = cnv.coords(carre)
                        if (prise(case_pion_coords, carre, pion, "test", cnv.gettags(pion)[1]) and
                                cnv.itemcget(carre, 'fill') != 'white' and len(
                                    cnv.find_overlapping(carre_coords[0] + 1,
                                                         carre_coords[1] + 1, carre_coords[2] - 1,
                                                         carre_coords[3] - 1)) == 1):
                            dame_case_pos.append(carre)
                    if len(dame_case_pos) > 0:
                        dico_des_prises_pos[pion] = dame_case_pos"""



# return dico_des_prises_pos


# ----------------------------------------- Vérification d'une prise ---------------------------------------------------
def prise(pion_case_coord, case, pion, mode, type):
    global pion_select, case_select, carre_taille
    case_select_coords = cnv.coords(case)
    inter_case_coords = []
    if type != 'Dame':
        if abs(pion_case_coord[0] - case_select_coords[0]) == 2 * carre_taille and abs(
                pion_case_coord[1] - case_select_coords[1]) == 2 * carre_taille:
            if case_select_coords[1] > pion_case_coord[1]:
                if case_select_coords[0] > pion_case_coord[0]:

                    inter_case_coords.append(pion_case_coord[2])
                    inter_case_coords.append(pion_case_coord[3])
                    inter_case_coords.append(case_select_coords[0])
                    inter_case_coords.append(case_select_coords[1])
                else:

                    inter_case_coords.append(pion_case_coord[0] - carre_taille)
                    inter_case_coords.append(pion_case_coord[1] + carre_taille)
                    inter_case_coords.append(pion_case_coord[0])
                    inter_case_coords.append(case_select_coords[1])
            else:
                if case_select_coords[0] < pion_case_coord[0]:

                    inter_case_coords.append(case_select_coords[2])
                    inter_case_coords.append(case_select_coords[3])
                    inter_case_coords.append(pion_case_coord[0])
                    inter_case_coords.append(pion_case_coord[1])
                else:

                    inter_case_coords.append(pion_case_coord[0] + carre_taille)
                    inter_case_coords.append(pion_case_coord[1] - carre_taille)
                    inter_case_coords.append(case_select_coords[0])
                    inter_case_coords.append(pion_case_coord[1])
        if len(inter_case_coords) > 0:
            # inter = cnv.find_closest(inter_case_coords[2] - 3, inter_case_coords[3] - 3)[0]
            contenu_inter = cnv.find_overlapping(inter_case_coords[0] + 1, inter_case_coords[1] + 1,
                                                 inter_case_coords[2] - 1, inter_case_coords[3] - 1)
            if len(contenu_inter) > 1 and cnv.gettags(contenu_inter[1])[0] != cnv.gettags(pion)[0]:
                if mode != "test":
                    pions_id.remove(contenu_inter[1])
                    cnv.delete(contenu_inter[1])
                return True
            else:
                return False
        else:
            return False
    else:
        diago_elems = dame_mouvement(case_select_coords, pion_case_coord)
        verifie = True
        for i in range(1, len(diago_elems)):
            elem_coords = cnv.coords(diago_elems[i])
            ctn = cnv.find_overlapping(elem_coords[0] + 1, elem_coords[1] + 1, elem_coords[2] - 1, elem_coords[3] - 1)
            if len(ctn) > 1 and cnv.gettags(ctn[1])[0] == cnv.gettags(pion)[0]:
                verifie = False
                break
            if i + 1 != len(diago_elems):
                case_suivante = cnv.coords(diago_elems[i + 1])
                case_actu = cnv.coords(diago_elems[i])
                ctn_suivante = cnv.find_overlapping(case_suivante[0] + 1, case_suivante[1] + 1,
                                                    case_suivante[2] - 1, case_suivante[3] - 1)
                ctn_actu = cnv.find_overlapping(case_actu[0] + 1, case_actu[1] + 1,
                                                case_actu[2] - 1, case_actu[3] - 1)
                if len(ctn_actu) > 1 and len(ctn_suivante) > 1:
                    verifie = False
                    break
        if verifie:
            liste_prises = []
            for i in range(1, len(diago_elems) - 1):
                pris = False
                inter_case_coords = cnv.coords(diago_elems[i])
                case_suivante = cnv.coords(diago_elems[i + 1])
                contenu_suivante = cnv.find_overlapping(case_suivante[0] + 1, case_suivante[1] + 1,
                                                        case_suivante[2] - 1, case_suivante[3] - 1)
                contenu_inter = cnv.find_overlapping(inter_case_coords[0] + 1, inter_case_coords[1] + 1,
                                                     inter_case_coords[2] - 1, inter_case_coords[3] - 1)
                if len(contenu_inter) > 1 and cnv.gettags(contenu_inter[1])[0] != cnv.gettags(pion)[0] and len(
                        contenu_suivante) == 1:
                    if mode != "test":
                        pions_id.remove(contenu_inter[1])
                        cnv.delete(contenu_inter[1])
                    pris = True
                liste_prises.append(pris)
            if True in liste_prises:
                return True
            else:
                return False
        else:
            # print("Non, dame ne saute pas son ami")
            return False


# ----------------------------------------- Vérification d'une case de deplacement -------------------------------------
def verification(case):
    global case_select, carres_id, pions_id
    case_coords = cnv.coords(case)
    if cnv.itemcget(case, 'fill') != 'white' and len(cnv.find_overlapping(case_coords[0] + 1,
                                                                          case_coords[1] + 1, case_coords[2] - 1,
                                                                          case_coords[3] - 1)) == 1:
        case_pion_coords = find_case(pion_select)
        # case_pion-coords = coordonnes de la case où se trouve le pion
        if cnv.gettags(pion_select) == ('Marron', 'Normal'):
            if case_coords[3] == case_pion_coords[3] + carre_taille and abs(
                    case_pion_coords[0] - case_coords[0]) == carre_taille:
                return True
            elif prise(case_pion_coords, case, pion_select, "jouer", 'Normal'):  # si le pion saute des cases on verifie
                # s'il y a prise
                return True
        if cnv.gettags(pion_select) == ('Blanc', 'Normal'):
            if case_coords[3] == case_pion_coords[3] - carre_taille and abs(
                    case_pion_coords[0] - case_coords[0]) == carre_taille:
                return True
            elif prise(case_pion_coords, case, pion_select, "jouer", 'Normal'):
                return True
        if cnv.gettags(pion_select)[1] == 'Dame':
            print("Dame selctionne")
            if abs(case_pion_coords[0] - case_coords[0]) == abs(case_pion_coords[1] - case_coords[1]):
                if prise(case_pion_coords, case, pion_select, "jouer", 'Dame'):
                    return True
                else:
                    diago_elems = dame_mouvement(case_coords, case_pion_coords)
                    verifie = True
                    for i in range(1, len(diago_elems)):
                        elem_coords = cnv.coords(diago_elems[i])
                        ctn = cnv.find_overlapping(elem_coords[0] + 1, elem_coords[1] + 1, elem_coords[2] - 1,
                                                   elem_coords[3] - 1)
                        if len(ctn) > 1 and cnv.gettags(ctn[1])[0] == cnv.gettags(pion_select)[0]:
                            verifie = False
                            break
                        if i + 1 != len(diago_elems):
                            case_suivante = cnv.coords(diago_elems[i + 1])
                            case_actu = cnv.coords(diago_elems[i])
                            ctn_suivante = cnv.find_overlapping(case_suivante[0] + 1, case_suivante[1] + 1,
                                                                case_suivante[2] - 1, case_suivante[3] - 1)
                            ctn_actu = cnv.find_overlapping(case_actu[0] + 1, case_actu[1] + 1,
                                                            case_actu[2] - 1, case_actu[3] - 1)
                            if len(ctn_actu) > 1 and len(ctn_suivante) > 1:
                                verifie = False
                                break
                    if verifie:
                        return True
                    else:
                        return False
            else:
                return False
    else:
        return False


# ------------------------------------------------ Deplacement du pion -------------------------------------------------
def deplace():
    global pion_select, case_select, cnv, decalage_pion, carre_taille, pion_diam, Tour, dico_des_prises_pos, pions_id, pion_precedent
    i = 0
    if pion_select != 0 and case_select != 0:
        nbre_pions = len(pions_id)
        if verification(case_select):  # verifie si le deplacement est possible
            case_coords = cnv.coords(case_select)
            cnv.coords(pion_select, case_coords[0] + decalage_pion, case_coords[1] + decalage_pion,
                       case_coords[2] - carre_taille + pion_diam, case_coords[3] - carre_taille + pion_diam)
            cnv.tag_raise(pion_select, case_select)
            pion_case_coords = find_case(pion_select)
            if pion_case_coords[1] == 0 and cnv.gettags(pion_select) == ('Blanc', 'Normal'):
                cnv.itemconfig(pion_select, tags=(cnv.gettags(pion_select)[0], 'Dame'), fill='yellow')
            if pion_case_coords[1] == (lignes - 1) * carre_taille and cnv.gettags(pion_select) == ('Marron', 'Normal'):
                cnv.itemconfig(pion_select, tags=(cnv.gettags(pion_select)[0], 'Dame'), fill='#66B2F0')
            changement_de_tour()
            if len(pions_id) != nbre_pions:
                i = 1
                gagnant()  # verifie la fin du jeu
                changement_de_tour()
                if len(dico_des_prises_pos) > 0:
                    try:
                        for elem in dico_des_prises_pos:
                            if elem != pion_select:
                                dico_des_prises_pos.pop(elem)
                    except:
                        pass
                if pion_select not in dico_des_prises_pos:
                    # print("Apres retrait, on a : ", dico_des_prises_pos)
                    pion_select = 0
                    changement_de_tour()

    if i == 0:
        pion_select = 0


# ------------------------------------------------- Liaison au clic ----------------------------------------------------

def clic(event):
    global carres_id, pions_id, case_select, pion_select, Tour, dico_des_prises_pos
    point_clic_x = event.x
    point_clic_y = event.y
    pos_clic = cnv.find_closest(point_clic_x, point_clic_y)
    if pos_clic[0] in carres_id:
        print("Case selectionnee ", pos_clic[0])
        case_select = pos_clic[0]
        if len(dico_des_prises_pos) > 0:
            if pion_select not in dico_des_prises_pos:
                pion_select = 0
            else:
                if case_select not in dico_des_prises_pos[pion_select]:
                    pion_select = 0
        deplace()
    if pos_clic[0] in pions_id:
        if (cnv.gettags(pos_clic[0])[0] == 'Marron' and Tour.get() == 2) or (
                cnv.gettags(pos_clic[0])[0] == 'Blanc' and Tour.get() == 1):
            print("Pion selectionne ", pos_clic[0])
            pion_select = pos_clic[0]


root = Tk()
Tour = IntVar()
Tour.set(1)
Tour.trace("w", si_prise_obligatoire)  # Les blancs sont les premiers joueurs
Tour_de_jeu = StringVar()
Tour_de_jeu.set("Tour des Blancs")
Gagnant = StringVar()
root.geometry(str(largeur_fenetre + 300) + "x" + str(hauteur_fenetre) + "+300+50")
root.resizable(False, False)
root.title("Dames")
Label(root, textvariable=Tour_de_jeu, font=('Arial Black', 10)).place(x=(largeur_fenetre + 165),
                                                                      y=(hauteur_fenetre // 2) - 100)
Label(root, textvariable=Gagnant, font=('Arial Black', 20)).place(x=(largeur_fenetre + 155), y=hauteur_fenetre // 2)

cnv = Canvas(root, width=largeur_fenetre, height=hauteur_fenetre)
cnv.pack()

tablier = Damier(cnv, lignes, colonnes)
tablier.creation()

root.after(500, si_prise_obligatoire)
root.bind('<Button-1>', clic)
root.mainloop()
