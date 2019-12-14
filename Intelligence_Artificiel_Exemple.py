from tkinter import *
from tkinter import messagebox
import os
from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import *

class Fait:
    def __init__(self, num=-1, fait=""):
        self.num=num
        self.fait=fait

class Regle:
    def __init__(self, num=-1, premisse=[], concl="", active=True):
        self.num=num
        self.premisse=premisse
        self.concl=concl
        self.active=active
    
    #read les faits a partir de base de connaissance (file) la resultat retourné dans une liste
def read_faits(file):
    list=[]
    nb=1
    f=open(file,"r")
    lines=f.readlines()
    for x in lines:
        if((x.startswith('si '))==False):
            list.append(Fait(nb,x[:-1]))        
            nb+=1
    return list

    #read les régles a partir de base de connaissance (file)la resultat retourné dans une liste
def read_regles(file):
    list=[]
    nb=1
    f=open(file,"r")
    lines=f.readlines()
    for x in lines:
        if((x.startswith('si '))==True):
            ligne=x.split(" alors ")
            ligne[0]=ligne[0][3:]
            list.append(Regle(nb,ligne[0].split(" et "),ligne[1][:-1],True))    
            nb+=1
    return list
#afficher la base de faits sur le console
def showBF(faits):
    print("BF: {",end='')
    for x in faits:
        print(x.fait,sep='',end=',')
    print("}")

#afficher la resultat de base de fait dans le fichier trace 
def showBF_fichier(faits):
    ch=""
    end=''
    end1=','
    sep=''
    ch=ch+("BF: {"+end)
    for x in faits:
        ch=ch+(x.fait+sep+end1)
    ch=ch+("}")
    print(ch)
    return(ch+"\n")

def showBR(regles):
    print("BR")
    for x in regles:
       print(x.num)
       for y in x.premisse:
           print(y)
       print(x.concl,x.active)

#afficher la resultat de base de Régles dans le fichier trace 
    
def showBR_fichier(regles):
    ch=""
    ch=ch+"BR :"
    for x in regles:
        ch=ch+(str(x.num))
        for y in x.premisse:
            ch=ch+str(y +": \n")
        ch=ch+(str(x.concl))
        ch=ch+(str(x.active))
    return (ch+"\n")
#fonction qui permet de verifier si but est inclut dans la base de fait
def exist(but, bf):
    for x in bf:
        if but==x.fait:
            return True
    return False

def match(premisse, bf):
    for x in premisse:
        if exist(x,bf)==False:
            return False
    return True

def error(ch, bf):
    if ch[-4:]=="Vrai":
        ch=ch[:-4]+"Faux"
    else:
        ch=ch[:-4]+"Vrai"
    return exist(ch, bf)

def filtrageAV(br, bf):
    BRF=[]
    for x in br:
        if x.active and match(x.premisse, bf):
            x.active=False
            BRF.append(x)
    return BRF

def filtrageAV_avecConflit(br, bf):
    BRF=[]
    for x in br:
        if x.active and match(x.premisse, bf):
            x.active=False
            BRF.insert(0,x)
    return BRF

#Addition de regles actives sous contraintes dans la BRF
def chainageAvant(bf, br, but, file):
    if exist(but,bf):
        return True #but existe dans BF
    BRF=filtrageAV(br,bf)
    while BRF:
        for r in BRF:
            if error(r.concl,bf):
                file.write("error")
                print("error")
                return False
            bf.append(Fait(len(bf),r.concl))
            file.write("Regle declanchable :R"+str(r.num)+"\n")
            file.write(showBF_fichier(bf))
            print("R",r.num)
            showBF(bf)
            if but==r.concl:
                return True
        BRF=filtrageAV(br,bf)    
    return False

def filtrageAR(but, br):
    BRF=[]
    for x in br:
        if x.concl==but:
            BRF.append(x)
    return BRF

def verif(premisse,br,bf,file):
    v=True
    i=0
    while v and i<len(premisse):
        v=chainageArriere(bf, br, premisse[i],file)
        i+=1
    return v
#Addition de regles actives sous contraintes que la 1ere régle soit declenchable dans la BRF
def chainageAvantAvecConflit(bf, br, but, file):
    if exist(but,bf):
        return True
    BRF=filtrageAV(br,bf)
    while BRF:
        for r in BRF:
            if error(r.concl,bf):
                file.write("error")
                print("error")
                return False
            bf.append(Fait(len(bf),r.concl))
            file.write("Regle declanchable :R"+str(r.num)+"\n")
            file.write(showBF_fichier(bf))
            print("R",r.num)
            showBF(bf)
            if but==r.concl:
                return True
        BRF=filtrageAV_avecConflit(br,bf) #remplir BRF sous la contrainte de 1ere régle declenchable   
    return False

