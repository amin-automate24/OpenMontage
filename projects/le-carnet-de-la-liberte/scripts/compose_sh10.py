#!/usr/bin/env python3
"""SH10 post-production: handwritten text in perspective on the blank notebook (original image untouched). Local only."""
import random, subprocess, sys, numpy as np
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import font_amatic_sc
R = Path(__file__).resolve().parent.parent
SRC = R/"references/p1/SH10_carnet_Younes_v001.png"
OUT = R/"references/p1/post"
FONT = str(Path(font_amatic_sc.__file__).parent/"files/AmaticSC-Bold.ttf")
INK = np.array([52, 30, 16], dtype=np.float32)/255.0
FPS, DUR = 25, 6.0
# text areas (destination quads in ORIGINAL 2752x1536 coords): TL, TR, BR, BL
LEFT  = [(560,700),(950,722),(1280,1280),(745,1225)]
RIGHT = [(1090,700),(1480,615),(1650,1000),(1310,1130)]
FW, FH = 800, 900  # flat page canvas
# (page_quad, text, y_center_flat, size, t_start, t_end)
LINES = [
 (LEFT,  "Amina —",              250, 175, 0.3, 1.0),
 (LEFT,  "Mes souvenirs",        430, 175, 1.0, 1.9),
 (RIGHT, "11 janvier 1944",      150, 165, 2.0, 2.7),
 (RIGHT, "Nous rêvions",         390, 175, 2.8, 3.4),
 (RIGHT, "d'un Maroc",           570, 175, 3.4, 3.9),
 (RIGHT, "libre.",               750, 175, 3.9, 4.2),
]

def homography(dst, src):
    A=[];b=[]
    for (x,y),(X,Y) in zip(dst,src):
        A.append([x,y,1,0,0,0,-X*x,-X*y]);b.append(X)
        A.append([0,0,0,x,y,1,-Y*x,-Y*y]);b.append(Y)
    return np.linalg.solve(np.array(A,float),np.array(b,float)).tolist()

def flat_line(text, yc, size, seed):
    rnd=random.Random(seed)
    f=ImageFont.truetype(FONT,size)
    layer=Image.new("L",(FW,FH),0)
    total=sum(f.getlength(c) for c in text)
    x=(FW-total)/2
    for c in text:
        w=int(f.getlength(c))+40
        tile=Image.new("L",(w+40,size*2),0); ImageDraw.Draw(tile).text((20,size*0.35),c,font=f,fill=255)
        tile=tile.rotate(rnd.uniform(-2.2,2.2),resample=Image.BICUBIC)
        layer.paste(255,(int(x-20),int(yc-size*0.9+rnd.uniform(-4,4))),tile)
        x+=f.getlength(c)
    return layer

def warp(flat, quad, size):
    co=homography(quad,[(0,0),(FW,0),(FW,FH),(0,FH)])
    return flat.transform(size,Image.PERSPECTIVE,co,Image.BICUBIC)

def build():
    base=Image.open(SRC).convert("RGB"); W,H=base.size
    layers=[]
    xgrad=Image.fromarray(np.tile(np.linspace(0,255,FW,dtype=np.uint8),(FH,1)),"L")
    for i,(q,t,yc,sz,t0,t1) in enumerate(LINES):
        a=warp(flat_line(t,yc,sz,i+7),q,(W,H)); xm=warp(xgrad,q,(W,H))
        a=np.asarray(a,np.float32)/255.0; xm=np.asarray(xm,np.float32)/255.0
        ys,xs=np.where(a>0.02); bb=(ys.min(),ys.max()+1,xs.min(),xs.max()+1)
        # tight x-range for reveal normalisation
        sub=xm[bb[0]:bb[1],bb[2]:bb[3]]; m=a[bb[0]:bb[1],bb[2]:bb[3]]>0.1
        lo,hi=sub[m].min(),sub[m].max()
        layers.append(dict(a=a[bb[0]:bb[1],bb[2]:bb[3]],x=(sub-lo)/max(hi-lo,1e-3),bb=bb,t0=t0,t1=t1))
    return np.asarray(base,np.float32)/255.0,layers

def render_state(base,layers,t):
    out=base.copy()
    for L in layers:
        p=np.clip((t-L["t0"])/(L["t1"]-L["t0"]),0,1)
        if p<=0: continue
        soft=0.12
        mask=np.clip((p*(1+soft)-L["x"])/soft,0,1)
        a=(L["a"]*mask)[...,None]*0.93
        y0,y1,x0,x1=L["bb"]; reg=out[y0:y1,x0:x1]
        out[y0:y1,x0:x1]=reg*(1-a)+reg*INK*a   # multiply ink: keeps paper shading
    return out

def main():
    base,layers=build()
    fin=render_state(base,layers,99)
    Image.fromarray((fin*255).astype(np.uint8)).save(OUT/"SH10_composite_final.png")
    # transparent text-only layer for Resolve (final state)
    H,W=base.shape[:2]; ov=np.zeros((H,W,4),np.uint8)
    for L in layers:
        y0,y1,x0,x1=L["bb"]; a=(L["a"]*0.93*255).astype(np.uint8)
        ov[y0:y1,x0:x1,:3]=(INK*255).astype(np.uint8); ov[y0:y1,x0:x1,3]=np.maximum(ov[y0:y1,x0:x1,3],a)
    Image.fromarray(ov,"RGBA").save(OUT/"SH10_text_layer_final.png")
    if "--still" in sys.argv: return
    cmd=["ffmpeg","-y","-v","error","-f","rawvideo","-pix_fmt","rgb24","-s","1920x1080","-r",str(FPS),"-i","-","-c:v","libx264","-preset","medium","-crf","18","-pix_fmt","yuv420p",str(OUT/"SH10_composite_v001.mp4")]
    ff=subprocess.Popen(cmd,stdin=subprocess.PIPE); n=int(DUR*FPS)
    for f in range(n):
        t=f/FPS; img=Image.fromarray((render_state(base,layers,t)*255).astype(np.uint8))
        z=1.0+0.06*(f/(n-1)); cw,ch=W/z,H/z; ox,oy=(W-cw)/2,(H-ch)/2
        img=img.transform((1920,1080),Image.EXTENT,(ox,oy,ox+cw,oy+ch),Image.BICUBIC)
        ff.stdin.write(img.tobytes())
    ff.stdin.close(); ff.wait()
main()
