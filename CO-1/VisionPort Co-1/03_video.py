"""Task 4: Playback requires video; a still image is a preview only."""
from visionport.common import cli,settings,open_video,frames,show,finish,image_mode,image_notice
args=cli('Task 4: Traffic video playback (image preview if only JPG supplied)');cfg=settings(args);cap=open_video(cfg)
if image_mode(cap):print('IMAGE MODE: showing one photo, not video playback. Supply --video data/traffic.mp4 for playback.')
try:
    for i,t,frame in frames(cap):
        if image_mode(cap):image_notice(frame,'Still image preview only - video playback needs an MP4')
        if not show(frame,args,delay=0 if image_mode(cap) else 30):break
finally:finish(cap)
