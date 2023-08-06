#!/usr/bin/env python
# coding=utf-8

from parapheur.parapheur import config
import os

url = config.get("Database", "url")
port = config.get("Database", "port")
name = config.get("Database", "name")
password = config.get("Database", "password")

argument = "script/ipclean.sh "

if url != "":
    argument = "-s " + url + " "
if port != "":
    argument += "-P " + port + " "
if name != "":
    argument += "-u " + name + " "
if password != "":
    argument += "-p " + password + " "

os.system(argument)