import os
import csv
from shutil import copy

#dictionary contenente le classi
classi={}

#Carichiamo in un hashmap tutte le classi per id
with open('classi_verbi.csv') as csvfile:
    #leggo il file csv
    CSVClassi = csv.reader(csvfile, delimiter=',')
    #per ogni riga prendo id e classe e lo inserico in una struttura dati
    for row in CSVClassi:
        classi[row[0]] = row[1]

#Dataset sorgenti già fatti
gia_fatti = []

#Tengo traccia di quelli già fatti in modo da non ripeterli
with open('DATASET_SOURCES/gia_fatti.csv') as csvfile:
    CSVFatti = csv.reader(csvfile, delimiter=',')
    for row in CSVFatti:
        #leggo quelli già fatti e li metto in una lista
        gia_fatti.append(row[0])

#contatore cartelle
counter=0

#Prendo il numero di cartella più elevato
for root,dirs,files in os.walk("DATASET_TRAIN",topdown=False):
    for directory in dirs:
        numero = int(directory.split('_')[0])
        if numero >= counter:
            counter = numero
            
#Il contatore partirà dal numero successivo all'ultimo
counter += 1

#Apriamo il file csv con tutte le annotazioni
with open('DATASET_SOURCES/all_labels.csv') as csvfile:
    #leggo il file csv
    CSVFrames = csv.reader(csvfile, delimiter=',')
    #per ogni riga voglio prendere la classe e il frame iniziale e finale
    for row in CSVFrames:
        #Nome del dataset letto nel csv
        dataset_folder = row[2]
        #Vado avanti solo se non ho già fatto questo dataset
        if dataset_folder not in gia_fatti:
            #Se la cartella sorgente del dataset esiste vado avanti
            if os.path.isdir('DATASET_SOURCES/'+dataset_folder):
                #Se l'insieme delle classi contiene questo id lo prendo (dopo aver elminato qualche classe da non considerare)
                if row[9] in classi:
                    #classe dell'azione
                    classe_verbo = classi[row[9]]
                    #frame iniziale dell'azione
                    start_frame = row[6]
                    #frame finale dell'azione
                    stop_frame = row[7]
                    
                    #creo la cartella contente i frames
                    os.mkdir("./DATASET_TRAIN/"+str(counter)+"_"+classe_verbo)
                    
                    #numero frame iniziale
                    number_image_start = int(start_frame)
                    #numero frame finale
                    number_image_stop = int(stop_frame)
                    #Array contenente il nome dei frame da copiare
                    frame_da_copiare = []
                    
                    #Vado a popolare la lista di frame da copiare
                    for counter_frame in range(number_image_start,number_image_stop+1):
                        #Genero il nome del file
                        length = len(str(counter_frame))
                        numberZero = 10-length
                        filename="frame_"
                        for i in range(1,numberZero+1):
                            filename = filename + str(0)
                        filename = filename +str(counter_frame) + ".jpg"
                        frame_da_copiare.insert(len(frame_da_copiare),filename)
                    
                    for file in frame_da_copiare:
                        copy("DATASET_SOURCES/"+dataset_folder+"/"+file, "./DATASET_TRAIN/"+str(counter)+"_"+classe_verbo)
                      
                    print('Fatta cartella numero '+str(counter))
                    counter+=1
                
    
        
        