#! /usr/bin/env python3
from lxml import etree
import numpy as np
from xlwt import Workbook
with open('08Aero.txt', 'r') as f:
    liste_ori=f.readlines()

entree='Ori-'+liste_ori[0].strip()

del liste_ori[0]

with open('08Aero.txt', 'w') as w:
    for ori_out in liste_ori:
        w.write(ori_out)
        
fich_residu = entree + "/residus.xml"
print(fich_residu)
tree = etree.parse(entree+"/residus.xml")

book = Workbook()
feuil1 = book.add_sheet('Residu')
feuil1.write(6,0,'Image')
feuil1.write(6,1,'Residu')
feuil1.write(6,2,'PercOk')
feuil1.write(6,3,'NbPts')
feuil1.write(6,4,'NbPtsMul')
feuil1.write(0,0,'Residu moyen')
feuil1.write(0,1,'Ecart moyen')
feuil1.write(0,2,'NbPts moyen')
feuil1.write(0,3,'NbPtsMul moyen')
feuil1.col(0).width = 4000
feuil1.col(1).width = 4000
feuil1.col(2).width = 4000
feuil1.col(3).width = 4000
feuil1.col(4).width = 4000
feuil1.col(5).width = 4000





nb_im=6
residu_OneIm = []
residu=[]
PercOk=[]
NbPts=[]
NbPtsMul=[]

#Recuperation de la derniere iteration dans Iters
for iters in tree.xpath("/XmlSauvExportAperoGlob/Iters"):
    Iters = iters

#Repercation des valeurs de la derniere iteration (Residu, PercOk, ...)
for name in Iters:
    if name.tag == 'OneIm':
        i=nb_im-6
        nb_im+=1
        Name = name
        for detail_img in Name:
            if detail_img.tag == 'Name':
                feuil1.write(nb_im,0, detail_img.text)
                residu_OneIm.append({"name":detail_img.text})
            elif detail_img.tag == 'Residual':
                residu.append(float(detail_img.text))
                feuil1.write(nb_im,1, round(float(detail_img.text),4))
                residu_OneIm[i]["Residu"]=round(float(detail_img.text),4)
            elif detail_img.tag == 'PercOk':
                PercOk.append(float(detail_img.text))
                feuil1.write(nb_im,2, round(float(detail_img.text),4))
                residu_OneIm[i]["PercOk"]=round(float(detail_img.text),4)
            elif detail_img.tag == 'NbPts':
                NbPts.append(int(detail_img.text))
                feuil1.write(nb_im,3, int(detail_img.text))
                residu_OneIm[i]["NbPts"]=int(detail_img.text)
            elif detail_img.tag == 'NbPtsMul':
                NbPtsMul.append(int(detail_img.text))
                feuil1.write(nb_im,4, int(detail_img.text))
                residu_OneIm[i]["NbPtsMul"]=int(detail_img.text)


#Calcul des moyennes et ecriture dans le fichier de sortie
vi_res= residu-np.mean(residu)
em_res = (np.sum(vi_res**2)/(len(vi_res-1)))**0.5
feuil1.write(1,0,np.mean(residu))
feuil1.write(1,1,np.mean(em_res))
feuil1.write(1,2,np.mean(NbPts))
feuil1.write(1,3,np.mean(NbPtsMul))

for i in range(len(residu_OneIm)):
    if residu_OneIm[i]['Residu']==round(max(residu),4):
        res_max = 'Le residu max est de ' + str(residu_OneIm[i]["Residu"])+" sur l'image " + residu_OneIm[i]["name"]
        feuil1.write(2,0, res_max)
    if residu_OneIm[i]['PercOk']==round(min(PercOk),4):
        pour_min = 'Le Pourcentage min est de ' + str(residu_OneIm[i]["PercOk"])+" sur l'image " + residu_OneIm[i]["name"]
        feuil1.write(3,0, pour_min)
    if residu_OneIm[i]['NbPts']==min(NbPts):
        NbPts_min = 'Le NbPts min est de ' + str(residu_OneIm[i]["NbPts"])+" sur l'image " + residu_OneIm[i]["name"]  
        feuil1.write(4,0, NbPts_min)


#Traitement des commentaires de test des images
i=0
commentaire = ''
for x in vi_res:
    if vi_res[i]>=2.58*em_res:
        commentaire = "Vi superieur a 2.58em"        
    if residu_OneIm[i]["NbPts"]<200:
        if commentaire!='':
            commentaire+= " / Image comprenant moins de 200 pts homologues"
        else:
            commentaire+= "Image comprenant moins de 200 pts homologues"
    if residu_OneIm[i]["PercOk"]<80:
        if commentaire!='':
            commentaire+= " / Pourcentage des points homologues justes en-dessous de 70%"
        else:
            commentaire+= "Pourcentage des points homologues justes en-dessous de 70%"    
    if commentaire!='':
        feuil1.write(i+7,5, commentaire)     
    commentaire=''
    i+=1

book.save('03'+entree+'_residus.xls')
