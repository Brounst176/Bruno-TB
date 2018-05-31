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

run_commande=[]

#Calcul de l'aerotriangulation
tapioca='mm3d Tapioca All ".*.'+extension+'" ' + px_tapioca
num_img = 1000
nb_img=len(liste_fichier_img)


#POINTS HOMOLOGUES ET AEROTRIANGULATION
#-----------------------------------------------------------------------------------------------------

#creation de la commande de calcul de points homologues et du pattern des images pour le calcul de la calibration
with open('02aerotriangulation.bat', 'w') as f:
        run_commande.append('02aerotriangulation.bat\n')
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
        f.write('mm3d AperiCloud ".*.JPG" TerLocal\n')

#Creation d'un fichier contenant toutes les orientations calculée via Tapas
with open('08Aero.txt', 'w') as f:
        f.write(mod_calib+'\n')
        for ori in figee:
                f.write(ori+'\n')
        f.write('TerLocal\n')
nom_aero = 'TerLocal'

#REFERENCEMENT DE L'AEROTRIANGULATION
#-----------------------------------------------------------------------------------------------------
geo_bool = str(input("Indiquez si vous désirez référencer votre chantier (O/N) : "))
while (geo_bool != 'O') and (geo_bool !='N'):
        geo_bool = str(input("Désirez-vous référencer votre chantier (O/N) : "))
if geo_bool == 'O':
        run_commande.append('03referencement.bat\n')
        georef = str(input("Indiquez le type de referencement SBGlobBascule = SB ou GCPGlobBascule = GCP : "))
        
        #Contrôle si l'utilisateur a bien choisi un mode de referencement
        while (georef != 'SB') and (georef !='GCP'):
                georef = str(input("Indiquez le type de referencement SBGlobBascule = SB ou GCPGlobBascule =G CP : "))
        
        with open('03referencement.bat', 'w') as r:
                r.write(':Caclul du référencement de notre aérotriangulation\n')
        
        if georef=='SB':
                image_BascQT = str(input("Indiquez les images pour la saisie des points pour le facteur d'échelle (Exemple: IMG_1502.JPG|IMG_2365): "))
                echelle_BascQT = str(input("Indiquez la longueur en m entre les 2 points saisis pour le facteur d'échelle (Exemple: 5.22): "))
                image_MasqQT = str(input("Indiquez les images pour la sélection des plans horizontaux (Exemple: IMG_1502.JPG|IMG_2365): "))
        
                with open('03referencement.bat', 'a') as f:
                        f.write('mm3d SaisieBascQT "'+image_BascQT+'" TerLocal MesureSBbascule.xml\n')
                        liste_image_MasqQT = image_MasqQT.split('|')
                        for image in liste_image_MasqQT:
                                f.write('mm3d SaisieMasqQT "'+image+'" Post=_MasqPlan\n')
                        f.write('mm3d SBGlobBascule ".*.JPG" TerLocal MesureSBbascule-S2D.xml TerSBbascule PostPlan=_MasqPlan DistFS='+echelle_BascQT+'\n')
                        f.write('mm3d AperiCloud ".*.JPG" TerSBbascule\n')
                        nom_aero = 'TerSBbascule'
        elif georef == 'GCP':
                GCP_txt = str(input("Indiquer le nom du fichier contenant les coordonnées avec l'extension (Type: #F= N X Y Z): "))
                with open(GCP_txt, 'r') as r:
                        fichier_GCP = r.readlines()
                        del fichier_GCP[0]
                GCP_xml=GCP_txt+'.xml'
        
        
                num_pts=[]
                for points in fichier_GCP:
                        line_point = points.split(' ')
                        num_pts.append(line_point[0])
        
                image_for_pts = []
                for i in range(3):
                        num = num_pts[i]
                        image_num = str(input("Indiquer les images pour la saisie initiale du point "+num+" (Exemple: IMG_2535.JPG|IMG_2542.JPG): "))
                        image_for_pts.append({"num":num, "mm3d_saisie": 'mm3d SaisieAppuisInitQT "'+image_num+'" TerLocal '+num+' MesureInitiale.xml\n'})
        
                prec_pts = str(input("Indiquer la précision des coordonnées des points GCP en m (Exemple: 0.02): "))
                prec_image = str(input("Indiquer la précision de sélection des points dans les images en px (Exemple: 1): "))
                with open('03referencement.bat', 'a') as r:
                        r.write('mm3d GCPConvert AppInFile '+ GCP_txt+' Out='+GCP_xml+'\n')
                        for dico in image_for_pts:
                                r.write(dico['mm3d_saisie'])
                        r.write('mm3d GCPBascule ".*.JPG" TerLocal TerIni '+GCP_xml+' "MesureInitiale-S2D.xml"\n')
                        r.write('mm3d SaisieAppuisPredicQT ".*.JPG" TerIni '+GCP_xml+' MesureFinal.xml\n')
                        r.write('mm3d GCPBascule ".*.JPG" TerIni TerIni2 '+GCP_xml+' "MesureFinal-S2D.xml"\n')
                        r.write('mm3d Campari ".*.JPG" TerIni2 TerFinal GCP=['+GCP_xml+','+prec_pts+',MesureFinal-S2D.xml,'+prec_image+']\n')
                        r.write('Pause\n')
                        r.write('mm3d AperiCloud ".*.JPG" TerFinal\n')
                        nom_aero = 'TerFinal'
                        
#Calcul de nuage de points denses + Maillage
#-----------------------------------------------------------------------------------------------------
mode_C3DC = str(input("Indiquez le mode de calcul de points denses (Forest, BigMac, MicMac,...): "))

with open('04points_denses.bat', 'w') as p:
        run_commande.append('04points_denses.bat\n')
        p.write('mm3d SaisieMasqQT AperiCloud_'+nom_aero+'.ply\n')
        p.write('mm3d C3DC '+mode_C3DC+' ".*.JPG" '+nom_aero+' Masq3D=AperiCloud_'+nom_aero+'_selectionInfo.xml\n')

#Creation du fichier qui lance les differentes commandes
with open('01run_commande.bat', 'w') as r:
        r.write(':Lancement des différentes commandes\n')
        for commande in run_commande:
                r.write(commande)

        

