import os
liste_fichier_brute = os.listdir()
liste_fichier_img = os.listdir()
extension = str(input("Indiquez l'extention des images: "))
cam_supp = str(input("Indiquez les caméras à supprimer: "))
len_ext=len(extension)
for i in range(len(liste_fichier_brute)-1):
        name_fichier = liste_fichier_brute[i]
        if name_fichier[-len_ext:]!=extension:
                liste_fichier_img.remove(name_fichier)
print(liste_fichier_img)
for image in liste_fichier_img:
        if cam_supp in image:
                print('Image '+image+ ' supprimée')
                os.remove(image)

                
                