#!/usr/bin/env python
# -*- coding: utf-8 -*- 
from PIL import Image
from os import listdir, renames, remove, mkdir
from shutil import copyfile
from pandas import read_excel
from io import BytesIO
from collections import Counter
from datetime import datetime, timedelta
from pyzabbix import ZabbixAPI
from requests import get
from io import BytesIO
from PIL.Image import open as pil_open


global cookies, headers

cookies = {
    'PHPSESSID': 'e8cacc181a6288bfa71036117a701147',
    'tab': '1',
    'zbx_sessionid': 'b6c2b1db0ebdaa57cf998a93a5d4605a',
}

headers = {
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.123 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'en-US,en;q=0.9,pt-BR;q=0.8,pt;q=0.7',
}

global situacao_servidores
situacao_servidores = {}
global zabbix
zabbix = ZabbixAPI("http://guardiao.workdb.com.br")
zabbix.login("lucas.hoeltgebaum", "workdb#2020")
        
class Graph():

    def __init__(self, id, servidor, graph_name):
        self.id = id
        self.servidor = servidor
        self.name = graph_name

    def remove_invalid_char(self, name):
        words_blacklist = [
        "{$SID}", 
        "-", 
        "/", 
        "{}".format("/"), 
        "(SEG)", 
        "º"
        ]
        filtered_word = ""
        altered = False
        for word in name.split():
            if "#" in word:
                if not altered:
                    filtered_word = name.replace("#", "")
                elif altered:
                    filtered_word = filtered_word.replace("#", "")
                altered = True
            elif word in words_blacklist:
                if not altered:
                    filtered_word = name.replace(word, "")
                elif altered:
                    filtered_word = filtered_word.replace(word, "")
                altered = True
            elif "/" in word:
                if not altered:
                    filtered_word = name.replace("/", "")
                elif altered:
                    filtered_word = filtered_word.replace("/", "")
                altered = True
            elif ":" in word:
                if not altered:
                    filtered_word = name.replace(":", "")
                elif altered:
                    filtered_word = filtered_word.replace(":", "")
                altered = True
            else:
                filtered_word = name
            filtered_word = filtered_word
        while filtered_word[-1] == " ":
            filtered_word = filtered_word[0:-1]
        return filtered_word

    def get_img(self):
        if "swap" not in self.name.lower() and "disk" not in self.name.lower():
            response = get('http://guardiao.workdb.com.br/chart2.php?graphid={}&from=now-1M%2FM&to=now-1M%2FM&profileIdx=web.graphs.filter&profileIdx2={}=um5etv25&screenid='.format(self.id, self.id), headers=headers, cookies=cookies, verify=False)
        else:
            response = get('http://guardiao.workdb.com.br/chart2.php?graphid={}&from=now-1M%2FM&to=now-1M%2FM&profileIdx=web.graphs.filter&profileIdx2={}&width=1274&height=280&_=um5ge3fh&screenid='.format(self.id, self.id), headers=headers, cookies=cookies, verify=False)
        img = pil_open(BytesIO(response.content))
        name = self.remove_invalid_char(self.name)
        img.save(r"Relatórios\{}\{}.png".format(self.servidor, name))
        situacao_servidores[self.servidor] = "Extracted Graphs"
        

class Servidor():
    def __init__(self, servidor, id):
        situacao_servidores[servidor] = "Initiated Process"
        self.servidor = servidor
        self.id = id
        self.graphs = (zabbix.graph.get(hostids = self.id))
        try:
            mkdir("Relatórios")
        except FileExistsError:
            pass
        try:
            mkdir(r"Relatórios\{}".format(self.servidor))
        except FileExistsError:
            pass

    def move_model(self):
        try:
            try:
                copyfile(r"Modelos\{}\_Model.docx".format(self.servidor), r"Relatórios\{}\_Model.docx".format(self.servidor))
            except FileNotFoundError:
                print("Model {} not in correct folder!".format(self.servidor))
            except FileExistsError:
                print("Model {} already in folder with relatório".format(self.servidor))
            situacao_servidores[self.servidor] = "Moved Models"
        except Exception as excp:
            print(excp)

    def get_graphs(self):
        count = 0
        for graph in self.graphs:
            count += 1
            graph_obj = Graph(id = graph["graphid"], servidor = self.servidor, graph_name = graph["name"])
            graph_obj.get_img()
            print(f"Saved {count}/{len(self.graphs)} images.")




def START(type = None, name = None, id = None):
    if type != None:
        if type.lower() == "workdb":
            servidores_excel = read_excel("Servidores.xlsx", sheet_name = "WorkDB")
        elif type.lower() == "optidata":
            servidores_excel = read_excel("Servidores.xlsx", sheet_name = "Optidata")
        for server in servidores_excel["SERVER"]:
            situacao_servidores[server] = "Not Started"
        for server, id in zip(servidores_excel["SERVER"], servidores_excel["ID"]):
            print(f"\n\nStarting data collection from server {server} with ID {id}")
            Servidor_obj = Servidor(server, id)
            Servidor_obj.move_model()
            Servidor_obj.get_graphs()
            print("\n{}".format(Counter(situacao_servidores.values())))
            
    elif type == None:
        print(f"\n\nStarting data collection from server {name} with ID {id}")
        Servidor_obj = Servidor(name, id)
        Servidor_obj.move_model()
        Servidor_obj.get_graphs()

exit = False

while not exit:
    print("1 - Gerar relatórios Optidata")
    print("2 - Gerar relatórios WorkDB")
    print("3 - Gerar relatório de servidor específico")
    print("4 - Sair")
    opcao = input()
    try:
        opcao = int(opcao)
    except ValueError:
        print("Insira um valor entre 1-3")
        opcao = input()
    if opcao == 1:
        START(type = "optidata")
    elif opcao == 2:
        START(type = "workdb")
    elif opcao == 3:
        print("Nome:")
        nome = input()
        try:
            print("ID:")
            id = input()
        except ValueError:
            print("Insira um valor numérico válido para um único Host do guardião")
            id = input()
        START(type = None, name = nome.upper(), id = id)
    elif opcao == 4:
        break
    else:
        print("Por favor insira um valor válido!")



