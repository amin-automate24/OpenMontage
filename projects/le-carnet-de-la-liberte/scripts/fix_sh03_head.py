#!/usr/bin/env python3
"""SH03 local head tilt (no AI): rotate head+hair about the neck so the face rises toward the teacher; uncovered slivers inpainted.
Input: v003 (iris already moved). Output: v004. Originals untouched."""
import numpy as np, sys, cv2
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
R=Path(__file__).resolve().parent.parent
SRC=R/"references/p4/post/SH03_gaze_corrected_v003.png"; OUT=R/"references/p4/post"
ANG=float(sys.argv[1]) if len(sys.argv)>1 else 7.0; PIV=(1960,930)
img=Image.open(SRC).convert("RGB"); W,H=img.size
HEAD=[(1720,560),(1712,480),(1725,410),(1775,350),(1850,318),(1950,300),(2100,305),(2230,370),(2335,470),(2350,560),(2305,655),(2205,725),(2145,785),(2112,865),(2062,905),(1990,915),(1900,930),(1800,918),(1745,882),(1705,812),(1688,762),(1698,735),(1730,690),(1735,640)]
m=Image.new("L",(W,H),0); ImageDraw.Draw(m).polygon(HEAD,fill=255)
mrot=m.rotate(-ANG,center=PIV,resample=Image.BICUBIC)           # clockwise = chin/nose go up
irot=img.rotate(-ANG,center=PIV,resample=Image.BICUBIC)
mf=np.asarray(mrot.filter(ImageFilter.GaussianBlur(2.5)),np.float32)/255.0
A=np.asarray(img,np.float32); comp=A*(1-mf[...,None])+np.asarray(irot,np.float32)*mf[...,None]
unc0=(np.asarray(m)>127)&(np.asarray(mrot)<=127)                # old head pixels no longer covered
unc=cv2.dilate(unc0.astype(np.uint8)*255,np.ones((7,7),np.uint8))>0
# left of the face the background is the (uniform) blackboard / blurred classroom: copy it from 46 px to the left
comp8=np.clip(comp,0,255).astype(np.uint8)
shifted=np.roll(np.asarray(img),135,axis=1)                    # out[x] = img[x-135] (pure blackboard to the left of the forehead)
core=cv2.erode((np.asarray(mrot)>127).astype(np.uint8),np.ones((5,5),np.uint8))>0                # keep the rotated head intact
unc2=cv2.dilate(unc0.astype(np.uint8)*255,np.ones((17,17),np.uint8))>0
yy,xx=np.mgrid[0:H,0:W]; left=unc2&~core&(xx<1840)&(yy<690)
fb=np.asarray(mf,np.float32)[...,None]*0
comp8[left]=shifted[left]
rest=(unc2&~left&~core&(yy>=670)).astype(np.uint8)*255; rest[(yy<670)]=0                           # chin / neck / back slivers: ordinary inpaint
res=cv2.inpaint(cv2.cvtColor(comp8,cv2.COLOR_RGB2BGR),rest,9,cv2.INPAINT_TELEA)
# soften the seam of the copied patch
Image.fromarray(cv2.cvtColor(res,cv2.COLOR_BGR2RGB)).save(OUT/"SH03_gaze_head_v004.png"); print("ok",ANG)
