import os
import sys
import glob
import zipfile
import fnmatch
import random
import shutil

sys.path.append('.')

def line2rec(line):
        items = line.strip().split('/')
        label = class_mapping[items[0]]
        vid = items[1].split('.')[0]
        return vid, label

def walklevel(some_dir, level=1):
    some_dir = some_dir.rstrip(os.path.sep)
    assert os.path.isdir(some_dir)
    num_sep = some_dir.count(os.path.sep)
    for root, dirs, files in os.walk(some_dir):
        yield root, dirs, files
        num_sep_this = root.count(os.path.sep)
        if num_sep + level <= num_sep_this:
            del dirs[:]

def build_split_list(split_tuple, frame_info, split_idx, shuffle=False):
    split = split_tuple[split_idx]

    def build_set_list(set_list):
        rgb_list, flow_list = list(), list()
        for item in set_list:
            frame_dir = frame_info[0][item[0]]
            rgb_cnt = frame_info[1][item[0]]
            flow_cnt = frame_info[2][item[0]]
            rgb_list.append('{} {} {}\n'.format(frame_dir, rgb_cnt, item[1]))
            flow_list.append('{} {} {}\n'.format(frame_dir, flow_cnt, item[1]))
        if shuffle:
            random.shuffle(rgb_list)
            random.shuffle(flow_list)
        return rgb_list, flow_list

    train_rgb_list, train_flow_list = build_set_list(split[0])
    test_rgb_list, test_flow_list = build_set_list(split[1])
    return (train_rgb_list, test_rgb_list), (train_flow_list, test_flow_list)

dataset = "DATASET_FLOW/"
rgb_p = 'img_'
flow_x_p = 'flow_x'
flow_y_p = 'flow_y'
num_split = 3
out_path = 'data/'
shuffle = True

#Se non esiste creo la cartella data
if not os.path.isdir('data/'):
    os.mkdir("data/")
    
#dictionary (classe, lista_cartelle)
lista_classi = {}
#dictionary (classe, frequenza_classe)
lista_frequenze = {}
#dictionary (classe, frequenza_in_train)
lista_frequenze_train = {}
#Creo le liste di training e testing
for root,dirs,files in walklevel(dataset,0):
    for directory in dirs:
        classe = directory.split('_')[1]
        if classe not in lista_classi:
            lista_classi[classe] = []
        lista_classi[classe].append(directory)
        #se la classe è già presente nel dictionary, aumento di uno la sua frequenza
        if classe in lista_frequenze:
            lista_frequenze[classe] += 1
        #altrimenti la inserisco con 0
        else:
            lista_frequenze[classe] = 0
            
#per ogni classe prendo il 70% della frequenza e lo metto come frequenza di train
for classe in lista_frequenze:
    frequenza = lista_frequenze[classe]
    frequenza70 = int((frequenza*7)/10)
    lista_frequenze_train[classe] = frequenza70

#Creo il file con l'indice delle classi
#Pulisco il file
file_lista = open('data/classInd.txt',"w")
file_lista.truncate()
file_lista.close()
file_lista = open('data/classInd.txt',"a")
counter = 1;
#Per ogni cartella scrivo nel file 
for classe in lista_classi:
    if counter > 1:
        file_lista.write('\n')
    file_lista.write(str(counter)+" "+classe)
    counter+=1
file_lista.close()

# liste contenenti i 3 folds
train1 = []
train2 = []
train3 = []
test1 = []
test2 = []
test3 = []
    
#Popolo train1 e test1: prendiamo il primo 70% di ogni classe come train e il restante 30% come test
for classe in lista_classi:
    lista_classi[classe].sort()
    for i in range(0,lista_frequenze_train[classe]):
        train1.append(lista_classi[classe][i])
    for i in range(lista_frequenze_train[classe],lista_frequenze[classe]):
        test1.append(lista_classi[classe][i])

#Popolo train2 e test2: prendiamo il primo 35% di ogni classe come train, il successivo 30% come test
    #e il restante 35% di nuovo come train
for classe in lista_classi:
    primo_fold = int(lista_frequenze_train[classe]/2)
    secondo_fold = lista_frequenze_train[classe] - primo_fold
    test_fold = lista_frequenze[classe] - (primo_fold + secondo_fold)
    for i in range(0,primo_fold):
        train2.append(lista_classi[classe][i])
    for i in range(primo_fold,(primo_fold+test_fold)):
        test2.append(lista_classi[classe][i])
    for i in range((primo_fold+test_fold),(primo_fold+test_fold+secondo_fold)):
        train2.append(lista_classi[classe][i])
#Popolo train3 e test3: prendiamo il primo 30% di ogni classe come test e il restante 70% come train
for classe in lista_classi:
    for i in range(0,lista_frequenze[classe]):
        if i < (lista_frequenze[classe] - lista_frequenze_train[classe]):
            test3.append(lista_classi[classe][i])
        else:
            train3.append(lista_classi[classe][i])
#1
txt_train1 = open('data/trainlist01.txt',"w")
txt_train1.truncate()
txt_train1.close
txt_test1 = open('data/testlist01.txt',"w")
txt_test1.truncate()
txt_test1.close
txt_train1 = open('data/trainlist01.txt',"a")
txt_test1 = open('data/testlist01.txt',"a")
counter=0
#Creo i file train1 e test1
for elemento in train1:
    if counter>0:
        txt_train1.write('\n')
    classe = elemento.split('_')[1]
    video = elemento+".avi"
    txt_train1.write(classe+'/'+video)
    counter+=1
