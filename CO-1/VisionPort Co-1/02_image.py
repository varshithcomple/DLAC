"""Task 3: Display the included traffic image; supports headless execution."""
from visionport.common import cli,settings,open_video,frames,show,finish
args=cli('Task 3: Read and display traffic image');cfg=settings(args);cap=open_video(cfg)
try:
    for i,t,frame in frames(cap):
        if not show(frame,args,delay=0):break
finally:finish(cap)
