#!/usr/bin/env python3
"""P4 local corrections (no AI): SH02 chalk title on blackboard, SH08 cover title, SH37 crop + background defocus + backpack removal.
Originals untouched; outputs in references/p4/post/."""
import sys, numpy as np, cv2
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
sys.path.insert(0, str(Path(__file__).parent))
from compose_p2 import homography, flat_line, flat_dims, FONT
R=Path(__file__).resolve().parent.parent; SRC=R/"references/p4"; OUT=SRC/"post"
SERB="/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
def load(n): return Image.open(SRC/f"{n}.png").convert("RGB")
def shrink(q,k):
    cx=sum(p[0] for p in q)/4; cy=sum(p[1] for p in q)/4; return [(cx+(x-cx)*(1-k),cy+(y-cy)*(1-k)) for x,y in q]
def text_layer(size,quad,lines,font,scale=4.0):
    W,H=size; FW,FH=flat_dims(quad,scale); n=len(lines)
    def fit(t):
        sz=int(FH/n*0.9); f=ImageFont.truetype(font,sz)
        while sum(f.getlength(c) for c in t)>FW*0.94: sz-=2; f=ImageFont.truetype(font,sz)
        return sz
    us=min(fit(t) for t in lines); acc=np.zeros((H,W),np.float32)
    for i,t in enumerate(lines):
        flat=flat_line(t,FW,FH,FH*(i+0.5)/n,us,i+11,font,True)
        a=np.asarray(flat.transform((W,H),Image.PERSPECTIVE,homography(quad,[(0,0),(FW,0),(FW,FH),(0,FH)]),Image.BICUBIC),np.float32)/255.0
        acc=np.maximum(acc,a)
    return acc
def to1080(img): return img.resize((1920,1080),Image.LANCZOS)

def sh02():
    img=load("SH02_maitresse_tableau_v001"); W,H=img.size; arr=np.asarray(img,np.float32)/255.0
    a=text_layer((W,H),[(1280,395),(2060,388),(2060,640),(1280,648)],["18 NOVEMBRE —","FÊTE DE L'INDÉPENDANCE"],FONT,5.0)
    rng=np.random.default_rng(3); chalk=np.clip(0.72+0.28*rng.random((H,W)).astype(np.float32),0,1)   # chalk grain
    a=np.asarray(Image.fromarray((a*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.7)),np.float32)/255.0*chalk*0.92
    col=np.array([0.95,0.95,0.90],np.float32); out=arr*(1-a[...,None])+col*a[...,None]
    fin=Image.fromarray((out*255).astype(np.uint8)); fin.save(OUT/"SH02_composite_final.png"); to1080(fin).save(OUT/"SH02_edit_1080p.png")

def sh08():
    img=load("SH08_carnet_couverture_v001"); W,H=img.size; arr=np.asarray(img,np.float32)/255.0
    cover=[(1108,511),(1792,542),(1308,1026),(554,895)]            # far-left, far-right, near-right, near-left
    q=shrink(cover,0.18)
    a=text_layer((W,H),q,["AMINA —","MES SOUVENIRS"],SERB,4.0)*0.88
    ink=np.array([70,38,14],np.float32)/255.0
    out=arr*(1-a[...,None])+arr*ink*a[...,None]
    fin=Image.fromarray((out*255).astype(np.uint8)); fin.save(OUT/"SH08_composite_final.png"); to1080(fin).save(OUT/"SH08_edit_1080p.png")

def sh37():
    """Local fix: Younes + desk kept sharp (hand-drawn silhouette), classroom behind defocused (shallow depth of field), crop 1.7x."""
    img=load("SH37_maitresse_younes_cahier_v001"); W,H=img.size
    poly=[(1785,700),(1800,620),(1860,565),(1960,540),(2070,555),(2125,630),(2135,740),(2100,820),(2065,880),(2045,900),(2072,940),(2078,1100),(2072,1280),
          (1990,1280),(1560,1280),(1555,1030),(1730,1012),(1760,1000),(1800,940),(1810,900),(1805,850),(1790,790)]
    m=Image.new("L",(W,H),0); ImageDraw.Draw(m).polygon(poly,fill=255); keep=m.filter(ImageFilter.GaussianBlur(6))
    blur=img.filter(ImageFilter.GaussianBlur(11)); comp=Image.composite(img,blur,keep); comp.save(OUT/"SH37_composite_full.png")
    crop=comp.crop((1250,560,2370,1190)).resize((1920,1080),Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=1.6,percent=60,threshold=2))
    crop.save(OUT/"SH37_composite_final.png"); crop.save(OUT/"SH37_edit_1080p.png")

if __name__=="__main__":
    for s in (sys.argv[1:] or ["sh02","sh08","sh37"]): globals()[s]()
