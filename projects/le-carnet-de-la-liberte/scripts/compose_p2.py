#!/usr/bin/env python3
"""P2 post-production: handwritten inscriptions for SH16, SH19, SH24 (local, no AI, originals untouched)."""
import random, subprocess, sys, math, numpy as np
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import font_amatic_sc
R = Path(__file__).resolve().parent.parent
OUT = R/"references/p2/post"
FONT = str(Path(font_amatic_sc.__file__).parent/"files/AmaticSC-Bold.ttf")
CAPF = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FPS = 25
INK = {"SH16": np.array([40,30,25])/255.0, "SH19": np.array([52,30,16])/255.0, "SH24": np.array([35,38,60])/255.0}

SHOTS = {
 "SH16": dict(src="SH16_table_feuille_v001", dur=5.0,
   patch=[(1388,1067),(1512,1002),(1536,1014),(1590,1036),(1534,1076),(1446,1097)],
   quad=[(1360,1069),(1530,984),(1610,1026),(1432,1111)], inset=0.22,
   lines=[("Manifeste de",0.8,1.4,"/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"),("l'indépendance —",1.4,2.1,"/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"),("11 janvier 1944",2.1,2.8,"/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf")],
   zoom=(1.0,4.0,(1500,1045),0.2,2.8),
   caption=("ILLUSTRATION PÉDAGOGIQUE — reconstitution, non archive",1.6)),
 "SH19": dict(src="SH19_amina11_ecrit_v001", dur=6.5, patch=None,
   quad=[(1272,1251),(1397,1250),(1397,1287),(1272,1277)], inset=0.0,
   lines=[("Un jour, mon pays",0.8,2.4),("sera libre.",2.4,3.4)],
   zoom=(1.0,6.5,(1345,1266),0.5,4.2), caption=None),
 "SH24": dict(src="SH24_amina20_ecrit_v001", dur=6.0, patch=None,
   quad=[(1300,1310),(1650,1318),(1635,1428),(1190,1385)], inset=0.04,
   lines=[("Nous garderons espoir.",1.0,3.0)],
   zoom=(1.0,1.5,(1450,1340),0.5,3.5), caption=None),
}

def homography(dst, src):
    A=[];b=[]
    for (x,y),(X,Y) in zip(dst,src):
        A.append([x,y,1,0,0,0,-X*x,-X*y]);b.append(X)
        A.append([0,0,0,x,y,1,-Y*x,-Y*y]);b.append(Y)
    return np.linalg.solve(np.array(A,float),np.array(b,float)).tolist()

def shrink(q, k):
    cx=sum(p[0] for p in q)/4; cy=sum(p[1] for p in q)/4
    return [(cx+(x-cx)*(1-k),cy+(y-cy)*(1-k)) for x,y in q]

def flat_dims(q, s=4.0):
    d=lambda a,b:math.dist(a,b)
    w=(d(q[0],q[1])+d(q[3],q[2]))/2; h=(d(q[0],q[3])+d(q[1],q[2]))/2
    return int(w*s),int(h*s)

def flat_line(text, FW, FH, yc, size, seed, font=None, fixed=False):
    font=font or FONT; rnd=random.Random(seed); f=ImageFont.truetype(font,size)
    if not fixed:
        while sum(f.getlength(c) for c in text)>FW*0.92: size-=4; f=ImageFont.truetype(font,size)
    layer=Image.new("L",(FW,FH),0); total=sum(f.getlength(c) for c in text); x=(FW-total)/2
    for c in text:
        w=int(f.getlength(c))+40; tile=Image.new("L",(w+40,size*2),0); ImageDraw.Draw(tile).text((20,size*0.35),c,font=f,fill=255)
        tile=tile.rotate(rnd.uniform(-2.2,2.2) if font==FONT else 0,resample=Image.BICUBIC)
        layer.paste(255,(int(x-20),int(yc-size*0.9+(rnd.uniform(-3,3) if font==FONT else 0))),tile); x+=f.getlength(c)
    return layer

