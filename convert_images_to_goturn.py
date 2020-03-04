# %% imports
import sys
import os
from glob import glob
import matplotlib.pyplot as plt
import cv2
from math import sqrt
folder_path = 'data/goturn/Luedinghausen/7'
train_path = folder_path + '_target'
searching_path = folder_path + '_searching'
outpath = os.path.join(folder_path, 'goturn_label.txt')
frame_width = 3840
frame_height = 2160
ratio = frame_width / frame_height
plot_width = 14
out_res = 227
sqrt2 = sqrt(2)

def jpg(name):
    return str(name) + '.jpg'

def txt(name):
    return str(name) + '.txt'

def show(frame):
    plt.figure(figsize=(plot_width, plot_width * ratio))
    plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

# %% action
file_list = glob(os.path.join(folder_path, '*.jpg'))
file_list.sort()
if not os.path.isdir(train_path): os.path.mkdir(train_path)
if not os.path.isdir(searching_path): os.path.mkdir(searching_path)
for index, target_path in enumerate(file_list):
    if index == len(file_list)-1: break
    # for...
    # searching_path = file_list[index+1]

index = 0
target_path = file_list[0]
_, target_file = os.path.split(target_path)
target_name, _ = os.path.splitext(target_file)
target_txt_path = os.path.join(folder_path, txt(target_name))
target = cv2.imread(target_path)
with open(target_txt_path, mode='r') as file:
    _, x, y, _, height = file.readline().split(' ')
    x, y, height = round(float(x)*frame_width), round(float(y)*frame_height), round(float(height)*frame_height)
    x,y,height
offset = round(sqrt2*height/2)
left, top, right, bottom = x-offset, y-offset, x+offset, y+offset
resized_target = cv2.resize(target[top:bottom, left:right], (out_res, out_res))

for i in range(1,11,3): print(i)
# if index out of bounds: break
searching_path = file_list[1]
_, searching_file = os.path.split(searching_path)
searching_name, _ = os.path.splitext(searching_file)
searching = cv2.imread(searching_path)
searching_txt_path = os.path.join(folder_path, txt(searching_name))
resized_searching = cv2.resize(searching[top:bottom, left:right], (out_res, out_res))

cropped_height = bottom-top
scale = out_res / cropped_height

with open(searching_txt_path, mode='r') as file:
    _, x, y, width, height = file.readline().split(' ')
    x, y, offset_x, offset_y = float(x*frame_width), float(y*frame_height), float(width*frame_width/2), float(height*frame_height/2)
sleft, stop, sright, sbottom = round(x-offset_x), round(y-offset_y), round(x+offset_x), round(y+offset_y)
sleft, stop, sright, sbottom = sleft-left, stop-top, sright-left, sbottom-top
sleft, stop, sright, sbottom = sleft*scale, stop*scale, sright*scale, sbottom*scale
sleft, stop, sright, sbottom = sleft/out_res, stop/out_res, sright/out_res, sbottom/out_res