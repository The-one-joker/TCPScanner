#######################################################
# TP1 - TCP scanner
# Author: Romane Lesueur, Lucas Aubriet
#######################################################

import scanner
import iptraitment

choix = 0

while (choix != 4 ) : 
    print("""
          -------------------------------------------------------------------------------------
          -                      --- Welcome to the TCP scanner :) ---                        -
          -                                                                                   -
          -    Choisissez une option :                                                        -
          -              1- Scanner une cyble sur le port 1 à 1024                            -
          -              2- Scanner une cyble sur une plage port définie                      -
          -              3- Scanner une cyble sur un port définie                             -
          -              4- Fermer le programme                                               - 
          -                                                                                   -
          -------------------------------------------------------------------------------------
        """)

    choix = int(input("Entrez votre choix (1,2,3,4) : "))

    if 1 <= choix <= 3 :
        target = input("Saisissez adresse IP cible : ")
        if not iptraitment:
            print("IP incorrecte")
            break
    
    match choix :
        case 1:
            scanner.scanner(target)
        case 2 :
            start_port = int(input("Saisissez le premier port à scanner : "))
            end_port = int(input("Saisissez le dernier port à scanner : "))
            if start_port > end_port or not (1 <= start_port <= 65535) or not (1 <= end_port <= 65535):
                print("Ports non valides")
                break
            scanner.scanner(target, start_port, end_port)
        case 3 : 
            port = int(input("Saisissez le port à scanner : "))
            if not (1 <= port <= 65535):
                print("Port non valide")
                break
            scanner.scanner(target, port, port)
        case 4 : 
            print("Biz 😘")
            break
        case _ : 
            print("Choix non valide")
            break