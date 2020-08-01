import json
import cv2
import os
import sys

train_dir = "/mydrive/ObjDetection/Train"
out_dir = "/content/mAP/input/ground-truth"
classfile = "classes.txt"
classes = []

def getImageFile(filename):
    imgextensions = [".jpg", ".JPG", ".png", ".PNG"]
    for index, ext in enumerate(imgextensions):
        imgfile = filename.split(".")[0] + ext
        if imgfile in os.listdir(train_dir):
            return imgfile
    return None


# Reading classes text file
with open(train_dir + '/' + classfile) as classiostream:
    classcontent = classiostream.read()

    for classline in classcontent.split("\n"):
        if classline != "":
            classes.append(classline)


for filename in os.listdir(train_dir):
    if filename.endswith(".txt"):

        # Check if img file exist
        imagefile = getImageFile(filename)
        if imagefile == None: continue

        # Reading text file
        with open(train_dir + "/" + filename) as iostream:
            content = iostream.read()

        boxes = []
        for line in content.split("\n"):
            if line != "":
                classID, x, y, width, height = line.split(" ")
             
                image_path = train_dir + "/" + imagefile

                image = cv2.imread(image_path)
                h, w = image.shape[:2]

                className = classes[int(classID)]

                bbox_width = float(width) * w
                bbox_height = float(height) * h
                center_x = float(x) * w
                center_y = float(y) * h
                xmin = round(center_x - (bbox_width / 2))
                ymin = round(center_y - (bbox_height / 2))
                xmax = round(center_x + (bbox_width / 2))
                ymax = round(center_y + (bbox_height / 2))

                newbox = className + " " + str(int(xmin)) + " " + str(int(ymin)) + " " + str(int(xmax)) + " " + str(int(ymax))
                boxes.append(newbox)

        outfilename = filename
        with open(out_dir + "/" + outfilename, "w") as outfile:
            for box in boxes:
                outfile.write(box)
                outfile.write("\n")
            outfile.close()



    
    


    
