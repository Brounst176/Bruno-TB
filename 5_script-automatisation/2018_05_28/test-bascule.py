

georef = str(input("Indiquez le type de referencement SBGlobBascule = SB ou GCPGlobBascule = GCP : "))

while (georef != 'SB') and (georef !='GCP'):
    georef = str(input("Indiquez le type de referencement SBGlobBascule = SB ou GCPGlobBascule =G CP : "))

if georef=='SB':
    image_BascQT = str(input("Indiquez les images pour la saisie des points pour le facteur d'échelle (Exemple: IMG_1502.JPG|IMG_2365): "))
    echelle_BascQT = str(input("Indiquez la longueur en m entre les 2 points saisis pour le facteur d'échelle (Exemple: 5.22): "))
    image_MasqQT = str(input("Indiquez les images pour la sélection des plans horizontaux (Exemple: IMG_1502.JPG|IMG_2365): "))
    
    with open('03georeferencement.bat', 'w') as f:
        f.write('mm3d SaisieBascQT "'+image_BascQT+'" TerLocal MesureSBbascule.xml\n')
        liste_image_MasqQT = image_MasqQT.split('|')
        for image in liste_image_MasqQT:
            f.write('mm3d SaisieMasqQT "'+image+'" Post=_MasqPlan\n')
        f.write('mm3d SBGlobBascule ".*.JPG" TerLocal MesureSBbascule-S2D.xml TerSBbascule PostPlan=_MasqPlan DistFS='+echelle_BascQT+'\n')
elif georef == 'GCP':
    GCP_txt = str(input("Indiquer le nom du fichier contenant les coordonnées avec l'extension (Type: #F= N X Y Z): "))
    with open(GCP_txt), 'r') as r:
        fichier_GCP = r.readlines()
        del fichier_GCP[0]
    num_pts=[]
    for points in fichier_GCP:
        line_point = points.split(' ')
        num_pts.append(line_point[0])
    
    image_for_pts = []
    for num in num_pts:
        image_num = str(input("Indiquer le nom du fichier contenant les coordonnées avec l'extension (Type: #F= N X Y Z): "))
        image_for_pts.append(image_num)
        
    


    
    
    