counter=0
for elemento in test1:
    if counter>0:
        txt_test1.write('\n')
    classe = elemento.split('_')[1]
    video = elemento+".avi"
    txt_test1.write(classe+'/'+video)
    counter+=1
txt_test1.close()
txt_train1.close()

#2
txt_train2 = open('data/trainlist02.txt',"w")
txt_train2.truncate()
txt_train2.close()
txt_test2 = open('data/testlist02.txt',"w")
txt_test2.truncate()
txt_test2.close()
txt_train2 = open('data/trainlist02.txt',"a")
txt_test2 = open('data/testlist02.txt',"a")
counter=0
#Creo i file train1 e test1
for elemento in train2:
    if counter>0:
        txt_train2.write('\n')
    classe = elemento.split('_')[1]
    video = elemento+".avi"
    txt_train2.write(classe+'/'+video)
    counter+=1
counter=0
for elemento in test2:
    if counter>0:
        txt_test2.write('\n')
    classe = elemento.split('_')[1]
    video = elemento+".avi"
    txt_test2.write(classe+'/'+video)
    counter+=1
txt_test2.close()
txt_train2.close()

#3
txt_train3 = open('data/trainlist03.txt',"w")
txt_train3.truncate()
txt_train3.close()
txt_test3 = open('data/testlist03.txt',"w")
txt_test3.truncate()
txt_test3.close()
txt_train3 = open('data/trainlist03.txt',"w")
txt_test3 = open('data/testlist03.txt',"w")
counter=0
#Creo i file train1 e test1
for elemento in train3:
    if counter>0:
        txt_train3.write('\n')
    classe = elemento.split('_')[1]
    video = elemento+".avi"
    txt_train3.write(classe+'/'+video)
    counter+=1
counter=0
for elemento in test3:
    if counter>0:
        txt_test3.write('\n')
    classe = elemento.split('_')[1]
    video = elemento+".avi"
    txt_test3.write(classe+'/'+video)
    counter+=1
txt_test3.close()
txt_train3.close()

#Faccio il parse del dataset
class_ind = [x.strip().split() for x in open('data/classInd.txt')]
class_mapping = {x[1]:int(x[0])-1 for x in class_ind}

#Genero le coppie (train,test)
split_tp = []
for i in range(1, 4):
    train_list = [line2rec(x) for x in open('data/trainlist{:02d}.txt'.format(i))]
    test_list = [line2rec(x) for x in open('data/testlist{:02d}.txt'.format(i))]
    split_tp.append((train_list, test_list))

# operation
for root,dirs,files in walklevel(dataset,0):
    for directory in dirs:
        zip_folders = glob.glob(os.path.join("DATASET_FLOW/"+directory+"/", '*'))
        for i,f in enumerate(zip_folders):
            #Unzippo il file ed elimino lo zip
            if f.endswith("zip"):
                zip_file = zipfile.ZipFile(f)
                zip_file.extractall("DATASET_FLOW/"+directory+"/"+f.split('/')[2].split('.')[0])
                zip_file.close()
                os.remove(f)
        
frame_folders = glob.glob(os.path.join("DATASET_FLOW/", '*'))
rgb_counts = {}
flow_counts = {}
dir_dict = {}
for x,t in enumerate(frame_folders):
    #Continuo
    subdirectories = glob.glob(os.path.join(t,'*'))
    all_cnt = {}
    k = t.split('/')[-1]
    for i,f in enumerate(subdirectories):
        if os.path.isdir(f):
            lst = os.listdir(f)
            all_cnt[f.split('/')[-1]] = len(lst)
    rgb_counts[k] = all_cnt['img']
    dir_dict[k] = t
    x_cnt = all_cnt['flow_x']
    y_cnt = all_cnt['flow_y']
    if x_cnt != y_cnt:
        raise ValueError('x and y direction have different number of flow images. video: '+f)
    flow_counts[k] = x_cnt

f_info = dir_dict, rgb_counts, flow_counts

for i in range(max(3, len(split_tp))):
    lists = build_split_list(split_tp, f_info, i, shuffle)
    open(os.path.join("data/", 'rgb_train_split_{}.txt'.format(i+1)), 'w').writelines(lists[0][0])
    open(os.path.join("data/", 'rgb_val_split_{}.txt'.format(i+1)), 'w').writelines(lists[0][1])
    open(os.path.join("data/", 'flow_train_split_{}.txt'.format(i+1)), 'w').writelines(lists[1][0])
    open(os.path.join("data/", 'flow_val_split_{}.txt'.format(i+1)), 'w').writelines(lists[1][1])
    
for root,dirs,files in walklevel(dataset,0):
    for directory in dirs:
       subdirectories = glob.glob(os.path.join(dataset+directory,'*'))
       for subdirectory in subdirectories:
           if os.path.isdir(subdirectory):
               files = glob.glob(os.path.join(subdirectory,'*'))
               for file in files:
                   shutil.copy(file, dataset+directory)
               shutil.rmtree(subdirectory) 
