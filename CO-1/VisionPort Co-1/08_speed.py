from visionport.common import *
args=cli('Task 13: Speed from two measured-distance virtual lines')
cfg=settings(args);m=model(cfg);cap=open_video(cfg);out=writer(args,cap)
# Image-only mode: preserve actual detections but never fabricate temporal results.
if image_mode(cap):
    print('IMAGE MODE: Speed unavailable: two timed crossings required')
    try:
        for _, _, frame in frames(cap):
            objs=detections(predict(m,frame,cfg))
            for obj in objs: draw(frame,obj)
            text(frame,f'Vehicles detected: {len(objs)}')
            image_notice(frame,'Speed unavailable: two timed crossings required')
            show(frame,args,delay=0)
    finally: finish(cap,out)
    raise SystemExit(0)
a=cfg['speed_line_a'];b=cfg['speed_line_b'];dist=cfg['speed_distance_m']
if not (a and b and isinstance(dist,(int,float)) and dist>0):
    finish(cap,out);raise ValueError('Set speed_line_a, speed_line_b, and measured speed_distance_m in config/settings.json')
motion=Motion();starts={};speeds={}
try:
    for i,t,frame in frames(cap):
        objs=detections(predict(m,frame,cfg,track=True),track=True)
        old=motion.update(objs,t)
        for obj in objs:
            k=obj['id']
            if k is None:continue
            previous=old.get(k)
            if crossed(previous,obj['foot'],a,0):starts[k]=t
            if crossed(previous,obj['foot'],b,0) and k in starts and t>starts[k]:
                speeds[k]=3.6*dist/(t-starts[k]);del starts[k]
            draw(frame,obj,(f'{speeds[k]:.1f} km/h approx' if k in speeds else ''))
        draw_line(frame,a,(0,255,0));draw_line(frame,b,(0,100,255))
        text(frame,'Speed estimates require calibrated real-world line distance')
        if out:out.write(frame)
        if not show(frame,args):break
finally:finish(cap,out)
