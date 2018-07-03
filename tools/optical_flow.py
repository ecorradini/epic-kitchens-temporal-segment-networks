import os
from pipes import quote
from multiprocessing import Pool, current_process

df_path='temporal_segment_networks/lib/dense_flow/'
dataset_train = 'DATASET_TRAIN/'
out_path = 'DATASET_FLOW/'
NUM_CPU=1

if not os.path.isdir(out_path):
    os.makedirs(out_path)
    
for root,dirs,files in os.walk("DATASET_TRAIN",topdown=False):
    for directory in dirs:
        
        vid_path = dataset_train+directory+'/'+directory+'.avi'
        
        vid_name = vid_path.split('/')[-1].split('.')[0]
        out_full_path = os.path.join(out_path, directory+'/')
        
        if not os.path.isdir(out_full_path):
            try:
                os.mkdir(out_full_path)
            except OSError:
                pass

            image_path = '{}img'.format(out_full_path)
            flow_x_path = '{}flow_x'.format(out_full_path)
            flow_y_path = '{}flow_y'.format(out_full_path)

            cmd = os.path.join(df_path + 'build/extract_cpu')+' -f={} -x={} -y={} -i={} -b=20 -t=1 -s=1 -o=avi -w=340 -h=256'.format(
                quote(vid_path), quote(flow_x_path), quote(flow_y_path), quote(image_path))

            print(cmd)
            
            os.system(cmd)
            print('{} done'.format(vid_name))