def warp(flat, quad, flatsize, size, interp=Image.BICUBIC):
    FW,FH=flatsize; co=homography(quad,[(0,0),(FW,0),(FW,FH),(0,FH)])
    return flat.transform(size,Image.PERSPECTIVE,co,interp)

def build(name, cfg):
    base=Image.open(R/f"references/p2/{cfg['src']}.png").convert("RGB"); W,H=base.size
    if cfg["patch"]:  # remove the AI scribbles on a COPY: median filter keeps the paper shading
        x0,y0,x1,y1=[int(v) for v in (min(p[0] for p in cfg["patch"])-6,min(p[1] for p in cfg["patch"])-6,max(p[0] for p in cfg["patch"])+6,max(p[1] for p in cfg["patch"])+6)]
        crop=base.crop((x0,y0,x1,y1)); med=crop.filter(ImageFilter.MedianFilter(17)).filter(ImageFilter.GaussianBlur(1.2))
        m=Image.new("L",(W,H),0); ImageDraw.Draw(m).polygon([tuple(p) for p in shrink(cfg["patch"],0.0)],fill=255)
        m=m.filter(ImageFilter.GaussianBlur(1.5)).crop((x0,y0,x1,y1))
        crop=Image.composite(med,crop,m); base=base.copy(); base.paste(crop,(x0,y0))
    q=shrink(cfg["quad"],cfg["inset"]); FW,FH=flat_dims(q); n=len(cfg["lines"])
    def fit(ln):
        f0=ln[3] if len(ln)>3 else FONT; sz=int(FH/n*0.95); ff=ImageFont.truetype(f0,sz)
        while sum(ff.getlength(c) for c in ln[0])>FW*0.92: sz-=4; ff=ImageFont.truetype(f0,sz)
        return sz
    usize=min(fit(l) for l in cfg['lines'])
    layers=[]; xgrad=Image.fromarray(np.tile(np.linspace(0,255,FW,dtype=np.uint8),(FH,1)),"L")
    for i,ln in enumerate(cfg["lines"]):
        t,t0,t1=ln[:3]; fnt=ln[3] if len(ln)>3 else None
        yc=FH*(i+0.5)/n; size=usize
        a=np.asarray(warp(flat_line(t,FW,FH,yc,size,i+3,fnt,True),q,(FW,FH),(W,H)),np.float32)/255.0
        xm=np.asarray(warp(xgrad,q,(FW,FH),(W,H)),np.float32)/255.0
        ys,xs=np.where(a>0.02); bb=(ys.min(),ys.max()+1,xs.min(),xs.max()+1)
        sub=xm[bb[0]:bb[1],bb[2]:bb[3]]; mm=a[bb[0]:bb[1],bb[2]:bb[3]]>0.1; lo,hi=sub[mm].min(),sub[mm].max()
        layers.append(dict(a=a[bb[0]:bb[1],bb[2]:bb[3]],x=(sub-lo)/max(hi-lo,1e-3),bb=bb,t0=t0,t1=t1))
    return np.asarray(base,np.float32)/255.0,layers

def state(base,layers,t,ink):
    out=base.copy()
    for L in layers:
        p=np.clip((t-L["t0"])/(L["t1"]-L["t0"]),0,1)
        if p<=0: continue
        mask=np.clip((p*1.12-L["x"])/0.12,0,1); a=(L["a"]*mask)[...,None]*0.93
        y0,y1,x0,x1=L["bb"]; reg=out[y0:y1,x0:x1]; out[y0:y1,x0:x1]=reg*(1-a)+reg*ink*a
    return out

