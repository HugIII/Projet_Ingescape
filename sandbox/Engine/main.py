#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  main.py
#  Engine
#  Created by BLAYES Hugo, BAFFOGNE Clara on 2024/09/28
#  Created by Ingenuity i/o on 2024/09/28
#  Description:
#   Ce programme est le bloc principal de notre jeu video,
#   il s'occupe de la partie graphique de notre projet en plus de centraliser la plupart de nos informations
#

import pygame
import sys
import ingescape as igs
import math
import time
import threading
import moviepy.editor

#variables########################################################################

#Map de secours
string_map = [["X","X","X","X","X","X","X","X","X","X"],
              ["X",".",".",".",".",".",".",".",".","X"],
              ["X",".",".",".",".",".",".",".",".","X"],
              ["X",".",".",".",".",".",".",".",".","X"],
              ["X",".",".",".",".",".",".",".",".","X"],
              ["X",".",".",".",".",".",".",".",".","X"],
              ["X",".",".",".",".",".",".",".",".","X"],
              ["X",".",".",".",".",".",".",".",".","X"],
              ["X",".",".",".",".",".",".",".",".","X"],
              ["X","X","X","X","X","X","X","X","X","X"]]

#dictionnaire comporant toutes les couleurs permettant de calculer à l'avance la couleurs des murs en fonction de la distance
#à laquelle nous nous situons du mur
dic_color = {}

#constante apparente à notre fenêtre
WINDOW_HEIGHT = 780.0
WINDOW_WIDTH = 1280.0
WINDOW_HEIGHT_INT = int(WINDOW_HEIGHT)
WINDOW_WIDTH_INT = int(WINDOW_WIDTH)
WINDOW_HEIGHT_DEMI = WINDOW_HEIGHT/2
WINDOW_WIDTH_DEMI = WINDOW_WIDTH/2
MAX_DEPTH = 800

#valeur par default de notre player
player_x = 430
player_y = 430
angle = 45

#variable d'affichage de la fenetre
fov = math.pi / 3
number_rays = 142
tile_size = 50
middle_rays = number_rays / 2
angle_step = float(fov / number_rays)
wall_width = WINDOW_WIDTH//number_rays

#booleen
debug_perspective = False
player_click_left = False
player_click_right = False
lock_ennemi_kill = True
lock_player_kill = True
wave_bool = False
cinematics_end = False

#variables liste
ennemies = []
ennemies_move = []
player_enn = []

wall_draw_list = []
ennemy_draw_list = []
player_enn_draw_list = []
ennemy_dict = {}
player_enn_dict = {}

#toutes les images du projet
monstre_link = ["./image/monstre1.png","./image/monstre2.png","./image/monstre3.png","./image/monstre4.png","./image/monstre5.png","./image/monstre6.png","./image/monstre7.png","./image/monstre8.png","./image/monstre9.png"]
player_link = "./image/other_player.png"
weapon_link = "./image/weapon.png"
weapon_link2 = "./image/weapon2.png"
sky_link = "./image/sky.png"
cursor_link = "./image/cursor.png"
scratch_link = ["./image/scratch1.png","./image/scratch2.png","./image/scratch3.png"]
screamer_link = "./image/screamer.png"
arrow_link = "./image/arrow.png"

#variables int
wave = 1
cursor_cooldown = 0
screamer_cooldown = 0
arrow_left = 0
vie = 100
kill_index = -1

#prechargement des images
image_monstre = []
for i in monstre_link:
    image_monstre.append(pygame.image.load(i))

image_weapon = pygame.image.load(weapon_link)
image_weapon2 = pygame.image.load(weapon_link2)
image_player = pygame.image.load(player_link)
image_sky = pygame.image.load(sky_link)
image_cursor = pygame.image.load(cursor_link)

image_scratch = []
for i in scratch_link:
    image_scratch.append(pygame.image.load(i))

image_screamer = pygame.image.load(screamer_link)
image_arrow = pygame.image.load(arrow_link)

#creation du screen
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

#fonctions###################################################################################

def send_service_rectangle_whiteboard(x,y,longeur,largeur,color,couleur_contour,contour):
    #dessine un rectangle sur notre fenetre pygame
    pygame.draw.rect(screen,color,(x,y,longeur,largeur))

