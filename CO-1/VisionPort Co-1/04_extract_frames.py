"""Task 5: Extract available frames; JPG gives exactly one source image."""
import cv2
from visionport.common import BASE,cli,settings,open_video,frames,finish,image_mode
args=cli('Task 5: Save frames from source');cfg=settings(args);cap=open_video(cfg)
outdir=BASE/'frames';outdir.mkdir(exist_ok=True)
fps=cap.get(cv2.CAP_PROP_FPS) or 30;step=max(1,round(fps));count=0
try:
    for i,t,frame in frames(cap):
        if i%step==0:
            if not cv2.imwrite(str(outdir/f'frame_{i:06d}.jpg'),frame):raise RuntimeError('Could not write frame')
            count+=1
finally:finish(cap)
print(f'Saved {count} frame(s) to {outdir}.' + (' A still image is NOT video-frame extraction.' if image_mode(cap) else ''))
