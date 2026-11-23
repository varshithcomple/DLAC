from visionport.common import *
args=cli('Task 19: Restricted-zone vehicle stationary-time alerts')
cfg=settings(args);m=model(cfg);cap=open_video(cfg);out=writer(args,cap)
# Image-only mode: preserve actual detections but never fabricate temporal results.
if image_mode(cap):
    print('IMAGE MODE: Parking duration unavailable from a photo')
    try:
        for _, _, frame in frames(cap):
            objs=detections(predict(m,frame,cfg))
            for obj in objs: draw(frame,obj)
            text(frame,f'Vehicles detected: {len(objs)}')
            image_notice(frame,'Parking duration unavailable from a photo')
            show(frame,args,delay=0)
    finally: finish(cap,out)
    raise SystemExit(0)
zone=cfg['parking_zone']
if len(zone)<3:
    finish(cap,out);raise ValueError('Set parking_zone polygon in settings.json')
motion=Motion();since={};alerts=set()
try:
    for i,t,frame in frames(cap):
        objs=detections(predict(m,frame,cfg,track=True),track=True)
        motion.update(objs,t)
        for obj in objs:
            k=obj['id']
            if k is None:continue
            speed=motion.speeds.get(k)
            if in_zone(obj['foot'],zone) and speed is not None and speed<cfg['stationary_px_s']:
                since.setdefault(k,t)
                if t-since[k]>=cfg['parking_seconds']:alerts.add(k)
            else:since.pop(k,None)
            draw(frame,obj,'POSSIBLE ILLEGAL PARKING' if k in alerts else '')
        polygon(frame,zone,(0,0,255));text(frame,f'Parking alerts: {len(alerts)}')
        if out:out.write(frame)
        if not show(frame,args):break
finally:finish(cap,out)
