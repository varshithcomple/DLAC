from visionport.common import *
args=cli('Task 15: Per-vehicle waiting time from low pixel motion')
cfg=settings(args);m=model(cfg);cap=open_video(cfg);out=writer(args,cap)
# Image-only mode: preserve actual detections but never fabricate temporal results.
if image_mode(cap):
    print('IMAGE MODE: Waiting time unavailable: video required')
    try:
        for _, _, frame in frames(cap):
            objs=detections(predict(m,frame,cfg))
            for obj in objs: draw(frame,obj)
            text(frame,f'Vehicles detected: {len(objs)}')
            image_notice(frame,'Waiting time unavailable: video required')
            show(frame,args,delay=0)
    finally: finish(cap,out)
    raise SystemExit(0)
motion=Motion();stopped_since={};waits={}
try:
    for i,t,frame in frames(cap):
        objs=detections(predict(m,frame,cfg,track=True),track=True)
        motion.update(objs,t)
        for obj in objs:
            k=obj['id']
            if k is None:continue
            velocity=motion.speeds.get(k)
            if velocity is not None and velocity < cfg['stationary_px_s']:
                stopped_since.setdefault(k,t)
                duration=t-stopped_since[k]
                waits[k]=duration if duration>=cfg['waiting_stopped_seconds'] else 0
            else:
                stopped_since.pop(k,None);waits[k]=0
            draw(frame,obj,f'waiting {waits.get(k,0):.1f}s')
        text(frame,'Waiting time based on video timestamps and pixel motion')
        if out:out.write(frame)
        if not show(frame,args):break
finally:finish(cap,out)
