#!/usr/bin/env python3
"""P3 local corrections (no AI): SH17 fake text masked + verified inscription; SH29/SH31 'reconstitution symbolique' mention
(SH31 fake text masked); SH30 notebook inscription (clip). Originals untouched."""
import sys, subprocess, numpy as np
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
sys.path.insert(0, str(Path(__file__).parent))
from compose_p2 import homography, flat_line, flat_dims, FONT
R = Path(__file__).resolve().parent.parent; SRC = R/"references/p3"; OUT = SRC/"post"
SERB="/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"; CAPF="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def load(n): return Image.open(SRC/f"{n}.png").convert("RGB")

def median_clean(img, mask_L, size=25):
    med = img.filter(ImageFilter.MedianFilter(size)).filter(ImageFilter.GaussianBlur(1.0))
    return Image.composite(med, img, mask_L.filter(ImageFilter.GaussianBlur(2)))

def text_block(img, quad, lines, ink, font=SERB, scale=4.0, alpha=0.93):
    """Draw lines (uniform size) in perspective quad at image resolution (multiply ink)."""
    W,H=img.size; FW,FH=flat_dims(quad,scale); n=len(lines)
    def fit(t):
        sz=int(FH/n*0.9); f=ImageFont.truetype(font,sz)
        while sum(f.getlength(c) for c in t)>FW*0.92: sz-=2; f=ImageFont.truetype(font,sz)
        return sz
    us=min(fit(t) for t in lines); acc=np.zeros((H,W),np.float32)
    for i,t in enumerate(lines):
        flat=flat_line(t,FW,FH,FH*(i+0.5)/n,us,i+5,font,True)
        co=homography(quad,[(0,0),(FW,0),(FW,FH),(0,FH)])
        a=np.asarray(flat.transform((W,H),Image.PERSPECTIVE,co,Image.BICUBIC),np.float32)/255.0
        acc=np.maximum(acc,a)
    arr=np.asarray(img,np.float32)/255.0; a=(acc*alpha)[...,None]
    return Image.fromarray(((arr*(1-a)+arr*ink*a)*255).astype(np.uint8)), acc

def caption_1080(img, text):
    f=img.resize((1920,1080),Image.LANCZOS); d=ImageDraw.Draw(f,"RGBA"); cf=ImageFont.truetype(CAPF,30)
    w=d.textlength(text,font=cf); d.rectangle([(1920-w)/2-24,980,(1920+w)/2+24,1040],fill=(0,0,0,170))
    d.text((960,1010),text,font=cf,fill=(255,235,200),anchor="mm"); return f

CAP_ILL="ILLUSTRATION PÉDAGOGIQUE — reconstitution, non archive"
CAP_SYM="RECONSTITUTION SYMBOLIQUE — sans valeur documentaire"

def sh17():
    img=load("SH17_document_illustre_v001"); W,H=img.size
    m=Image.new("L",(W,H),0); ImageDraw.Draw(m).polygon([(1000,676),(1645,628),(1650,596),(1815,588),(1930,1150),(1030,1125)],fill=255)
    img=median_clean(img,m,27)
    ink=np.array([60,38,22])/255.0
    img,_=text_block(img,[(1050,393),(1658,328),(1664,385),(1055,450)],["Manifeste de l'indépendance"],ink)
    img,_=text_block(img,[(1180,790),(1700,735),(1708,830),(1188,885)],["— 11 janvier 1944 —"],ink)
    img.save(OUT/"SH17_composite_final.png"); caption_1080(img,CAP_ILL).save(OUT/"SH17_edit_1080p.png")

def sh29():
    img=load("SH29_trone_symbolique_v001"); img.save(OUT/"SH29_composite_final.png")  # unchanged image
    caption_1080(img,CAP_SYM).save(OUT/"SH29_edit_1080p.png")

