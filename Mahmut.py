import importlib, sys, smtplib, traceback, random, time, subprocess, numpy, sqlite3, warnings, json, os, check, requests

from PyQt5 import QtCore, QtGui, QtWidgets, Qt
import random, time, os, numpy, warnings, json, sqlite3, sys
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import check

owner = 'Osman-Kahraman'
repo = 'mahmut'

def run(owner, repo):
    os.chdir("{}\\built_ins".format(os.getcwd()))
    versions = sorted([file.rstrip(".py") for file in os.listdir() if file.endswith(".py")], key = lambda version: int(version.lstrip("v_").replace("_", "")))
    try:
        highest_version = versions[-1]
    except:
        highest_version = "v_1_0"

    message = sys.argv[1:]

    while highest_version and check.run():
        if not highest_version in versions:
            for module in os.listdir("..\\build\\Mahmut"):
                if module != "__pycache__":
                    if module.endswith(".py"):
                        module = module[:-3]
                        spec = importlib.util.spec_from_file_location(module, "..\\build\\Mahmut\\{}.py".format(module))
                    else:
                        spec = importlib.util.spec_from_file_location(module, "..\\build\\Mahmut\\{}\\__init__.py".format(module))

                    module_obj = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module_obj)

                    globals()[module] = module_obj

            
            r = requests.get(
                'https://raw.githubusercontent.com/{owner}/{repo}/refs/heads/main/{path}.py'.format(
                owner = owner, repo = repo, path = highest_version)
                )

            PATH = "{}.py".format(highest_version)
            if r.text != '{"message":"Not Found","documentation_url":"https://docs.github.com/rest/reference/repos#get-repository-content"}':
                with open(PATH, 'w', encoding = "utf-8") as file:
                    file.write(r.text)
                    versions.append(highest_version)

                with open("datas\\modules.txt", "r", encoding = "utf-8") as file:
                    data = file.read()

                    module_files = data.split(", ") if data else list()

                for file in module_files: 
                    if file not in os.listdir("..\\build\\Mahmut"): 
                        main_r = requests.get(
                            'https://raw.githubusercontent.com/{owner}/{repo}/refs/heads/master/{path}'.format(owner = owner, repo = repo, path = file),
                            )

                        master_PATH = "..\\build\\Mahmut\\{}".format(file)
                        with open(master_PATH, 'w') as file:
                            file.write(main_r.text)

                message = sys.argv[1:]
            else:
                message = "Not found the version..."
        else:
            for version in versions[:-1]:
                try:
                    if version != highest_version:
                        os.remove("{}.py".format(version))
                except FileNotFoundError:
                    continue
                else:
                    versions.remove(version)

            spec = importlib.util.spec_from_file_location(highest_version, "{}.py".format(highest_version))
            foo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(foo)

            program = foo.run(message = message)

            if type(program["wanted_version"]) is str: 
                highest_version = program["wanted_version"]

                if highest_version == "": 
                    a = requests.get(
                        'https://api.github.com/repos/{owner}/{repo}/contents'.format(
                        owner = owner, repo = repo)
                        )

                    versions_ = sorted([infos["name"].rstrip(".py") for infos in json.loads(a.text)], key = lambda version: int(version.lstrip("v_").replace("_", "")))
                    highest_version = versions_[-1]
            else:
                break

run(owner, repo)