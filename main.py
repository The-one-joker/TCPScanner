#!/usr/bin/env python3
#######################################################
# TP1 - TCP scanner
# Author: Romane Lesueur, Lucas Aubriet
# Date: 01-10-2025
#######################################################

import socket
import signal
import sys
import concurrent.futures
import threading


# ========== CONFIGURATION ==========
DEFAULT_PORT_RANGE = (1, 1024) # Scan des well-known ports (les ports "connus")
DEFAULT_TIMEOUT = 1.0 # Temps de timeout pour chaque tentative de connexion
MAX_WORKERS = 50 # Nombre maximum de threads exécuités simultanément


# ========== VARIABLES GLOBALES ==========
openned_ports = [] # Liste des ports ouverts trouvés
lock = threading.Lock() # Verrou pour la gestion thread-safe des accès à openned_ports (cela permet d'éviter que plusieurs threads modifient la liste en même temps)


# ========== FONCTIONS UTILITAIRES ==========
def validate_arguments():
    """Valide les arguments passés en ligne de commande et indique à l'utilisateur le format attendu."""
    if len(sys.argv) != 2: # sys.argv est une liste contenant les arguments passés en ligne de commande. Le premier [0] est le nom du fichier et le deuxième [1] est l'argument attendu
        print("Usage: python main.py <adresse_ip>")
        print("Exemple: python main.py 192.168.1.1")
        sys.exit(2) # Terminer le programme avec un code d'erreur 2 (erreur d'usage)
    return sys.argv[1]


def signal_handler(sig, frame):
    """Gestionnaire pour l'interruption Ctrl+C."""
    print("\n\nScan interrompu par l'utilisateur (Ctrl+C).")
    print("Ports ouverts trouvés jusqu'à présent :", sorted(openned_ports))
    sys.exit(0) # Terminer le programme proprement avec un code 0 (sans erreur)


def port_scanner(target, port):
    """
    Teste si un port TCP spécifique est ouvert sur la cible.
    
    Args:
        target (str): L'adresse IP ou nom d'hôte à scanner
        port (int): Le numéro de port à scanner
        
    Returns:
        int or None: Le numéro du port s'il est ouvert, None sinon
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        """Création d'un socket TCP à l'aide de socket.socket() instancié via un Context Manager. Ce denier permet une fermeture automatique du socket à la fin du bloc with.
        AF_INET : famille d'adresses --> IPv4
        SOCK_STREAM : type de socket --> TCP
        """
        s.settimeout(DEFAULT_TIMEOUT)
        try:
            result = s.connect_ex((target, port)) # Tentative de connexion au port spécifié
            if result == 0:  # 0 = connexion réussie
                with lock:  # Protection de la section critique (ajout du port ouvert dans la liste)
                    openned_ports.append(port)
                print(f"Port {port} ouvert")
                return port # Si le port est ouvert, on retourne son numéro
            return None # Si le port est fermé, on retourne None
        except Exception:
            # Port fermé ou erreur de réseau
            return None 


def scan_ports(target, start_port=DEFAULT_PORT_RANGE[0], end_port=DEFAULT_PORT_RANGE[1]):
    """
    Lance le scan des ports en utilisant le multithreading.
    
    Args:
        target (str): L'adresse IP ou nom d'hôte à scanner
        start_port (int): Port de début du scan
        end_port (int): Port de fin du scan
    """
    print(f"Démarrage du scan TCP sur {target}...")
    print(f"Scan des ports {start_port}-{end_port-1}")
    print("Appuyez sur Ctrl+C pour interrompre le scan\n")

    # Utilisation d'un context manager pour une gestion propre des threads
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        """concurrent.futures.ThreadPoolExecutor : Permet de gérer un pool de threads pour exécuter des appels de manière asynchrone.
        Ici on créer donc un groupe de 50 threads qui vont chacun tester un port différent en parallèle."""
        
        # Soumettre tous les ports pour scan
        future_to_port = {
            executor.submit(port_scanner, target, port): port 
            for port in range(start_port, end_port)
        }
        """Ici on créer un dictonnaire en compréhension.
        La clé est executor.submit(port_scanner, target, port) --> soumet la fonction port_scanner avec les arguments target et port au pool de threads et retourne un objet Future représentant l'exécution de cette tâche.
        Cet création de tâche est faite pour chaque port dans la plage spécifiée (de start_port à end_port-1).
        Notre dictionnaire ressemble à ceci :
            {Future_du_port_1: 1,
            Future_du_port_2: 2, 
            Future_du_port_80: 80, etc...}
        """
        
        # Récupérer les résultats au fur et à mesure
        for future in concurrent.futures.as_completed(future_to_port):
            """concurrent.futures.as_completed(future_to_port) : Permet d'itérer sur les objets Future au fur et à mesure qu'ils se terminent."""
            port = future_to_port[future] # Fait le lien entre le Future et le port qu'il teste
            try:
                result = future.result() # Récupère le résultat de l'exécution du Future soit le numéro du port s'il est ouvert, None sinon
            except Exception as exc:
                print(f'Port {port} a généré une exception: {exc}') # Gestion des erreurs


def main():
    """Fonction principale du programme."""
    # Récupération et validation des arguments passés en ligne de commande
    target = validate_arguments()
    
    # Configuration du gestionnaire de signal
    signal.signal(signal.SIGINT, signal_handler)
    
    # Lancement du scan
    scan_ports(target)
    
    # Affichage des résultats
    print("\nScan terminé. Ports ouverts :", sorted(openned_ports))


# ========== POINT D'ENTRÉE ==========
"""Exécute la fonction main() si le script est exécuté directement (et non importé comme module)."""
if __name__ == "__main__":
    main()