def run(name, cfg, clip=True):
    ink=INK[name]; base,layers=build(name,cfg); H,W=base.shape[:2]
    Image.fromarray((state(base,layers,99,ink)*255).astype(np.uint8)).save(OUT/f"{name}_composite_final.png")
    ov=np.zeros((H,W,4),np.uint8)
    for L in layers:
        y0,y1,x0,x1=L["bb"]; ov[y0:y1,x0:x1,:3]=(ink*255).astype(np.uint8); ov[y0:y1,x0:x1,3]=np.maximum(ov[y0:y1,x0:x1,3],(L["a"]*0.93*255).astype(np.uint8))
    Image.fromarray(ov,"RGBA").save(OUT/f"{name}_text_layer_final.png")
    if not clip: return
    z0,z1,(cx,cy),zs,ze=cfg["zoom"]; n=int(cfg["dur"]*FPS)
    # --- frame-resolution text: flats drawn at 8 px per source px, warped straight into the 1080p frame (sharp edges)
    q=shrink(cfg["quad"],cfg["inset"]); FW2,FH2=flat_dims(q,8.0); nl=len(cfg["lines"])
    def fit2(ln):
        f0=ln[3] if len(ln)>3 else FONT; sz=int(FH2/nl*0.95); ff_=ImageFont.truetype(f0,sz)
        while sum(ff_.getlength(c) for c in ln[0])>FW2*0.92: sz-=4; ff_=ImageFont.truetype(f0,sz)
        return sz
    us=min(fit2(l) for l in cfg["lines"]); flats=[]
    for i,ln in enumerate(cfg["lines"]):
        a=np.asarray(flat_line(ln[0],FW2,FH2,FH2*(i+0.5)/nl,us,i+3,ln[3] if len(ln)>3 else None,True),np.float32)/255.0
        cols=np.where(a.max(axis=0)>0.1)[0]; flats.append((a,cols.min(),cols.max(),ln[1],ln[2]))
    base_pil=Image.fromarray((base*255).astype(np.uint8))
    ff=subprocess.Popen(["ffmpeg","-y","-v","error","-f","rawvideo","-pix_fmt","rgb24","-s","1920x1080","-r",str(FPS),"-i","-","-c:v","libx264","-preset","medium","-crf","14","-pix_fmt","yuv420p",str(OUT/f"{name}_composite_v001.mp4")],stdin=subprocess.PIPE)
    cf=ImageFont.truetype(CAPF,30); xs=np.arange(FW2,dtype=np.float32)
    for f in range(n):
        t=f/FPS; u=np.clip((t-zs)/(ze-zs),0,1); u=u*u*(3-u*2); z=z0+(z1-z0)*u
        cw,ch=W/z,H/z; ox=min(max(W/2-cw/2+(cx-W/2)*u,0),W-cw); oy=min(max(H/2-ch/2+(cy-H/2)*u,0),H-ch); sc=1920/cw
        img=np.asarray(base_pil.resize((1920,1080),Image.LANCZOS,box=(ox,oy,ox+cw,oy+ch)),np.float32)/255.0
        fq=[((x-ox)*sc,(y-oy)*sc) for x,y in q]; co=homography(fq,[(0,0),(FW2,0),(FW2,FH2),(0,FH2)])
        for a,lo,hi,t0,t1 in flats:
            pr=np.clip((t-t0)/(t1-t0),0,1)
            if pr<=0: continue
            m=np.clip((pr*1.12-(xs-lo)/max(hi-lo,1))/0.12,0,1)[None,:]
            al=np.asarray(Image.fromarray((a*m*255).astype(np.uint8)).transform((1920,1080),Image.PERSPECTIVE,co,Image.BICUBIC),np.float32)/255.0*0.95
            img=img*(1-al[...,None])+img*ink*al[...,None]
        img=Image.fromarray((img*255).astype(np.uint8))
        if cfg["caption"] and t>=cfg["caption"][1]:
            d=ImageDraw.Draw(img,"RGBA"); txt=cfg["caption"][0]; w=d.textlength(txt,font=cf)
            d.rectangle([(1920-w)/2-24,980,(1920+w)/2+24,1040],fill=(0,0,0,170)); d.text((960,1010),txt,font=cf,fill=(255,235,200),anchor="mm")
        ff.stdin.write(img.tobytes())
    ff.stdin.close(); ff.wait()

if __name__=="__main__":
    sel=[a for a in sys.argv[1:] if a in SHOTS] or list(SHOTS)
    for k in sel: run(k,SHOTS[k],clip="--still" not in sys.argv)
