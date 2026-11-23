import cv2
import numpy as np
from visionport.common import *
args=cli('Task 14: Traffic light colour from manually set lamp regions')
cfg=settings(args);cap=open_video(cfg);out=writer(args,cap)
roi=cfg['signal_roi'];lamps=cfg['signal_lamps']
if not roi or not all(k in lamps for k in ('red','yellow','green')):
    print('Traffic light ROI not configured; result will be UNKNOWN. No signal will be guessed.')
    roi=None
# HSV OpenCV: H=0..179; red wraps around zero.
ranges={'red':[((0,90,100),(10,255,255)),((170,90,100),(179,255,255))],
        'yellow':[((15,85,100),(38,255,255))],
        'green':[((40,65,70),(90,255,255))]}
try:
    for i,t,frame in frames(cap):
        if not roi:
            text(frame,'Signal: UNKNOWN (ROI not configured)')
            if out:out.write(frame)
            if not show(frame,args,delay=0 if image_mode(cap) else 1):break
            continue
        x1,y1,x2,y2=map(int,roi);crop=frame[y1:y2,x1:x2]
        if crop.size==0:raise ValueError('signal_roi is outside image bounds')
        hsv=cv2.cvtColor(crop,cv2.COLOR_BGR2HSV)
        counts={}
        for color, box in lamps.items():
            ax,ay,bx,by=map(int,box);tile=hsv[ay:by,ax:bx]
            if color not in ranges or tile.size==0:continue
            mask=np.zeros(tile.shape[:2],np.uint8)
            for lo,hi in ranges[color]:mask|=cv2.inRange(tile,np.array(lo,dtype=np.uint8),np.array(hi,dtype=np.uint8))
            counts[color]=int(cv2.countNonZero(mask))
            cv2.rectangle(frame,(x1+ax,y1+ay),(x1+bx,y1+by),(255,255,255),1)
        best=max(counts,key=counts.get) if counts else 'unknown'
        status=best.upper() if counts and counts[best]>=cfg['signal_min_pixels'] else 'UNKNOWN'
        cv2.rectangle(frame,(x1,y1),(x2,y2),(255,255,0),2)
        text(frame,f'Signal: {status}')
        if out:out.write(frame)
        if not show(frame,args):break
finally:finish(cap,out)
