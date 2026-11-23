from visionport.common import cli,settings,open_video,frames,show,finish,model,predict,detections,draw,text,writer,image_mode,image_notice
args=cli('Task 12: Track vehicle IDs with ByteTrack')
cfg=settings(args);m=model(cfg);cap=open_video(cfg);out=writer(args,cap)
# Image-only mode: preserve actual detections but never fabricate temporal results.
if image_mode(cap):
    print('IMAGE MODE: Tracking IDs unavailable from one photo')
    try:
        for _, _, frame in frames(cap):
            objs=detections(predict(m,frame,cfg))
            for obj in objs: draw(frame,obj)
            text(frame,f'Vehicles detected: {len(objs)}')
            image_notice(frame,'Tracking IDs unavailable from one photo')
            show(frame,args,delay=0)
    finally: finish(cap,out)
    raise SystemExit(0)
try:
    for i,t,frame in frames(cap):
        items=detections(predict(m,frame,cfg,track=True),track=True)
        for obj in items:draw(frame,obj)
        text(frame,f'Currently tracked: {sum(x["id"] is not None for x in items)}')
        if out:out.write(frame)
        if not show(frame,args):break
finally:finish(cap,out)
