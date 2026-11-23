"""Task 2: Capture a camera image, or validate the bundled image without a camera."""
import argparse
from visionport.common import BASE
import cv2
p=argparse.ArgumentParser();p.add_argument('--no-display',action='store_true',help='Compatibility flag; this script does not open windows');p.add_argument('--capture',action='store_true',help='Capture a NEW camera photo, replacing data/traffic.jpg');a=p.parse_args()
dest=BASE/'data/traffic.jpg';dest.parent.mkdir(exist_ok=True)
if a.capture:
    cap=cv2.VideoCapture(0)
    try:
        if not cap.isOpened(): raise RuntimeError('Camera unavailable')
        ok,frame=cap.read()
        if not ok: raise RuntimeError('Unable to capture a camera frame')
        if not cv2.imwrite(str(dest),frame): raise RuntimeError('Image save failed')
    finally: cap.release()
else:
    if cv2.imread(str(dest)) is None: raise FileNotFoundError(f'No bundled image found: {dest}')
print(f'Traffic image ready: {dest}. Use --capture to capture a new one.')
