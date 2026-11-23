from visionport.common import *
args=cli('Task 18: Detect traffic against allowed lane vector')
cfg=settings(args);m=model(cfg);cap=open_video(cfg);out=writer(args,cap)
# Image-only mode: preserve actual detections but never fabricate temporal results.
if image_mode(cap):
    print('IMAGE MODE: Wrong-way detection unavailable: video required')
    try:
        for _, _, frame in frames(cap):
            objs=detections(predict(m,frame,cfg))
            for obj in objs: draw(frame,obj)
            text(frame,f'Vehicles detected: {len(objs)}')
            image_notice(frame,'Wrong-way detection unavailable: video required')
            show(frame,args,delay=0)
    finally: finish(cap,out)
    raise SystemExit(0)
zone=cfg['wrongway_zone'];direction=np.array(cfg['wrongway_direction'],dtype=float)
if len(zone)<3 or np.linalg.norm(direction)==0:
    finish(cap,out);raise ValueError('Configure wrongway_zone polygon and nonzero wrongway_direction vector in settings.json')
direction/=np.linalg.norm(direction)
first={};alerts=set()
try:
    for i,t,frame in frames(cap):
        objs=detections(predict(m,frame,cfg,track=True),track=True)
        for obj in objs:
            k=obj['id']
            if k is None:continue
            pt=np.array(obj['foot'],dtype=float)
            if in_zone(pt,zone):
                first.setdefault(k,pt.copy())
                displacement=pt-first[k]
                if np.linalg.norm(displacement)>=cfg['wrongway_min_movement_px'] and displacement.dot(direction)<-cfg['wrongway_min_movement_px']*.5:
                    alerts.add(k)
            else:first.pop(k,None)
            draw(frame,obj,'WRONG WAY' if k in alerts else '')
        polygon(frame,zone);text(frame,f'Wrong-way vehicles: {len(alerts)}')
        if out:out.write(frame)
        if not show(frame,args):break
finally:finish(cap,out)
