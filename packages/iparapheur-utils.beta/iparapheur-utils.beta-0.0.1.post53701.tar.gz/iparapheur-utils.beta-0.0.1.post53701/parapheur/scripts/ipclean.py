#!/usr/bin/env python
# coding=utf-8

from parapheur.parapheur import config
import os

url = config.get("Ipclean", "url")
port = config.get("Ipclean", "port")
name = config.get("Ipclean", "name")
password = config.get("Ipclean", "password")

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