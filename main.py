#######################################################
# TP1 - TCP scanner
# Author: Romane Lesueur, Lucas Aubriet
#######################################################

import socket
import signal
import sys
import concurrent.futures
import threading

# Vérifier qu'un argument a été fourni
if len(sys.argv) != 2:
    print("Usage: python main.py <adresse_ip>")
    print("Exemple: python main.py 192.168.1.1")
    sys.exit(1)

target = sys.argv[1]  # Récupère l'adresse IP depuis les arguments
openned_ports = []
lock = threading.Lock()  # Pour protéger la liste des ports ouverts

def signal_handler(sig, frame):
    print("\n\nScan interrompu par l'utilisateur (Ctrl+C).")
    print("Ports ouverts trouvés jusqu'à présent :", openned_ports)
    sys.exit(0)  # Quitte le programme proprement

def port_scanner(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1.0)  # Timeout plus réaliste
        try:
            result = s.connect_ex((target, port))
            if result == 0:  # 0 = connexion réussie
                with lock:  # Protection thread-safe
                    openned_ports.append(port)
                print(f"Port {port} ouvert")
                return port
            else:
                return None
        except Exception as e:
            # Port fermé ou erreur de réseau
            return None

# Associe la fonction signal_handler au signal SIGINT (Ctrl+C)
signal.signal(signal.SIGINT, signal_handler)

print(f"Démarrage du scan TCP sur {target}...")
print("Appuyez sur Ctrl+C pour interrompre le scan\n")

# Utilisation d'un context manager pour une gestion propre des threads
with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
    # Soumettre tous les ports pour scan
    future_to_port = {executor.submit(port_scanner, port): port for port in range(400, 444)}
    
    # Récupérer les résultats au fur et à mesure
    for future in concurrent.futures.as_completed(future_to_port):
        port = future_to_port[future]
        try:
            result = future.result()
            # Le résultat est soit le numéro du port (ouvert) soit None (fermé)
        except Exception as exc:
            print(f'Port {port} a généré une exception: {exc}')

print("\nScan terminé. Ports ouverts :", sorted(openned_ports))
