import os
liste_fichier_brute = os.listdir()
liste_fichier_img = os.listdir()

extension = str(input("Indiquer l'extension des images: "))
px_tapioca = str(input("Indiquer la taille en pixel de la recherche de points homologues: "))
mod_calib = str(input("Indiquer la calibration (RadialStd, FishEyeBasic,...): "))
nb_calib=int(input("Indiquer le nombre de photo à prendre pour le calibration: "))
pas=int(input("Indiquer le pas à prendre entre les différents calculs d'aero figee: "))


#Epuration de la liste des fichiers
len_ext=len(extension)
for i in range(len(liste_fichier_brute)-1):
        name_fichier = liste_fichier_brute[i]
        if name_fichier[-len_ext:]!=extension:
                liste_fichier_img.remove(name_fichier)





with open('01run_commande.bat', 'w') as r:
        r.write(":Lancement des différentes commandes\n02aerotriangulation.bat\n")


#Calcul de l'aerotriangulation
tapioca='mm3d Tapioca All ".*.'+extension+'" ' + px_tapioca
num_img = 1000
nb_img=len(liste_fichier_img)
num_fin=1153
mod_calib="RadialStd"
ext=".JPG"

img_calib='"'
for i in range(nb_calib-1):
        img_calib+=liste_fichier_img[i]+'|'

img_calib=img_calib[:-1]+'"'
calibrate='mm3d Tapas '+mod_calib+' '+img_calib
with open('02aerotriangulation.bat', 'w') as f:
        f.write(":Calcul des points homologues, de la calibration et de l'aéro-triangulation\n")
        f.write(tapioca+'\n')
        f.write(calibrate+'\n')
        f.write('02analyse-resultat.py\n')


nb=int(round(nb_img/pas+0.5,0))
img_ta='"'
m=0
q=0
figee=[]
for i in range(nb):
        figee.append('Figee'+str(q))
        for n in range(pas):
                if m+1<=nb_img:
                        img_ta += liste_fichier_img[m]+'|'
                        ta = ta='mm3d Tapas Figee '+img_ta
                        m+=1

        if q==0:
                tapas=ta[:-1]+'" InCal='+mod_calib+' Out='+figee[q]                
        else:
                tapas=ta[:-1]+'" InCal='+mod_calib+' InOri='+figee[int(q-1)]+' Out='+figee[q]

        q+=1
        if(q==nb):
                tapas_autocal='mm3d Tapas AutoCal ".*.'+extension+'" InCal='+mod_calib+' InOri='+figee[q-1]+' Out=TerLocal'              

        with open('02aerotriangulation.bat', 'a') as f:
                f.write(tapas+'\n')
                f.write('02analyse-resultat.py\n')


with open('02aerotriangulation.bat', 'a') as f:
        f.write(tapas_autocal+'\n')
        f.write('02analyse-resultat.py\n')

with open('08Aero.txt', 'w') as f:
        f.write(mod_calib+'\n')
        for ori in figee:
                f.write(ori+'\n')
        f.write('TerLocal\n')


