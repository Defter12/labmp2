import math
import pygame
import sys

# Constantes

BLEUCLAIR = (127, 191, 255)
ROUGE = (255, 0, 0)
NOIR = (0, 0, 0)
COULEUR = (255, 0, 0)
# Paramètres
A = 2
B = 5
C = 20
COU = 8.9876*(10**9)
t = 50



mobile_est_present = False
mobile_x = 200
mobile_y = 200
mobile_vx = 0
mobile_vy = 0
mobile_charge = 0
dimensions_fenetre = (1600, 900)  # en pixels
images_par_seconde = 25
objets = []
objet_present = False
energie_cinetique = 0
energie_potentielle = 0
 #Fonctions 

def ajouter_objets(x, y, q):
    objet = (x, y, q)
    objets.append(objet)

def dessiner_objet():

  for objet in objets:
        if objet[2] > 0:
            pygame.draw.circle(fenetre, ROUGE, (objet[0], objet[1]), 10)
        else:
            pygame.draw.circle(fenetre, NOIR, (objet[0], objet[1]), 10)

# nous noterons ce pour champ éléctrique 
def dessiner_mobile():
    if mobile_charge > 0:
        pygame.draw.circle(fenetre, ROUGE, (mobile_x, mobile_y), 10, 4)
    else:
        pygame.draw.circle(fenetre, NOIR, (mobile_x, mobile_y), 10, 4)

def gerer_bouton(evenement):
    if evenement.button == 1:
        ajouter_objets(evenement.pos[0], evenement.pos[1] ,10**-7)
    elif evenement.button == 2:
       retirer_objet(evenement.pos[0], evenement.pos[1])
    elif evenement.button == 3:
       ajouter_objets(evenement.pos[0], evenement.pos[1], -10**-7)  
       
    return True



def retirer_objet(x, y):
     for objet in objets:
        if math.sqrt(((x-objet[0])**2)+((y-objet[1])**2)) <= 10:
            objets.remove(objet)

 
def calculer_champ(x, y):
    ce_x = 0
    ce_y = 0 
 
    for objet in objets:
        if math.sqrt(((x-objet[0])**2)+((y-objet[1])**2)) < 20:
            return None
        alpha = math.atan2(y - objet[1], x - objet[0])
        if objet[2]>0:
            ce_x += (COU*abs(objet[2]))/(math.sqrt(((x-objet[0])**2)+((y-objet[1])**2))**2)*math.cos(alpha)
            ce_y += (COU*abs(objet[2]))/(math.sqrt(((x-objet[0])**2)+((y-objet[1])**2))**2)*math.sin(alpha)
        else:
            ce_x += (COU*abs(objet[2]))/(math.sqrt(((x-objet[0])**2)+((y-objet[1])**2))**2)*math.cos(alpha)*-1
            ce_y += (COU*abs(objet[2]))/(math.sqrt(((x-objet[0])**2)+((y-objet[1])**2))**2)*math.sin(alpha)*-1
    
    return (ce_x, ce_y)

def mettre_a_jour_mobile(t):
        global mobile_x, mobile_y, mobile_vx, mobile_vy
        if mobile_est_present == True and calculer_champ(objets[0], objets[1]) != None:
            force_x = calculer_champ(objets[0], None) * mobile_charge
            force_y = calculer_champ(None, objets[1]) * mobile_charge
            acceleration_x = force_x/10**-10
            acceleration_y = force_y/10**-10
            force_g_x = 10**-10 * acceleration_x
            force_g_y = 10**-10 * acceleration_y
            mobile_x, mobile_y, mobile_vx, mobile_vy = 0
            return((force_g_x, force_g_y), (force_x, force_y))


# def calculer_energie_potentielle(x, y):
    
            

     
# nous noterons cep le vecteur e'


pygame.init()

fenetre = pygame.display.set_mode(dimensions_fenetre)
pygame.display.set_caption("Programme 1")

horloge = pygame.time.Clock()
couleur_fond = BLEUCLAIR

# Dessin


fenetre.fill(couleur_fond)

while True:
    
#    energie_cinetique += 1/2
    for evenement in pygame.event.get():
        
        if evenement.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if evenement.type == pygame.MOUSEBUTTONDOWN:
            gerer_bouton(evenement)
            dessiner_objet()  
        
        if evenement.type == pygame.KEYDOWN:
            if evenement.key == pygame.K_p:
                if mobile_est_present == False:

                    fenetre.fill(couleur_fond)
                    mobile_charge=10**-7
                    x_souris, y_souris = pygame.mouse.get_pos()
                    mobile_x = x_souris
                    mobile_y = y_souris
                    dessiner_mobile()
         
                  
            elif evenement.key == pygame.K_n:
                if mobile_est_present == False:
                    fenetre.fill(couleur_fond)
                    mobile_charge=-10**-7
                    x_souris, y_souris = pygame.mouse.get_pos()
                    mobile_x = x_souris
                    mobile_y = y_souris   
                    dessiner_mobile()
                    if evenement.key == pygame.K_d:
                        for objet in objets:
                            objets.remove(objet)
        dessiner_objet()    
                       



    temps_maintenant = pygame.time.get_ticks()
    t += temps_maintenant - 1
    t = horloge.tick(images_par_seconde)/1000
    # t*=1000
    mettre_a_jour_mobile(t)
    pygame.display.flip()




