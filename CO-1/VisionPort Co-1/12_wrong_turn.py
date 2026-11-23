from visionport.common import *
args=cli('Task 17: Detect forbidden entry-to-exit route pairs')
cfg=settings(args);m=model(cfg);cap=open_video(cfg);out=writer(args,cap)
# Image-only mode: preserve actual detections but never fabricate temporal results.
if image_mode(cap):
    print('IMAGE MODE: Wrong-turn detection unavailable: video required')
    try:
        for _, _, frame in frames(cap):
            objs=detections(predict(m,frame,cfg))
            for obj in objs: draw(frame,obj)
            text(frame,f'Vehicles detected: {len(objs)}')
            image_notice(frame,'Wrong-turn detection unavailable: video required')
            show(frame,args,delay=0)
    finally: finish(cap,out)
    raise SystemExit(0)
zones=cfg['zones'];allowed=cfg['route_allowed']
if not zones or not allowed:
    finish(cap,out);raise ValueError('Set zones {name: [[x,y],...]} and route_allowed {entry_name: [exit_name,...]} in settings.json')
seen_entries={};alerts=set();reported=set()
try:
    for i,t,frame in frames(cap):
        objs=detections(predict(m,frame,cfg,track=True),track=True)
        for obj in objs:
            k=obj['id']
            if k is None:continue
            inside=[name for name,poly in zones.items() if in_zone(obj['foot'],poly)]
            if k not in seen_entries:
                for zone in inside:
                    if zone in allowed:seen_entries[k]=zone;break
            elif k not in reported:
                entry=seen_entries[k]
                for exit_name in inside:
                    if exit_name not in allowed and exit_name!=entry:
                        if exit_name not in allowed[entry]:alerts.add(k)
                        reported.add(k);break
            draw(frame,obj,'WRONG TURN' if k in alerts else '')
        for z,p in zones.items():
            polygon(frame,p)
            if p:cv2.putText(frame,z,tuple(p[0]),cv2.FONT_HERSHEY_SIMPLEX,.5,(255,255,255),2)
        text(frame,f'Forbidden turns: {len(alerts)}')
        if out:out.write(frame)
        if not show(frame,args):break
finally:finish(cap,out)
