import os
liste_fichier_brute = os.listdir()
liste_fichier_img = os.listdir()

extension = str(input("Indiquer l'extension des images: "))
px_tapioca = str(input("Indiquer la taille en pixel de la recherche de points homologues: "))
mod_calib = str(input("Indiquer la calibration (RadialStd, FishEyeBasic,...): "))
nb_calib=int(input("Indiquer le nombre de photo à prendre pour le calibration ou prendre toutes les photos (Tapper 0): "))
pas=int(input("Indiquer le pas à prendre entre les différents calculs d'aero figee ou prendre toutes les photos (Tapper 0): "))


#Epuration de la liste des fichiers
len_ext=len(extension)
for i in range(len(liste_fichier_brute)):
        name_fichier = liste_fichier_brute[i]
        if name_fichier[-len_ext:]!=extension:
                liste_fichier_img.remove(name_fichier)




#Creation du fichier qui lance les differentes commandes
with open('01run_commande.bat', 'w') as r:
        r.write(":Lancement des différentes commandes\n02aerotriangulation.bat\n")

print(liste_fichier_img)
#Calcul de l'aerotriangulation
tapioca='mm3d Tapioca All ".*.'+extension+'" ' + px_tapioca
num_img = 1000
nb_img=len(liste_fichier_img)




#creation de la commande de calcul de points homologues et du pattern des images pour le calcul de la calibration
with open('02aerotriangulation.bat', 'w') as f:
        f.write(":Calcul des points homologues, de la calibration et de l'aéro-triangulation\n")
        f.write(tapioca+'\n')
        img_calib='"'
        if nb_calib == 0:
                nb_calib = nb_img+1
        for i in range(nb_calib-1):
                img_calib+=liste_fichier_img[i]+'|'
        
        img_calib=img_calib[:-1]+'"'
        calibrate='mm3d Tapas '+mod_calib+' '+img_calib 
        
        f.write(calibrate+'\n')
        f.write('02analyse-resultat.py\n')

#creation des commandes d'aérotriangulation en figeant la calibration
if pas == 0:
        nb = 1
        pas = nb_img
else:
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
                        ta='mm3d Tapas Figee '+img_ta
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
        f.write('del 08Aero.txt /q \n') #Suppression du fichier 08Aero après l'analyse des résultats
        f.write('mm3d AperiCloud ".*._234.*.JPG|.*._235.*.JPG|.*._236[0-5].JPG|.*._238.*.JPG|.*._237.*.JPG|.*._239.*.JPG" TerLocal\n')

#Creation d'un fichier contenant toutes les orientations calculée via Tapas
with open('08Aero.txt', 'w') as f:
        f.write(mod_calib+'\n')
        for ori in figee:
                f.write(ori+'\n')
        f.write('TerLocal\n')


