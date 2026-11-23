from collections import defaultdict
from visionport.common import *
args=cli('Task 20: Experimental triple-riding candidate alerts; must be human-verified')
cfg=settings(args);m=model(cfg);cap=open_video(cfg);out=writer(args,cap)
# Detect motorcycles and persons. Person to bike spatial overlap is only a candidate heuristic.
# A real triple-riding system needs validated rider association / pose data.
streak=defaultdict(int);alerts=set()
def rider_related(person,bike):
    px1,py1,px2,py2=person['xyxy'];bx1,by1,bx2,by2=bike['xyxy']
    ix=max(0,min(px2,bx2)-max(px1,bx1))
    overlap=ix/max(1,px2-px1)
    # Person's lower body should be near bike's area; still an imperfect heuristic.
    return overlap>=cfg['triple_riding_overlap_ratio'] and by1-(by2-by1)*1.25<=py2<=by2+(by2-by1)*.5
try:
    for i,t,frame in frames(cap):
        res=predict(m,frame,cfg,track=True,classes=[0,3]);objs=detections(res,track=True)
        persons=[x for x in objs if x['cls']==0]
        bikes=[x for x in objs if x['cls']==3]
        for bike in bikes:
            k=bike['id'];candidates=sum(rider_related(p,bike) for p in persons)
            if image_mode(cap) and candidates>=3:
                draw(frame,bike,'POSSIBLE 3 riders - VERIFY')
            if k is not None and not image_mode(cap):
                streak[k]=streak[k]+1 if candidates>=3 else 0
                if streak[k]>=cfg['triple_riding_min_frames']:alerts.add(k)
            draw(frame,bike,f'{candidates} possible riders'+(' CHECK' if k in alerts else ''))
        for person in persons:draw(frame,person)
        text(frame,'Image candidate review only' if image_mode(cap) else f'Possible triple-riding IDs: {len(alerts)}')
        text(frame,'EXPERIMENTAL: manual verification required',1,(0,220,255))
        if out:out.write(frame)
        if not show(frame,args):break
finally:finish(cap,out)
