from visionport.common import cli,settings,open_video,frames,show,finish,model,predict,detections,draw,text,writer
args=cli('Tasks 6-9: Vehicle detection, classification, confidence and per-frame count')
cfg=settings(args);m=model(cfg);cap=open_video(cfg);out=writer(args,cap)
try:
    for i,t,frame in frames(cap):
        items=detections(predict(m,frame,cfg))
        for obj in items:draw(frame,obj)
        text(frame,f'Vehicles in frame: {len(items)}')
        if out:out.write(frame)
        if not show(frame,args):break
finally:finish(cap,out)