def send_service_ellipse_whiteboard(x,y,longeur,largeur,color,couleur_contour,contour):
    #dessine une ellipse sur notre fenetre pygame
    pygame.draw.ellipse(screen,color,(x,y,longeur,largeur))

def send_service_image_whiteboard(image,x,y,height,width):
    #dessine une image sur notre fenetre pygame
    if width <= 0 or height <= 0:
        return
    image = pygame.transform.scale(image, (width, height))
    screen.blit(image, (x,y))

def send_service_text(x,y,text):
    #dessine un texte sur notre fenetre pygame
    text_color = (255, 0, 0)
    font = pygame.font.Font(None, 38)
    text = font.render(text, True, text_color)
    text_rect = text.get_rect(center=(x, y))
    screen.blit(text, text_rect)

def draw_arow():
    #dessine une fleche pointant vers l'ennemie le plus proche de la carte
    try:
        ennemies_proche = min(ennemies_move,key=lambda i: math.dist(i,(player_x,player_y)))
    except:
        try:
            ennemies_proche = min(ennemies,key=lambda i: math.dist(i,(player_x,player_y)))
        except:
            return
    angle_arrow = calculate_angle(player_x,player_y,ennemies_proche[0],ennemies_proche[1])
    rotated_arrow = pygame.transform.rotate(image_arrow,angle_arrow)
    send_service_image_whiteboard(rotated_arrow,WINDOW_WIDTH_DEMI-50,WINDOW_HEIGHT-200,100,100)

def calculate_angle(ax,ay,bx,by):
    #calcule l'angle de difference entre deux point et l'angle de notre personnage
    global angle
    delta_x = ax-bx
    delta_y = ay-by

    theta_ennemie = math.atan2(delta_y, delta_x)
    delta_ennemie = angle - theta_ennemie
    return math.degrees(delta_ennemie)-90 


def draw_map_render_2D():
    #permet de dessiner les differents mur de la carte de notre rendu 2D
    for i in range(len(string_map)):
        for j in range(len(string_map[i])):
            if string_map[i][j] == "X":
                send_service_rectangle_whiteboard(50.0*i,50.0*j,50.0,50.0,"black","grey",1.0)

def cast_rays_2D():
    #permet d'afficher les resultats du raycasting sur notre rendu 2D
    ray_angle = angle - fov/2
    for i in range(int(fov/angle_step)):
        for depth in range(MAX_DEPTH):
            target_x = player_x + depth * math.cos(ray_angle)
            target_y = player_y + depth * math.sin(ray_angle)

            grid_x = int(target_x / tile_size)
            grid_y = int(target_y / tile_size)

            if 0 <= grid_x < len(string_map[0]) and 0 <= grid_y < len(string_map):
                if string_map[grid_x][grid_y] == "X":
                    send_service_ellipse_whiteboard(target_x-10.0,target_y-10.0,20.0,20.0,"green","black",1.0)
                    break
        ray_angle += angle_step

def draw_player_render_2D():
    #dessine notre personnage sur le rendu 2D
    send_service_ellipse_whiteboard(player_x-10.0,player_y-10.0,20.0,20.0,"red","black",1.0)

def draw_ennemie_render_2D():
    #dessine les differents adversaires sur notre rendu 2D
    for i in ennemies:
        send_service_ellipse_whiteboard(i[0]-10.0,i[1]-10.0,20.0,20.0,"purple","black",1.0)
    for i in ennemies_move:
        send_service_ellipse_whiteboard(i[0]-10.0,i[1]-10.0,20.0,20.0,"blue","black",1.0)
    for i in player_enn:
        send_service_ellipse_whiteboard(i[0]-10.0,i[1]-10.0,20.0,20.0,"yellow","black",1.0)


def draw_sky_floor_3D():
    #dessine le ciel et le sol de notre rendu 3D
    send_service_image_whiteboard(image_sky,0,0,WINDOW_HEIGHT_INT-200,WINDOW_WIDTH_INT)
    send_service_rectangle_whiteboard(0.0,WINDOW_HEIGHT_DEMI,WINDOW_WIDTH,WINDOW_HEIGHT_DEMI,"#655e5c","grey",0.0)

