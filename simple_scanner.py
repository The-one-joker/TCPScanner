#######################################################
# TP1 - TCP scanner
# Author: Romane Lesueur, Lucas Aubriet
#######################################################

import socket
import signal
import sys

# Vérifier qu'un argument a été fourni
if len(sys.argv) != 2:
    print("Usage: python main.py <adresse_ip or hostname>")
    print("Exemple: python simple_scanner.py 192.168.1.1")
    print("Exemple: python simple_scanner.py Google.com")
    sys.exit(1)

#Fonction pour vérifier que le nom d'hôte et l'IP sont valide
def validate_hostname(target):
    try : 
        socket.gethostbyname(target) # résout un hostname en adresse IP
        return True
    except socket.error as e:
        print(f"Adresse IP ou nom d'hôte invalide : {e}")
        sys.exit(1)


target = sys.argv[1]  # Récupère l'adresse IP depuis les arguments
validate_hostname(target) 
openned_ports = []

print(f"Démarrage du scan TCP sur {target}...")
print("Appuyez sur Ctrl+C pour interrompre le scan\n")

# Fonction pour gérer l'interruption par Ctrl+C
def signal_handler(sig, frame):
    print("\n\nScan interrompu par l'utilisateur (Ctrl+C).")
    print("Ports ouverts trouvés jusqu'à présent :", openned_ports)
    sys.exit(0)  # Quitte le programme proprement

# Associe la fonction signal_handler au signal SIGINT (Ctrl+C)
signal.signal(signal.SIGINT, signal_handler)

# Scanne
for port in range(1, 1023):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.25)
        try:
            s.connect((target, port))
            openned_ports.append(port)
            print(f"---> Port {port} ouvert")
        except (ConnectionRefusedError, socket.timeout, Exception):
            pass  # Ignore silencieusement les erreurs

print("\nScan terminé :)")
