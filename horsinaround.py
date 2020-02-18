import sys
import cv2
from crop import Cropper
from detector import Detector
from reader import Reader
from smooth import Smoother
from writer import Writer
from progress.bar import Bar

if len(sys.argv)<=1:
    print("Usage: horsinaround.py inputfile outfile skipframes=0 framestowrite")
    exit(0)

filename = sys.argv[1]
skip = int(sys.argv[3])
framestowrite = int(sys.argv[4])

show = False



reader = Reader(filename=filename)
reader.skipFrames(skip)
print("fps:",reader.getFPS())
height = reader.getHeight()
midx = int(reader.getWidth()/2.)
midy = int(height/2.)

writer = Writer(sys.argv[2],480,720)
cropper = Cropper()
detector = Detector(draw=show)
smoother = Smoother(initx=midx,inity=midy,inith=height)



bar = Bar('Processing frames', max=framestowrite)
hhh = []


for x in range(framestowrite):
    bar.next()
    frame = reader.read()
    orig_frame = frame.copy()
    success, boxes, frame = detector.detect(frame)
    if show: cv2.imshow("frame",frame)
    if success:
        # only 1 horse at a time
        box = boxes[0]
        left,top,right,bottom = box
        height = bottom-top
        midx = left + (right-left)/2
        midy = top + height/2
        if height<0: height*=-1
        hhh.append(height)
        if midx<0: midx*=-1
        if midy<0: midy*=-1
        midx,midy,height = smoother.update(midx,midy,height)

    cutout = cropper.crop(orig_frame,midx,midy,height)
    if show: cv2.imshow("cutout",cutout)
    writer.write(cutout)

    if show:
        key= cv2.waitKey(1) & 0xFF
        if key==ord("q"):
            break
        elif key==ord("s"):
            reader.skipFrames(reader.getFPS())

cv2.destroyAllWindows()
print("")
writer.save()
print("Done!")

print(hhh)