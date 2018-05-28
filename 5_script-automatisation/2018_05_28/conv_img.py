#! /usr/bin/env python3.6

import numpy as np
import cv2
from math import pi, sin, cos
import os

liste_fichier_brute = os.listdir()
liste_fichier_img = os.listdir()
extension = str(input("Indiquer l'extension des images: "))


len_ext=len(extension)
for i in range(len(liste_fichier_brute)-1):
    name_fichier = liste_fichier_brute[i]
    if name_fichier[-len_ext:]!=extension:
        liste_fichier_img.remove(name_fichier)
        
os.mkdir('image_png')
for image in liste_fichier_img:
    img = cv2.imread(image)

    cv2.imwrite(os.path.join('image_png', image+'.PNG'),img)