def cast_rays_3D():
    #calcul du raycasting de notre rendu 3D
    global wall_draw_list
    global ennemy_draw_list
    global player_enn_draw_list
    global string_map
    global ennemies
    global player_enn
    global player_click_left
    global player_click_right
    global lock_ennemi_kill
    global lock_player_kill
    global ennemies_move
    global kill_index
    global cursor_cooldown
    global cinematics_end

    start_angle = angle - fov / 2
    wall_height_memory = []
    wall_draw_list = []
    ennemy_draw_list = []
    player_enn_draw_list = []
    degat = 0

    #copie de notre map en une map temporaire
    string_map_temp = []
    for i in range(len(string_map)):
        string_map_temp.append([])
        for j in range(len(string_map[i])):
            if string_map[i][j] == ".":
                string_map_temp[i].append([])
            else:
                string_map_temp[i].append(string_map[i][j])

    #ajout de chaque ennemie dans la case dans laquelle il se trouve sur la map temporaire
    if len(ennemies_move) == 0:
        for index,i in enumerate(ennemies):
            grid_x = int(i[0]/tile_size)
            grid_y = int(i[1]/tile_size)
            if not isinstance(string_map_temp[grid_x][grid_y],str):
                string_map_temp[grid_x][grid_y].append(str(index))
    else:
        for index,i in enumerate(ennemies_move):
            if index == kill_index:
                continue
            grid_x = int(i[0]/tile_size)
            grid_y = int(i[1]/tile_size)
            if not isinstance(string_map_temp[grid_x][grid_y],str):
                string_map_temp[grid_x][grid_y].append(str(index))

    #ajout de chaque autre joueur dans la case dans laquelle il se trouve sur le map temporaire
    for index,i in enumerate(player_enn):
        grid_x = int(i[0]/tile_size)
        grid_y = int(i[1]/tile_size)
        if not isinstance(string_map_temp[grid_x][grid_y],str):
            string_map_temp[grid_x][grid_y].append("P"+str(index))

    #calcul pour chaque ray
    #on commence les calculs à -50 et on depasse de 51 rays pour que les objets qui ne sont pas entierement dans notre champs de vision soit afficher correctement
    for ray in range(-50,number_rays+51):
        touch_player = False
        ray_angle = start_angle + ray * angle_step
        ray_angle_cos = math.cos(ray_angle)
        ray_angle_sin = math.sin(ray_angle)
        #pour chaque point jusqu'a notre max depth on calcule si le point touche un mur ou un ennemie
        for depth in range(0,MAX_DEPTH):
            target_x = player_x + depth * ray_angle_cos
            target_y = player_y + depth * ray_angle_sin
 
            grid_x = int(target_x / tile_size)
            grid_y = int(target_y / tile_size)

            #si le point sort de la carte pas besoin de le prendre en compte
            if 0 <= grid_x < len(string_map[0]) and 0 <= grid_y < len(string_map):
                #lorsque le point atteint le mur, nous le mettons dans la liste des objets a dessiner 
                try:
                    if string_map[grid_x][grid_y] == "X":
                        corrected_depth = depth/10 * math.cos(ray_angle-angle)
                        wall_height = WINDOW_HEIGHT / (corrected_depth + 0.0001)  
                        wall_height = 600 if wall_height > 600 else wall_height            
                        wall_draw_list.append((ray,wall_height))
                        break
                except:
                    print(grid_x,grid_y)

                #pour des raisons de performance on affiche pas les ennemies à une distance superieure a 300
                if depth > 300:
                    continue

                #cette condition permet de voir si dans la map temporaire la case du depth est vide
                if isinstance(string_map_temp[grid_x][grid_y],list):
                    list_case = string_map_temp[grid_x][grid_y]
                    #si nous avons des ennemies dans la liste sans prendre en compte 
                    for i in list_case:
                        touch_enn = False
                        if i[0] == "P":
                            continue
                        try:
                            if(len(ennemies_move)==0):
                                ennemies_position = ennemies[int(i)]
                            else:
                                ennemies_position = ennemies_move[int(i)]
                        except:
                            continue
                        if touch_enn == False and ennemies_position[0] - 2 < target_x < ennemies_position[0] + 2 and ennemies_position[1] - 2 < target_y < ennemies_position[1] + 2:
                            #calcul de la depth en fonction de la distance de l'adversaire
                            corrected_depth = depth/5 * math.cos(ray_angle-angle)
                            wall_height = WINDOW_HEIGHT / (corrected_depth + 0.0001)
                            wall_height = 600 if wall_height > 600 else wall_height
                            ennemy_draw_list.append((ray,wall_height,i,ennemies_position[0],ennemies_position[1],depth))
                            touch_enn = True

                            #cette partie permet de retirer de la vie au personnage en fonction du nombre d'adversaire a l'ecran et de leur distance
                            if depth >= 120:
                                d = 0.001
                            elif depth >= 50:
                                d = 0.005
                            else:
                                d = 0.01

                            #evite au personnage prendre des degats si nous sommes dans la cinematique
                            if cinematics_end:
                                degat += d / depth

                            #si l'adversaire est dans les rayons du milieu et que le player a attaque alors nous tuons l'adversaire
                            if middle_rays - 20 <= ray <= middle_rays + 20 and (player_click_left == True or (player_click_right == True and depth < 25)) and lock_ennemi_kill == True:
                                if ennemies_position[0] -10 < target_x < ennemies_position[0] + 10 and ennemies_position[1] - 10 < target_y < ennemies_position[1] +10:
                                    lock_ennemi_kill = False
                                    kill_index = i
                                    cursor_cooldown = 15
                                    igs.output_set_int("kill",int(i))

                #meme boucle que au dessus mais pour le mode multi
                if isinstance(string_map_temp[grid_x][grid_y],list):
                    list_case = string_map_temp[grid_x][grid_y]
                    for i in list_case:
                        if i[0] != "P":
                            continue
                        player_enn_position = player_enn[int(i[1:])]
                        if touch_player == False and player_enn_position[0] - 2 < target_x < player_enn_position[0] + 2 and player_enn_position[1] - 2 < target_y < player_enn_position[1] + 2:
                            corrected_depth = depth/5 * math.cos(ray_angle-angle)
                            wall_height = WINDOW_HEIGHT / (corrected_depth + 0.0001)
                            wall_height = 600 if wall_height > 600 else wall_height
                            player_enn_draw_list.append((ray,wall_height,i,depth))
                            touch_player = True

                            if middle_rays - 5 <= ray <= middle_rays + 5 and (player_click_left == True or (player_click_right == True and depth < 25)) and lock_player_kill == True:
                                if player_enn_position[0] - 10 < target_x < player_enn_position[0] + 10 and player_enn_position[1] - 10 < target_y < player_enn_position[1] + 10:
                                    lock_player_kill = False
                                    igs.output_set_int("kill_player",int(i[1:]))

    #on partage les degats recu au systeme
    if degat != 0:
        igs.output_set_double("degat",degat)
    player_click_left = False
    player_click_right = False

