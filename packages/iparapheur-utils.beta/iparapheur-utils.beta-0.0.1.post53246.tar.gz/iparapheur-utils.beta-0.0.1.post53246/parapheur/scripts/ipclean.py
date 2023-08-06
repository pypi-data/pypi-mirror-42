#!/usr/bin/env python
# coding=utf-8

from parapheur.parapheur import config
import os

url = config.get("Database", "url")
port = config.get("Database", "port")
name = config.get("Database", "name")
password = config.get("Database", "password")

argument = "script/ipclean.sh "

try:
    if url != "":
        argument = "-s " + url + " "
except:
    print('URL de la base de données par défaut')

try:
    if port != "":
        argument += "-P " + port + " "
except:
    print('Port de la base de données par défaut')

try:
    if name != "":
        argument += "-u " + name + " "
except:
    print('Nom de la base de données par défaut')

try:
    if password != "":
        argument += "-p " + password + " "
except:
    print('Mot de passe de la base de données par défaut')

os.system(argument)