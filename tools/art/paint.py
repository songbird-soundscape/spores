"""Turn the rendered base into a painting: layered brush strokes that follow the image's own contours
(after Hertzmann 1998), on a lightly textured paper, then a gentle wash. Usage: paint.py base.png out.jpg"""
import sys, math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage as nd
random.seed(4); rng=np.random.default_rng(4)
src=Image.open(sys.argv[1]).convert('RGB'); Wd,Hd=src.size
ref_full=np.asarray(src).astype(float)
canvas=Image.new('RGB',(Wd,Hd),(244,238,224))
lum=lambda a: a[...,0]*.3+a[...,1]*.59+a[...,2]*.11
def strokes(R, thresh, maxlen, grid, alpha):
    ref=nd.gaussian_filter(ref_full,(R*.5,R*.5,0))
    L=lum(ref); gx=nd.sobel(L,1); gy=nd.sobel(L,0); gx=nd.gaussian_filter(gx,R*.5); gy=nd.gaussian_filter(gy,R*.5)
    cur=np.asarray(canvas).astype(float)
    diff=np.sqrt(((cur-ref)**2).sum(2))
    layer=Image.new('RGBA',(Wd,Hd),(0,0,0,0)); d=ImageDraw.Draw(layer)
    pts=[]
    for y in range(0,Hd,grid):
        for x in range(0,Wd,grid):
            y0,x0=y+random.randint(0,grid-1),x+random.randint(0,grid-1)
            if y0>=Hd or x0>=Wd: continue
            if diff[max(0,y0-grid):y0+grid,max(0,x0-grid):x0+grid].mean()>thresh: pts.append((x0,y0))
    random.shuffle(pts)
    for (x0,y0) in pts:
        c=ref[y0,x0]; col=tuple(int(np.clip(v+rng.normal(0,4),0,255)) for v in c)
        path=[(x0,y0)]; x,y=float(x0),float(y0); ldx,ldy=0,0
        for i in range(maxlen):
            xi,yi=int(min(Wd-1,max(0,x))),int(min(Hd-1,max(0,y)))
            if i>1 and np.abs(ref[yi,xi]-c).sum()>60: break
            g1,g2=gx[yi,xi],gy[yi,xi]
            if math.hypot(g1,g2)<1e-3: dx,dy=(ldx,ldy) if (ldx or ldy) else (1,0.15)
            else: dx,dy=-g2,g1
            if ldx*dx+ldy*dy<0: dx,dy=-dx,-dy
            n=math.hypot(dx,dy) or 1; dx,dy=dx/n,dy/n
            if ldx or ldy: dx,dy=.6*dx+.4*ldx,.6*dy+.4*ldy; n=math.hypot(dx,dy) or 1; dx,dy=dx/n,dy/n
            x+=dx*R; y+=dy*R; path.append((x,y)); ldx,ldy=dx,dy
        w=max(1,int(R*1.6))
        d.line(path,fill=col+(alpha,),width=w,joint='curve')
        for (px,py) in (path[0],path[-1]): d.ellipse((px-w/2,py-w/2,px+w/2,py+w/2),fill=col+(alpha,))
    canvas.paste(Image.alpha_composite(canvas.convert('RGBA'),layer).convert('RGB'))
strokes(12, 0,  6, 10, 235)
strokes(6, 9,  8, 5, 230)
strokes(3, 12,  6, 3, 225)
strokes(1.6, 26, 4, 2, 220)
out=np.asarray(canvas).astype(float)
# keep the faces and the vehicles a little crisper: blend some of the base back where detail is fine
edges=nd.gaussian_filter(np.abs(nd.sobel(lum(ref_full),0))+np.abs(nd.sobel(lum(ref_full),1)),2)
m=np.clip(edges/edges.max()*3,0,1)[...,None]*0.22
out=out*(1-m)+ref_full*m
# paper grain and a slight warm wash
paper=nd.gaussian_filter(rng.normal(0,1,(Hd,Wd)),1.2); paper=(paper/paper.std())*3.5
out=out+paper[...,None]
out=out*np.array([1.01,1.0,.97])
yy,xx=np.mgrid[0:Hd,0:Wd]; v=1-0.10*(((xx-Wd/2)/(Wd/2))**2+((yy-Hd*.45)/(Hd*.7))**2); out=out*v[...,None]
Image.fromarray(np.clip(out,0,255).astype(np.uint8)).save(sys.argv[2],quality=92)