def draw_3D_world():
    #cette fonction permet de determiner la taille des differents objets a dessiner
    global cursor_cooldown
    global screamer_cooldown

    #dessin des murs
    for wall in wall_draw_list:
        send_service_rectangle_whiteboard(wall[0] * wall_width, (WINDOW_HEIGHT-wall[1])//2,wall_width,wall[1],dic_color[int(wall[1])],"black",1.0)

    #dessin des ennemies
    ennemy_draw_dict = {}
    ennemy_draw_origin_dict = {}
    ennemy_depth_dict = {}
    for enn in ennemy_draw_list:
        if enn[2] not in ennemy_draw_origin_dict.keys():
            ennemy_draw_origin_dict[enn[2]] = enn[0] 
            ennemy_depth_dict[enn[5]] = enn[2]
        ennemy_draw_dict[enn[2]] = (ennemy_draw_origin_dict[enn[2]],enn[1],enn[0],enn[3],enn[4],enn[2])

    #dessin des autres joueurs
    player_enn_draw_dict = {}
    player_enn_draw_origin_dict = {}
    player_depth_dict = {}
    for pla in player_enn_draw_list:
        if pla[2] not in player_enn_draw_origin_dict.keys():
            player_enn_draw_origin_dict[pla[2]] = pla[0] 
            player_depth_dict[pla[3]] = pla[2]
        player_enn_draw_dict[pla[2]] = (player_enn_draw_origin_dict[pla[2]],pla[1],pla[0])

    for i in reversed(ennemy_depth_dict.keys()):
        enn = ennemy_draw_dict[ennemy_depth_dict[i]]
        try:
            index = (ennemies[int(enn[5])][0]+ennemies[int(enn[5])][1])%len(image_monstre)
            send_service_image_whiteboard(image_monstre[index],enn[0] * wall_width,(WINDOW_HEIGHT-enn[1])//2,int((enn[2]-enn[0])*wall_width),int(enn[1]))
        except:
            pass

    for i in reversed(player_depth_dict.keys()):
        pla = player_enn_draw_dict[player_depth_dict[i]]
        send_service_image_whiteboard(image_player,pla[0] * wall_width,(WINDOW_HEIGHT-pla[1])//2,int((pla[2]-pla[0])*wall_width),int(pla[1]))

    #dessin du curseur
    if cursor_cooldown > 0:
        cursor_cooldown -= 1
        send_service_image_whiteboard(image_cursor,WINDOW_WIDTH_DEMI-15,WINDOW_HEIGHT_DEMI-15,30.0,30.0)
    else:
        send_service_ellipse_whiteboard(WINDOW_WIDTH_DEMI-2,WINDOW_HEIGHT_DEMI-2,5.0,5.0,"red","black",1.0)

    #dessin des armes
    send_service_image_whiteboard(image_weapon,WINDOW_WIDTH-400,WINDOW_HEIGHT-400,400,400)
    send_service_image_whiteboard(image_weapon2,0,WINDOW_HEIGHT-300,300,300)

    #dessin texte vie et arrow 
    send_service_text(50,50,"  life: "+str(vie))
    send_service_text(50,75,"  arrow: "+str(arrow_left))
    if wave_bool == True:
        send_service_text(50,100,"  wave: "+str(wave))
    
    #dessin screamer
    if screamer_cooldown > 0:
        send_service_image_whiteboard(image_screamer,0,0,WINDOW_HEIGHT_INT,WINDOW_WIDTH_INT)
        screamer_cooldown -= 1

    #dessin griffures 
    if vie < 75:
        send_service_image_whiteboard(image_scratch[0],800,0,300,300)
        if vie < 60:
            send_service_image_whiteboard(image_scratch[1],200,400,300,300)
            if vie < 30:
                send_service_image_whiteboard(image_scratch[2],0,0,WINDOW_HEIGHT_INT,WINDOW_WIDTH)

def update():
    #cette fonction permet de mettre a jour la fenetre pygame
    global debug_perspective
    if debug_perspective == True:
        draw_map_render_2D()
        draw_player_render_2D()
        cast_rays_2D()
        draw_ennemie_render_2D()
    else:
        draw_sky_floor_3D()
        cast_rays_3D()
        draw_3D_world()
        draw_arow()
    pygame.display.update()



def input_callback(iop_type, name, value_type, value, my_data):
    #cette fonction prend en compte les differents inputs de ingescape
    global player_x
    global player_y
    global debug_perspective
    global angle
    global player_click_left
    global player_click_right
    global ennemies
    global player_enn
    global string_map
    global player_x
    global player_y
    global lock_ennemi_kill
    global lock_player_kill
    global wave
    global wave_bool
    global arrow_left
    global ennemies_move
    global angle
    global screamer_cooldown
    global kill_index
    global vie

    if name=="Ennemies":
        if value == "[]":
            ennemies = []
            return
        ennemies = []
        for i in value.split("("):
            if i != "[" and i != "":
                t = i.strip()[:-2].split(",")
                ennemies.append((int(t[0]),int(t[1])))
        lock_ennemi_kill = True
        kill_index = -1
    if name=="other_player":
        if value == "[]":
            player_enn = []
            return
        player_enn = []
        for i in value.split("("):
            if i != "[" and i != "":
                t = i.strip()[:-2].split(",")
                player_enn.append((float(t[0]),float(t[1])))
        lock_player_kill = True
    elif name=="map":
        temp_list = []
        temp_sub_list = []
        for i in range(len(value)):
            if value[i] == "R":
                temp_list.append(temp_sub_list)
                temp_sub_list = []
            else:
                temp_sub_list.append(value[i])
        temp_list.append(temp_sub_list)
        string_map = temp_list
    elif name=="player_x":
        player_x = value
    elif name=="player_y":
        player_y = value
    elif name=="wave":
        wave_bool = True
        wave = value
    elif name=="arbalete_shot":
        player_click_left = True
    elif name=="sword_hit":
        player_click_right = True
    elif name=="arrow_left":
        arrow_left = value
    elif name=="Ennemies_move":
        if value == "[]":
            ennemies_move = []
            return
        ennemies_move = []
        for i in value.split("("):
            if i != "[" and i != "":
                t = i.strip()[:-2].split(",")
                ennemies_move.append((int(t[0]),int(t[1])))
        lock_ennemi_kill = True
    elif name == "screamer":
        screamer_cooldown += 20
    elif name == "angle":
        angle = value
    elif name == "vie" :
        vie = value
    # add code here if needed

def key_pressed_test():
    #cette fonction permet de dessiner le map debug
    global debug_perspective

    keys = pygame.key.get_pressed()  

    if keys[pygame.K_p]:
        debug_perspective = not debug_perspective

#code principal
if __name__=="__main__":
    if len(sys.argv) < 4:
        print("usage: python3 main.py agent_name network_device port")
        devices = igs.net_devices_list()
        print("Please restart with one of these devices as network_device argument:")
        for device in devices:
            print(f" {device}")
        exit(0)

    igs.agent_set_name(sys.argv[1])
    igs.definition_set_version("1.0")
    igs.log_set_console(True)
    igs.log_set_file(True, None)
    igs.set_command_line(sys.executable + " " + " ".join(sys.argv))

    igs.input_create("Ennemies",igs.STRING_T, None)
    igs.observe_input("Ennemies",input_callback,None)

    igs.input_create("other_player",igs.STRING_T, None)
    igs.observe_input("other_player",input_callback,None)

    igs.input_create("player_blood",igs.IMPULSION_T, None)
    igs.observe_input("player_blood",input_callback,None)

    igs.input_create("map",igs.STRING_T, None)
    igs.observe_input("map",input_callback,None)

    igs.input_create("player_x",igs.DOUBLE_T, None)
    igs.observe_input("player_x",input_callback,None)

    igs.input_create("player_y",igs.DOUBLE_T, None)
    igs.observe_input("player_y",input_callback,None)

    igs.input_create("wave",igs.INTEGER_T,None)
    igs.observe_input("wave",input_callback,None)

    igs.input_create("arbalete_shot",igs.IMPULSION_T,None)
    igs.observe_input("arbalete_shot",input_callback,None)

    igs.input_create("sword_hit",igs.IMPULSION_T,None)
    igs.observe_input("sword_hit",input_callback,None)

    igs.input_create("arrow_left",igs.INTEGER_T,None)
    igs.observe_input("arrow_left",input_callback,None)

    igs.input_create("vie",igs.INTEGER_T,None)
    igs.observe_input("vie",input_callback,None)

    igs.input_create("Ennemies_move",igs.STRING_T,None)
    igs.observe_input("Ennemies_move",input_callback,None)

    igs.input_create("screamer",igs.IMPULSION_T,None)
    igs.observe_input("screamer",input_callback,None)

    igs.input_create("angle",igs.DOUBLE_T,None)
    igs.observe_input("angle",input_callback,None)

    igs.output_create("kill", igs.INTEGER_T, None)
    igs.output_create("kill_player", igs.INTEGER_T, None)
    igs.output_create("degat", igs.DOUBLE_T, None)
    igs.output_create("music_trigger", igs.IMPULSION_T, None)

    igs.start_with_device(sys.argv[2], int(sys.argv[3]))
    
    #init pygame
    pygame.init()
    pygame.display.set_caption("DPPM")

    #init thread
    #on considere pygame plus important que les entrees en ingescape
    #donc on delegue la fonction ingescape dans un thread avec une priorite moindre 
    thread = threading.Thread(target=input)
    thread.start()

    #calcul du dictionnaire de couleur
    for i in range(int(WINDOW_HEIGHT)+1):
        if len(str(hex(int(i*255/600))[2:])) != 2: 
            dic_color[i] = "#"+("0"+str(hex(int(i*255/600))[2:]))*3
        else: 
            dic_color[i] = "#"+str(hex(int(i*255/600))[2:])*3

    running = True
    clock = pygame.time.Clock()
    time.sleep(3)

    #lancement de la cinematique
    if sys.argv[4] == "True":
        video = moviepy.editor.VideoFileClip("./cinematics/intro.mp4")
        video.preview()

    igs.output_set_impulsion("music_trigger")
    cinematics_end = True

    while running:
        pygame.event.pump()
        key_pressed_test()
        if wave > 5:
            running = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        update()
        clock.tick(144)

    igs.output_set_impulsion("music_trigger")

    #fin de la cinematique
    if wave > 5:
        video = moviepy.editor.VideoFileClip("./cinematics/Outro.mp4")
        video.preview()

    igs.stop()

    pygame.quit()

    exit()
