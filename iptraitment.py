import re

# Fonction qui vérifie si l'IP est valide 
def iptraitement (target):
    
    pattern = r'^((25[0-4]|2[0-4]\d|1\d{2}|[1-9]\d|\d)\.){3}(25[0-4]|2[0-4]\d|1\d{2}|[1-9]\d|\d)$'
    
    if re.fullmatch(pattern, target):
        print(f"'{target}' est une IP valide !")
        return True
    else:
        print(f"'{target}' n'est pas une IP valide.")
        return False

