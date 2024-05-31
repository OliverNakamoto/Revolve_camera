import os
import shutil

directory = '/home/oliverz/Documents/Revolve/fsoco/FSOCO_data/dataset/labels/train' # Adjust the directory path accordingly
destination = '/home/oliverz/Documents/Revolve/fsoco/FSOCO_data/dataset/labels/val'
check = '/home/oliverz/Documents/Revolve/fsoco/FSOCO_data/dataset/images/val'
# Iterate through all files in the specified directory

for filename in os.listdir(directory):
    source_path = os.path.join(directory, filename)
    destination_path = os.path.join(destination, filename)
    path1 = os.path.join(check, (filename.split('.')[0]+'.jpg'))
    path2 = os.path.join(check, (filename.split('.')[0]+'.png'))
    print(path2)
    if os.path.exists(path1) or os.path.exists(path2):
        shutil.move(source_path, destination)
    
    #print(filename.split('.')[0]+'.jpg' in '/home/oliverz/Documents/Revolve/fsoco/FSOCO_data/dataset/images/val')
    #if filename.split('.')[0]+'.jpg' in '/home/oliverz/Documents/Revolve/fsoco/FSOCO_data/dataset/images/val':
    #    shutil.move(source_path, destination)
    #elif filename.split('.')[0] + '.png' in '/home/oliverz/Documents/Revolve/fsoco/FSOCO_data/dataset/images/val':
    #    shutil.move(source_path, destination)


print("File renaming completed.")