def sh31():
    img=load("SH31_negociations_symboliques_v001"); W,H=img.size
    a=np.asarray(img).astype(int); lum=a.mean(axis=2)
    m=np.zeros((H,W),np.uint8); y0,y1,x0,x1=960,1530,900,1900
    sub=(lum[y0:y1,x0:x1]>135); m[y0:y1,x0:x1]=sub*255
    mL=Image.fromarray(m).filter(ImageFilter.MaxFilter(17)).filter(ImageFilter.MinFilter(17))  # close: fill the letter holes
    mL=mL.filter(ImageFilter.MinFilter(21))   # erode: stay clear of paper edges, pen, inkwell
    img=median_clean(img,mL,25); img.save(OUT/"SH31_composite_final.png")
    caption_1080(img,CAP_SYM).save(OUT/"SH31_edit_1080p.png")

def sh30():
    img=load("SH30_amina_ecrit_1955_v001"); W,H=img.size; ink=np.array([35,38,60])/255.0
    quad=[(1690,1236),(1835,1210),(1835,1318),(1690,1310)]
    lines=[("Le chemin",1.0,2.0),("a été long.",2.0,3.0)]
    fin,_=text_block(img,quad,[l[0] for l in lines],ink,font=FONT,scale=6.0)
    fin.save(OUT/"SH30_composite_final.png")
    # clip: 10 s, handwriting reveal + gentle push-in, text drawn at 1080p each frame
    dur,FPS=10.0,25; z0,z1,(cx,cy),zs,ze=1.0,1.45,(1730,1270),0.5,4.0
    FW,FH=flat_dims(quad,8.0); n=len(lines)
    def fit(t):
        sz=int(FH/n*0.95); f=ImageFont.truetype(FONT,sz)
        while sum(f.getlength(c) for c in t)>FW*0.92: sz-=4; f=ImageFont.truetype(FONT,sz)
        return sz
    us=min(fit(l[0]) for l in lines); flats=[]
    for i,(t,t0,t1) in enumerate(lines):
        a=np.asarray(flat_line(t,FW,FH,FH*(i+0.5)/n,us,i+3,FONT,True),np.float32)/255.0
        cols=np.where(a.max(axis=0)>0.1)[0]; flats.append((a,cols.min(),cols.max(),t0,t1))
    ff=subprocess.Popen(["ffmpeg","-y","-v","error","-f","rawvideo","-pix_fmt","rgb24","-s","1920x1080","-r",str(FPS),"-i","-","-c:v","libx264","-preset","medium","-crf","14","-pix_fmt","yuv420p",str(OUT/"SH30_composite_v001.mp4")],stdin=subprocess.PIPE)
    xs=np.arange(FW,dtype=np.float32)
    for f in range(int(dur*FPS)):
        t=f/FPS; u=np.clip((t-zs)/(ze-zs),0,1); u=u*u*(3-2*u); z=z0+(z1-z0)*u; cw,ch=W/z,H/z
        ox=min(max(W/2-cw/2+(cx-W/2)*u,0),W-cw); oy=min(max(H/2-ch/2+(cy-H/2)*u,0),H-ch); sc=1920/cw
        fr=np.asarray(img.resize((1920,1080),Image.LANCZOS,box=(ox,oy,ox+cw,oy+ch)),np.float32)/255.0
        fq=[((x-ox)*sc,(y-oy)*sc) for x,y in quad]; co=homography(fq,[(0,0),(FW,0),(FW,FH),(0,FH)])
        for a,lo,hi,t0,t1 in flats:
            pr=np.clip((t-t0)/(t1-t0),0,1)
            if pr<=0: continue
            mk=np.clip((pr*1.12-(xs-lo)/max(hi-lo,1))/0.12,0,1)[None,:]
            al=np.asarray(Image.fromarray((a*mk*255).astype(np.uint8)).transform((1920,1080),Image.PERSPECTIVE,co,Image.BICUBIC),np.float32)/255.0*0.93
            fr=fr*(1-al[...,None])+fr*ink*al[...,None]
        ff.stdin.write((fr*255).astype(np.uint8).tobytes())
    ff.stdin.close(); ff.wait()

if __name__=="__main__":
    sel=sys.argv[1:] or ["sh17","sh29","sh31","sh30"]
    for s in sel: globals()[s]()
