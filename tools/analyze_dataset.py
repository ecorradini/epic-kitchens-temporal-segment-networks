import os
import csv
import numpy as np
import matplotlib.pyplot as plt
import shutil

#Creo un dictionary dove inserire classe:frequenza
frequenza_classi = {}
#prendo ogni cartella nel dataset di train
for root,dirs,files in os.walk("DATASET_TRAIN",topdown=False):
    for directory in dirs:
        #prendo il nome della classe, dopo _ nel nome della cartella
        classe = directory.split('_')[1]
        #se la classe è già presente nel dictionary, aumento di uno la sua frequenza
        if classe in frequenza_classi:
            frequenza_classi[classe] += 1
        #altrimenti la inserisco con 0
        else:
            frequenza_classi[classe] = 0

#creo una lista di classi da mantenere
da_mantenere = []
#per ogni classe nel dictionary precedente
for fclasse in frequenza_classi:
    #se la frequenza è maggiore di 100, aggiungo la classe alla lista
    if(frequenza_classi[fclasse] >= 100):
        da_mantenere.append(fclasse)
        print('Da mantenere '+fclasse)

#per ogni cartella in dataset train, elimino quelle che non sono classi da mantenere
for root,dirs,files in os.walk("DATASET_TRAIN",topdown=False):
    for directory in dirs:
        classe = directory.split('_')[1]
        if classe not in da_mantenere:
            #se è da eliminare, la elimino anche dal dictionary delle classi
            if classe in frequenza_classi:
                frequenza_classi.pop(classe,None)
            #cancello la cartella
            shutil.rmtree('DATASET_TRAIN/'+directory, ignore_errors=True)
            print('Rimossa '+directory)

#Diagrammo tutto in un istogramma
plt.bar(range(len(frequenza_classi)), list(frequenza_classi.values()), align='center')
plt.xticks(range(len(frequenza_classi)), list(frequenza_classi.keys()))
plt.show()
