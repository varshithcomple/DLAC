from visionport.common import *
args=cli('Task 16: Count distinct tracked vehicles crossing entry and exit lines')
cfg=settings(args);m=model(cfg);cap=open_video(cfg);out=writer(args,cap)
# Image-only mode: preserve actual detections but never fabricate temporal results.
if image_mode(cap):
    print('IMAGE MODE: Entry/exit count unavailable: video required')
    try:
        for _, _, frame in frames(cap):
            objs=detections(predict(m,frame,cfg))
            for obj in objs: draw(frame,obj)
            text(frame,f'Vehicles detected: {len(objs)}')
            image_notice(frame,'Entry/exit count unavailable: video required')
            show(frame,args,delay=0)
    finally: finish(cap,out)
    raise SystemExit(0)
entry=cfg['entry_line'];exitline=cfg['exit_line']
if not entry or not exitline:
    finish(cap,out);raise ValueError('Configure entry_line and exit_line in config/settings.json')
motion=Motion();entered=set();exited=set()
try:
    for i,t,frame in frames(cap):
        objs=detections(predict(m,frame,cfg,track=True),track=True)
        old=motion.update(objs,t)
        for obj in objs:
            k=obj['id']
            if k is None:continue
            prev=old.get(k)
            if crossed(prev,obj['foot'],entry,cfg['entry_direction']):entered.add(k)
            if crossed(prev,obj['foot'],exitline,cfg['exit_direction']):exited.add(k)
            draw(frame,obj)
        draw_line(frame,entry,(0,255,0));draw_line(frame,exitline,(0,155,255))
        text(frame,f'Entry: {len(entered)} | Exit: {len(exited)}')
        if out:out.write(frame)
        if not show(frame,args):break
finally:finish(cap,out)
