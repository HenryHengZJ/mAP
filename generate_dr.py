import json
import cv2
import os
import sys

test_dir = "/mydrive/ObjDetection/Test"
out_dir = "/content/mAP/input/detection-results"
jsonfilepath = "result.json"

if ("--jsonfile" in sys.argv):
    jsonfilepath = sys.argv[sys.argv.index("--jsonfile") + 1]
    
# Reading json file
with open(jsonfilepath) as f:
  data = json.load(f)

for itemindex in range(len(data)):
    
    boxes = []
    cur_data = data[itemindex]
    cur_objects = cur_data["objects"]
    len_obj = len(cur_objects)
    image_path = cur_data["filename"]
    image = cv2.imread(image_path)
    h, w = image.shape[:2]

    for index in range(len_obj):
        cur_box = cur_objects[index]
        className = cur_box["name"]
        tooth_num = className.split("_")[0]

        classID = cur_box["class_id"]
        confidence = cur_box["confidence"]
        x = cur_box["relative_coordinates"]["center_x"]
        y = cur_box["relative_coordinates"]["center_y"]
        width = cur_box["relative_coordinates"]["width"]
        height = cur_box["relative_coordinates"]["height"]
        bbox_width = float(width) * w
        bbox_height = float(height) * h
        center_x = float(x) * w
        center_y = float(y) * h
        xmin = round(center_x - (bbox_width / 2))
        ymin = round(center_y - (bbox_height / 2))
        xmax = round(center_x + (bbox_width / 2))
        ymax = round(center_y + (bbox_height / 2))

        newbox = className + " " + str(confidence) + " " + str(int(xmin)) + " " + str(int(ymin)) + " " + str(int(xmax)) + " " + str(int(ymax))
        boxes.append(newbox)

    outfilename = image_path.split("/")[-1].split(".")[0] + ".txt"
    with open(out_dir + "/" + outfilename, "w") as outfile:
        for box in boxes:
            outfile.write(box)
            outfile.write("\n")
        outfile.close()



    
    


    
