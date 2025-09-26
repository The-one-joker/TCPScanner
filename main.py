#######################################################
# TP1 - TCP scanner
# Author: Romane Lesueur, Lucas Aubriet
#######################################################

import re
import scanner

pattern = r'^((25[0-4]|2[0-4]\d|1\d{2}|[1-9]\d|\d)\.){3}(25[0-4]|2[0-4]\d|1\d{2}|[1-9]\d|\d)$'

print("Welcome to the TCP scanner :)")
target = str(input("Enter the target IP address: "))

if re.fullmatch(pattern, target):
    print(f"'{target}' est une IP valide !")
else:
    print(f"'{target}' n'est pas une IP valide.")

answer = str(input("Do you want scan port 0 to 1024 ? (y/n) :"))

if (answer == "y"):
    scanner(target, 0, 1024)
elif answer == "n":
    port_range = str(input("Enter the port range (e.g., 20-80) :"))
    start_port, end_port = map(int, port_range.split('-'))
    scanner(target, start_port, end_port)
