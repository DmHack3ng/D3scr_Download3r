import re
import requests 
import BeautifulSoup as  BS
import optparse
import sys
import os

f="target.html"

###########
# NEXT STEP : REFACTORING CODE AND COMMENT IT :)
# Manage The Caractere Like &\##
###########

# Obtenir les options de l'utilisateur 
def get_args():
    parser=optparse.OptionParser()
    parser.add_option("-u","--url",dest="url",help="Set the target")
    return parser.parse_args()

# Lecture de fichier pour tester 
def read():
    with open(f,"r") as z:
        return z.read()
      
# Ecriture de la description dans un fichier
def writer(fi,data):
    with open(fi,"a") as r:
         r.write(data+"\n")
         r.close()

# Obtenir le code HTML
def get_code(url):
    return requests.get(url).content

# Supprimer les balises p
def get_text(string):
    f_dt=re.sub("<p>","",str(string))
    return re.sub("</p>","",str(f_dt))

# Telecharge l'image du cours     
def downloader(url):
    content=get_code(url)
    filename=url.split("/")[-1]
    with open(filename,"w") as rd:
        rd.write(content)
    print("[+] Image "+filename+" Downloaded")

# Recherche de la description dans le code HTML puis ecriture dans un fichier 
def bs_search(payload,string,clss,title):
    bs=BS.BeautifulSoup(string)
    dt=bs.findAll(payload)
    for d in dt:
        #print(d)
        cls=d.get("class")
        t=re.search("<p><",str(d))
        if not cls and not t:
            writer(title,get_text(d)+"\n")
            #print(get_text(d)+"\n")
            
# Obetnir le titre du cours            
def get_title(payload,string):
    bs=BS.BeautifulSoup(string)
    dt=bs.findAll(payload)
    for d in dt:
        title=d.get("content")
        nm=d.get("name")
        if nm=="twitter:title":
            if str(":") in title:
                title=title.replace(":","")
            #title.split(" ")         
            return title+".txt"
            
# Supprime la resolution de l'image                     
def clear_link(l):
    return l.split(" ")[0]

# Recherche de l'image dans le CODE HTML                      
def dw_image(payload, string, clss):
    bs=BS.BeautifulSoup(string)
    imgs=bs.findAll(payload)
    for img in imgs:
        cls=img.get("class")
        src=img.get("srcset")
        try:
            if "min.jpg" in src:
                f_link=clear_link(src)
                #print(f_link)
                downloader(f_link)
        except TypeError:
            continue 
def go_dir():
    os.chdir("Course/")            

# Lancement du parser de description Pour Freeeducationweb.com                 
def start_descr(url):
    go_dir()
    data=get_code(url)
    title=get_title("meta",data)
    bs_search("p",data,"card-description",title)
    dw_image("img",data,"wp-image-9547")
    

(option,argument)=get_args()
start_descr(option.url)