def chainageArriere(bf, br, but, file):
    if exist(but,bf):
        return True
    ok=False
    BRF=filtrageAR(but,br)
    i=0
    while ok==False and i<len(BRF):
        r=BRF[i]
        if error(r.concl,bf):
            file.write("error")
            print("error")
            return False
        file.write("Régle déclanchable : R"+str(r.num)+"-> \n")
        showBF_fichier(bf)    
        print("R",r.num,sep='',end='->')
        ok=verif(r.premisse,br,bf,file)
        i+=1
        if ok:
            bf.append(Fait(len(bf),r.concl))         
    return ok

def ouvrirfichier():
    filename = askopenfilename(title="Ouvrir votre base de connaissance",filetypes=[('txt files','.txt'),('all files','.*')])
    label = Label(window, text=filename, bg="yellow")
    label.pack()    
    return filename
def trace():
     showwarning('Informations utiles', 'Merci d accéder au trace.txt qui a été crée dans votre repertoire ou se trouve le projet ****.py')  
     filename = askopenfilename(title="Ouvrir votre fichier trace",filetypes=[('txt files','.txt'),('all files','.*')])
     fichier = open(filename, "r")
     content = fichier.read()
     fichier.close()
    #afficher le dialog contenant le trace
     window2=Tk()
     window2.title("Trace")
     label=Label(window2,text=content,bg="blue",fg='white')
     label.pack(padx=12, pady=12)
#affichege de message d'alert dans le cas ou but non ecrit ou 0 pour indiquer q'on va faire la saturation
def alert(ch):
    if(ch==''):
        showwarning('Impossible de continuer', 'Veuillez entrer un but ou "0" Pour saturer la base')
        return False
    return True
#fonction Principale qui va creer notre interface graphique et manipuler tous les données
def executer():
        if(alert(but.get())):
            f_resultat= open("trace.txt", "w")
            nom_fichier=ouvrirfichier() #
            faits=read_faits(nom_fichier)
            regles=read_regles(nom_fichier)   
            f_resultat.write(str(showBF_fichier(faits)))
            #selection d'option  avec conflit (1ere régle declenchable) ou sans conflit
            selected=liste.curselection()
            print(selected)
            if(str(selected)=="(0,)"):   
                if(Y.get()==1):
                    if(str(selected)=="(0,)"):
                        b=chainageAvantAvecConflit(faits, regles, but.get(), f_resultat)
                    else:    
                        b=chainageAvant(faits, regles, but.get(), f_resultat)
                    if but.get()=='0':
                        f_resultat.write(str(showBF_fichier(faits)))
                        f_resultat.write("\n **FIN**")
                        print("FIN")
                    elif b==True:
                        f_resultat.write(str(showBF_fichier(faits)))        
                        f_resultat.write(str(but.get()+" Found"))
                    else:
                        f_resultat.write(str(showBF_fichier(faits)))        
                        f_resultat.write(str(but.get())+" NOT found")
                else:
                    f_resultat.write("Le but a chercher : "+str(but.get())+"\n")
                    b=chainageArriere(faits,regles,but.get(), f_resultat)
                    f_resultat.write(str(showBF_fichier(faits)))                    
                    if b :
                            f_resultat.write("succes")
                    else:
                             
                            f_resultat.write("Failed")
                print()
window=Tk() #initialisation d'un nouveau tkinter()
window.title("AI TP_Edition_Finale")
label=Label(window,text="But (Ecrire "+"0 "+"pour saturer la base )",bg="red") #initialisation de premier Label
label.pack(padx=12, pady=12)
#choix de but  ou saturation
but = StringVar()
Champ = Entry(window, textvariable=but, fg='red',justify='center')
Champ.focus_set()
Champ.pack(padx=5, pady=5)

#choix de methode chainage avant ou arriére
label3=Label(window,text="Choisir la methode")
label3.pack(padx=6, pady=6)
Y = IntVar()
Y1 = Radiobutton(window, text="chainage Avant", variable=Y, value="1")
Y2 = Radiobutton(window, text="chainage Arriere", variable=Y, value="2")
Y1.pack(padx=10,anchor = W)
Y2.pack(padx=10,anchor = W)
#Avec ou sans conflit
liste = Listbox(window)
liste.insert(1, "Avec Conflit(1ere regle declanchable)")
liste.insert(2, "Sans Conflit")
liste.pack(ipadx=40,ipady=2)
#button permet de choisir le fichier de base de connaissance et executer la fonction executer()
B = Button(window, text = "Choisir base de connaissance & Executer",command=executer)
B.pack(padx=5, pady=5)
#button permet d'ouvrir la fichier trace.txt
B2 = Button(window, text = "Ouvrir fichier Trace",command=trace)
B2.pack(padx=5, pady=5)

label2=Label(window,text="Base de Connaissance : ")
label2.pack(padx=6, pady=6)

window.mainloop()
