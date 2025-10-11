# Travail Pratique #1: TCP Port Scanner

## Auteurs
- LESR12590400, LESUEUR, Romane
- AUBL12010500, AUBRIET, Lucas

## Compatibilité
Python - 3.13

## Description
Ce projet implémente deux versions d'un scanner de ports TCP :
- **simple_scanner.py** : Version séquentielle simple
- **multi-tread_scanner.py** : Version multithreadée pour de meilleures performances

## Utilisation

### Scanner Simple (simple_scanner.py)

Scanner séquentiel qui teste les ports un par un de 1 à 1023.

#### Syntaxe :
```bash
python simple_scanner.py <adresse_ip_ou_hostname>
```

#### Exemples :
```bash
# Scanner une adresse IP
python simple_scanner.py 192.168.1.1

# Scanner un nom de domaine
python simple_scanner.py google.com

# Scanner localhost
python simple_scanner.py 127.0.0.1
```

#### Interruption :
Appuyez sur `Ctrl+C` pour interrompre le scan et afficher les ports trouvés jusqu'à présent.

---

### Scanner Multithread (multi-tread_scanner.py)

Scanner parallèle utilisant 25 threads simultanés pour des performances optimisées.

#### Syntaxe :
```bash
python multi-tread_scanner.py <adresse_ip_ou_hostname>
```

#### Exemples :
```bash
# Scanner une adresse IP avec multithreading
python multi-tread_scanner.py 8.8.8.8

# Scanner un serveur web
python multi-tread_scanner.py www.example.com

# Scanner avec nom de domaine
python multi-tread_scanner.py github.com
```

#### Configuration :
- **Plage de ports** : 1-1022 (well-known ports)
- **Timeout** : 0.25 secondes par connexion
- **Threads maximum** : 25 threads simultanés

#### Interruption :
Appuyez sur `Ctrl+C` pour interrompre le scan. Le programme affichera les ports ouverts trouvés et s'arrêtera proprement.

---

### Exemples de sortie

#### Scan réussi :
```
python simple_scanner.py google.com
Démarrage du scan TCP sur google.com...
Appuyez sur Ctrl+C pour interrompre le scan

---> Port 80 ouvert
---> Port 443 ouvert

Scan terminé :)
```

#### Interruption par l'utilisateur :
```
python multi-tread_scanner.py github.com
Démarrage du scan TCP sur github.com...
Scan des ports 1-1022
Appuyez sur Ctrl+C pour interrompre le scan

---> Port 22 ouvert
---> Port 80 ouvert
^C
Scan interrompu par l'utilisateur (Ctrl+C).
Ports ouverts trouvés jusqu'à présent : [22, 80]
```

#### Erreur de résolution :
```
python simple_scanner.py inexistant.invalid
Adresse IP ou nom d'hôte invalide : [Errno 11001] getaddrinfo failed
```

#### Erreur d'usage :
```
python simple_scanner.py
Usage: python main.py <adresse_ip or hostname>
Exemple: python simple_scanner.py 192.168.1.1
Exemple: python simple_scanner.py Google.com
```

### Notes importantes

!!!! NE PAS UTILISER DE VPN POUR LE SCAN !!!!

1. **Permissions** : Aucun privilège administrateur requis
2. **Réseau** : Fonctionne sur réseaux locaux et Internet
3. **Firewall** : Les résultats peuvent varier selon la configuration firewall
4. **Performance** : Le scanner multithread est ~10x plus rapide que la version simple
5. **Légalité** : N'utilisez ces outils que sur vos propres systèmes ou avec autorisation explicite
