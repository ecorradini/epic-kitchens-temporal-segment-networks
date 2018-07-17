import cv2
import os

for root,dirs,files in os.walk("DATASET_TRAIN",topdown=False):
    for directory in dirs:
        frames_folder = 'DATASET_TRAIN/'+directory+'/'
        video_path = frames_folder+directory+'.avi'
        images = [img for img in os.listdir(frames_folder) if img.endswith(".jpg")]
        images.sort()
        frame = cv2.imread(os.path.join(frames_folder,images[0]))
        height,width,layers = frame.shape
        
        fourcc = cv2.VideoWriter_fourcc(*'FFV1')
        video = cv2.VideoWriter(video_path,fourcc,59.94,(width,height))
        
        for image in images:
            video.write(cv2.imread(os.path.join(frames_folder,image)))
        
        cv2.destroyAllWindows()
        video.release
        print('Fatto: '+video_path)
