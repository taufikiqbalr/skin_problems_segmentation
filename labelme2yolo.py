import cv2
import numpy as np
import json 
import argparse
import os
import json
import shutil

# Add Parser
parser = argparse.ArgumentParser()
parser.add_argument("--dataset", type=str, default="dataset", help="Dataset")
parser.add_argument("--names", type=str, default="classes.txt", help="Class Names")
args = parser.parse_args()

def getClassId(class_name):
    if class_name in class_names: 
        index = class_names.index(class_name) 
    else: 
        index = -1

    return index

def copyImage(filename, folder_path):
    image_name = filename + ".jpg"
    image_path = os.path.join(args.dataset, image_name)

    if(os.path.exists(image_path)):
        shutil.copy(image_path, folder_path)

    else:
        image_name = filename + ".png"
        image_path = os.path.join(args.dataset, image_name)

        if(os.path.exists(image_path)):
            shutil.copy(image_path, folder_path)

# Get Class Names
with open(args.names) as f:
    class_names = f.read().splitlines()

for file in os.listdir(args.dataset):
    if (file.endswith(".json")):
        # Get File Path
        file_path = os.path.join(args.dataset, file)
        # Opening JSON file
        f = open(file_path)
        # returns JSON object as a dictionary
        data = json.load(f)        

        # Get Image Width
        image_width = data['imageWidth']
        # Get Image Height
        image_height = data['imageHeight']

        # Create Folder
        folder_name = "yolo_annotation"
            # Check Folder 
        folder_path = os.path.join(args.dataset, folder_name)
        exists = os.path.exists(folder_path)
        if(not exists): 
            os.mkdir(folder_path)

        # Open File
        # Get Filename
        separator = file.find(".")
        filename = file[0:separator] + ".txt"
        file_txt_path = os.path.join(folder_path, filename)           
        
        # Copy Image
        copyImage(file[0:separator], folder_path)

        file_txt = open(file_txt_path, "w")     
        
        # Loop All Annotation
        for shape in data['shapes']:
            # Get Class ID
            class_id = getClassId(shape['label'])

            if(class_id != -1):
                file_txt.write(str(class_id))

                # Loop All Points
                for point in shape['points']:
                    width_point = point[0]
                    height_point = point[1]

                    rel_width = width_point / image_width
                    rel_height = height_point / image_height

                    file_txt.write(" "+str(rel_width))
                    file_txt.write(" "+str(rel_height))
            
                file_txt.write("\n")        
        file_txt.close()       