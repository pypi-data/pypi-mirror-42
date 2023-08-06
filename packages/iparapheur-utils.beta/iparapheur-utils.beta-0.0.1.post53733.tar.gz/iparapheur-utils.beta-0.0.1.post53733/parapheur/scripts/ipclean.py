#!/usr/bin/env python
# coding=utf-8

from parapheur.parapheur import config
import os
from os import path as os_path

PATH = os_path.abspath(os_path.split(__file__)[0])
script = PATH + "/script/ipclean.sh "

url = config.get("Ipclean", "url")
port = config.get("Ipclean", "port")
name = config.get("Ipclean", "name")
password = config.get("Ipclean", "password")

if url != "":
    script = "-s " + url + " "

if port != "":
    script += "-P " + port + " "

if name != "":
    script += "-u " + name + " "

if password != "":
    script += "-p " + password + " "

os.system(script)