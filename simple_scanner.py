#######################################################
# TP1 - TCP scanner
# Author: Romane Lesueur, Lucas Aubriet
#######################################################

import socket
import signal
import sys

# Vérifier qu'un argument a été fourni
if len(sys.argv) != 2:
    print("Usage: python main.py <adresse_ip>")
    print("Exemple: python main.py 192.168.1.1")
    sys.exit(1)

target = sys.argv[1]  # Récupère l'adresse IP depuis les arguments
openned_ports = []

print(f"Démarrage du scan TCP sur {target}...")
print("Appuyez sur Ctrl+C pour interrompre le scan\n")

def signal_handler(sig, frame):
    print("\n\nScan interrompu par l'utilisateur (Ctrl+C).")
    print("Ports ouverts trouvés jusqu'à présent :", openned_ports)
    sys.exit(0)  # Quitte le programme proprement

# Associe la fonction signal_handler au signal SIGINT (Ctrl+C)
signal.signal(signal.SIGINT, signal_handler)

for port in range(400, 444):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.25)
        try:
            s.connect((target, port))
            openned_ports.append(port)
            print(f"Port {port} ouvert")
        except (ConnectionRefusedError, socket.timeout, Exception):
            pass  # Ignore silencieusement les erreurs

print("\nScan terminé. Ports ouverts :", openned_ports)
