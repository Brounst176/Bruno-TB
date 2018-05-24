with open('01run_commande.bat', 'w') as r:
	r.write(":Lancement des différentes commandes\n02aerotriangulation.bat\n")
#Calcul de l'aerotriangulation
tapioca='mm3d Tapioca All ".*.JPG" 1200'
num_img = 1000
nb_img=153
num_fin=1153
mod_calib="RadialStd"
ext=".JPG"
img_calib='"DSC_114[4-9].JPG|DSC_115[0-1].JPG"'
calibrate='mm3d Tapas '+mod_calib+' '+img_calib
with open('02aerotriangulation.bat', 'w') as f:
    f.write(":Calcul des points homologues, de la calibration et de l'aéro-triangulation\n")
    f.write(tapioca+'\n')
    f.write(calibrate+'\n')
    
pas=10
img_ta='"'
figee=0
nb=nb_img//pas+1
m=0
for i in range(0,nb_img,pas):
    for n in range(0,pas,1):
        if(num_img<(num_fin)):
            num_img+=1
            img_ta+='DSC_'+str(num_img)+ext+'|'
            ta='mm3d Tapas Figee '+img_ta
            tap='mm3d Tapas AutoCal '+img_ta
    if(m==0):
        tapas=ta[:-1]+'" InCal='+mod_calib+' Out=Figee'+str(figee+1)
    else:
        tapas=ta[:-1]+'" InCal='+mod_calib+' InOri=Figee'+str(figee)+' Out=Figee'+str(figee+1)
    figee+=1
    m+=1
    if(m==nb):
        tapas_autocal=tap[:-1]+'" InCal='+mod_calib+' InOri=Figee'+str(figee)+' Out=TerLocal'
    print(tapas)
    with open('02aerotriangulation.bat', 'a') as f:
        f.write(tapas+'\n')
print(tapas_autocal)
with open('02aerotriangulation.bat', 'a') as f:
        f.write(tapas_autocal+'\n')
        
            
