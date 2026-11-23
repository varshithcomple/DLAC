from collections import deque
from visionport.common import *
args=cli('Tasks 10-11: Traffic density and sustained-congestion heuristic')
cfg=settings(args);m=model(cfg);cap=open_video(cfg);out=writer(args,cap)
motion=Motion();history=deque()
try:
    for i,t,frame in frames(cap):
        items=detections(predict(m,frame,cfg,track=True),track=True)
        region=cfg['roi_polygon']
        items=[x for x in items if not region or in_zone(x['foot'],region)]
        motion.update(items,t)
        speeds=[motion.speeds[x['id']] for x in items if x['id'] in motion.speeds]
        avg=sum(speeds)/len(speeds) if speeds else None
        count=len(items)
        level='LOW' if count<=cfg['density_low_max'] else ('MEDIUM' if count<=cfg['density_medium_max'] else 'HIGH')
        congested_now=(count>=cfg['congestion_min_vehicles'] and avg is not None and avg<=cfg['congestion_max_avg_speed_px_s'])
        history.append((t,congested_now))
        while history and t-history[0][0]>cfg['congestion_seconds']:history.popleft()
        sustained=bool(history) and t-history[0][0]>=cfg['congestion_seconds']*.9 and all(s for _,s in history)
        for obj in items:draw(frame,obj)
        polygon(frame,region)
        text(frame,f'Count: {count} | Density: {level}')
        text(frame,'Avg motion: '+ ('unknown' if avg is None else f'{avg:.1f} px/s'),1)
        if image_mode(cap):
            text(frame,'Congestion: visual density only; motion unknown',2,(0,220,255))
        elif sustained:text(frame,'POSSIBLE CONGESTION',2,(0,0,255))
        if out:out.write(frame)
        if not show(frame,args):break
finally:finish(cap,out)
