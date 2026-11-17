#!/usr/bin/env python3
"""SH03 v002 local gaze correction (no AI): near eye only. Erase the old iris by inpainting from the surrounding sclera/lid shading,
then paste the iris shifted up/left (clipped by the eyelids) so the gaze points at the teacher's face. Original untouched."""
import numpy as np, sys, cv2
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
R=Path(__file__).resolve().parent.parent
SRC=R/"references/p4/SH03_younes_main_levee_v002.png"; OUT=R/"references/p4/post"; OUT.mkdir(exist_ok=True)
DX=float(sys.argv[1]) if len(sys.argv)>1 else -3; DY=float(sys.argv[2]) if len(sys.argv)>2 else -7
img=Image.open(SRC).convert("RGB"); W,H=img.size; A=np.asarray(img)
C=(1825,658)
OPEN=[(1805,655),(1815,632),(1837,623),(1863,633),(1881,668),(1864,684),(1838,693),(1810,688)]
def mk(pts=None,ell=None,blur=0):
    m=Image.new("L",(W,H),0); d=ImageDraw.Draw(m)
    if pts: d.polygon(pts,fill=255)
    if ell: d.ellipse(ell,fill=255)
    return m.filter(ImageFilter.GaussianBlur(blur)) if blur else m
O_full=mk(pts=OPEN)
O_clip=np.asarray(O_full.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.8)),np.float32)/255.0
# 1) region to repaint = iris + rim (dark pixels in an ellipse around it, inside the opening)
Ee=np.asarray(mk(ell=[C[0]-25,C[1]-33,C[0]+25,C[1]+33]))>0
dark=(A.min(axis=2)<175)
region=(Ee&dark&(np.asarray(O_full)>0)).astype(np.uint8)*255
region=cv2.dilate(region,np.ones((5,5),np.uint8))
region=cv2.bitwise_and(region,np.asarray(O_full.filter(ImageFilter.MinFilter(3))))     # stay inside the eyelid outline
bgr=cv2.cvtColor(A,cv2.COLOR_RGB2BGR); inp=cv2.inpaint(bgr,region,7,cv2.INPAINT_TELEA); base=cv2.cvtColor(inp,cv2.COLOR_BGR2RGB).astype(np.float32)
# 2) iris (original pixels) shifted, clipped by eyelids
E=mk(ell=[C[0]-21,C[1]-28,C[0]+21,C[1]+28],blur=1.2)
sh=lambda im:im.transform(im.size,Image.AFFINE,(1,0,-DX,0,1,-DY),Image.BICUBIC)
iris=np.asarray(sh(img),np.float32); Es=np.asarray(sh(E),np.float32)/255.0
ap=(Es*O_clip)[...,None]; out=base*(1-ap)+iris*ap
# upper-eyelid shadow on the sclera (restores the soft dark band the old iris used to carry)
Om=np.asarray(O_full)>0; ys,xs=np.where(Om)
for x in np.unique(xs):
    top=ys[xs==x].min(); yy=np.arange(top,top+14); w=np.exp(-(yy-top)/5.0)*0.45
    col=out[yy,x,:]; bright=col.min(axis=1)>140
    out[yy[bright],x,:]=col[bright]*(1-w[bright,None])+np.array([80,45,30],np.float32)*w[bright,None]
Image.fromarray(np.clip(out,0,255).astype(np.uint8)).save(OUT/"SH03_gaze_corrected_v003.png"); print("ok",DX,DY)
