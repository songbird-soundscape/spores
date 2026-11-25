"""Watercolour crossroads for the Sporae Dispersae AI notice, drawn through a pinhole camera.
World: metres, x east, y north, z up. The crossroads is at the origin. The photographer stands
in the corn south-west of the crossroads, at eye height, looking north-north-east past the
waiting pickup toward the mop-bucket robot under the flashing light."""
import math, random
import numpy as np
random.seed(7)
import sys
W,H=320,160
GLOW='--noglow' not in sys.argv
CAM=np.array([-8.0,-11.5,1.6]); YAW=math.radians(20); PITCH=math.radians(4.2); HFOV=math.radians(96)
F=(W/2)/math.tan(HFOV/2); CX,CY=W/2,H/2
fwd=np.array([math.sin(YAW)*math.cos(PITCH), math.cos(YAW)*math.cos(PITCH), math.sin(PITCH)])
rgt=np.array([math.cos(YAW), -math.sin(YAW), 0.0]); up=np.cross(rgt,fwd)
def cam(p): d=np.asarray(p,float)-CAM; return np.array([d@rgt, d@up, d@fwd])
def scr(c): return (CX+F*c[0]/c[2], CY-F*c[1]/c[2])
def proj(p): return scr(cam(p))
def depth(p): return cam(p)[2]
NEAR=0.4
def clip(poly):
    """clip a world polygon against the near plane; return screen points"""
    cs=[cam(p) for p in poly]; out=[]
    for i in range(len(cs)):
        a,b=cs[i],cs[(i+1)%len(cs)]
        ina,inb=a[2]>NEAR,b[2]>NEAR
        if ina: out.append(a)
        if ina!=inb:
            t=(NEAR-a[2])/(b[2]-a[2]); out.append(a+(b-a)*t)
    return [scr(c) for c in out]
def _c(v,lo,hi): return max(lo,min(hi,v))
def path(pts,close=True): return ('M'+' L'.join(f'{_c(x,-600,920):.2f} {_c(y,-400,560):.2f}' for x,y in pts)+('Z' if close else '')) if pts else ''
def gpoly(pts2d,z=0.0): return path(clip([(x,y,z) for x,y in pts2d]))
def strip(center,width):
    L=[];R=[]
    for i,(x,y) in enumerate(center):
        a=center[max(i-1,0)]; b=center[min(i+1,len(center)-1)]
        dx,dy=b[0]-a[0],b[1]-a[1]; n=math.hypot(dx,dy) or 1; nx,ny=-dy/n,dx/n
        w=width(i) if callable(width) else width
        L.append((x+nx*w/2,y+ny*w/2)); R.append((x-nx*w/2,y-ny*w/2))
    return L+R[::-1]
P=[]; A=P.append
HZ=CY+F*math.tan(PITCH)   # horizon on screen: looking up a little puts it below centre
A(f'''<svg class="an-scene" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Watercolour, seen from a cornfield at eye height: a red pickup waits at a country crossroads where a yellow mop-bucket robot mops a puddle of slop under a flashing yellow light; a tractor waits across the way, a hobo and a bike tourist head off up the road into low rolling hills">
<defs>
 <filter id="an-wash" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence type="fractalNoise" baseFrequency="0.022" numOctaves="3" seed="7" result="w"/><feDisplacementMap in="SourceGraphic" in2="w" scale="5" xChannelSelector="R" yChannelSelector="G" result="d"/><feGaussianBlur in="d" stdDeviation=".9"/></filter>
 <filter id="an-wash2" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence type="fractalNoise" baseFrequency="0.03" numOctaves="3" seed="5" result="w"/><feDisplacementMap in="SourceGraphic" in2="w" scale="3" xChannelSelector="R" yChannelSelector="G" result="d"/><feGaussianBlur in="d" stdDeviation=".7"/></filter>
 <filter id="an-pencil" x="-10%" y="-10%" width="120%" height="120%"><feTurbulence type="fractalNoise" baseFrequency="0.06" numOctaves="2" seed="3" result="w"/><feDisplacementMap in="SourceGraphic" in2="w" scale="1.1" xChannelSelector="R" yChannelSelector="G" result="d"/><feGaussianBlur in="d" stdDeviation=".3"/></filter>
 <filter id="an-crisp" x="-10%" y="-10%" width="120%" height="120%"><feTurbulence type="fractalNoise" baseFrequency="0.08" numOctaves="2" seed="3" result="w"/><feDisplacementMap in="SourceGraphic" in2="w" scale=".7" xChannelSelector="R" yChannelSelector="G" result="d"/><feGaussianBlur in="d" stdDeviation=".12"/></filter>
 <filter id="an-paper"><feTurbulence type="fractalNoise" baseFrequency="1.6" numOctaves="1" seed="2"/><feColorMatrix values="0 0 0 0 .55  0 0 0 0 .5  0 0 0 0 .42  0 0 0 -1.2 .9"/></filter>
 <linearGradient id="an-sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#a9c9de"/><stop offset=".6" stop-color="#d6e2e0"/><stop offset="1" stop-color="#f4e6c6"/></linearGradient>
 <radialGradient id="an-glow"><stop offset="0" stop-color="#ffd23f" stop-opacity=".9"/><stop offset="1" stop-color="#ffd23f" stop-opacity="0"/></radialGradient>
</defs>
<rect width="{W}" height="{H}" fill="#f6f0e2"/>
<g filter="url(#an-wash)">
 <rect width="{W}" height="{HZ+2:.1f}" fill="url(#an-sky)"/>
 <ellipse cx="66" cy="20" rx="40" ry="6" fill="#c9d3da" opacity=".9"/><ellipse cx="54" cy="15" rx="17" ry="8" fill="#fbf8f0"/><ellipse cx="74" cy="11" rx="15" ry="9" fill="#fdfaf3"/><ellipse cx="92" cy="15" rx="13" ry="7" fill="#f6f3ec"/><ellipse cx="40" cy="18" rx="10" ry="5" fill="#f3f1ea"/>
 <ellipse cx="246" cy="30" rx="38" ry="5" fill="#cbd5db" opacity=".9"/><ellipse cx="236" cy="26" rx="16" ry="6" fill="#fbf8f0"/><ellipse cx="254" cy="23" rx="13" ry="7" fill="#fdfaf3"/><ellipse cx="270" cy="27" rx="10" ry="5" fill="#f3f1ea"/>
 <ellipse cx="160" cy="6" rx="60" ry="3" fill="#bed3e2" opacity=".7"/><ellipse cx="300" cy="8" rx="30" ry="2.5" fill="#bed3e2" opacity=".7"/>''')
# low rolling hills on the horizon: silhouettes from heights at long range
def hill_line(dist,amp,seed,base=0):
    rnd=random.Random(seed); ph=[rnd.uniform(0,6) for _ in range(3)]
    pts=[]
    for i in range(0,W+1,4):
        ang=YAW+math.atan((i-CX)/F)
        hgt=base+amp*(0.55+0.25*math.sin(ang*7+ph[0])+0.15*math.sin(ang*13+ph[1])+0.08*math.sin(ang*29+ph[2]))
        pts.append((i, HZ - F*(hgt/dist) - (F*math.tan(PITCH)*0)))
    return pts
far=hill_line(1800,110,1); mid=hill_line(900,45,2); near=hill_line(420,14,3)
A(f'<path d="{path(far+[(W,HZ+3),(0,HZ+3)])}" fill="#9fb2bb"/>')
A(f'<path d="{path(mid+[(W,HZ+4),(0,HZ+4)])}" fill="#9db383"/>')
A(f'<path d="{path(near+[(W,HZ+5),(0,HZ+5)])}" fill="#a9bf78"/>')
# the ground: grass, then patchwork fields, nearer fields with crops
A(f'<rect x="-20" y="{HZ-1:.1f}" width="{W+40}" height="{H-HZ+21:.1f}" fill="#b2c77c"/>')
rnd=random.Random(5)
cols=["#cdb873","#a6bf6e","#d6c27c","#9fb86a","#c2b46c","#b9cc84"]
for gx in range(-12,14):
    for gy in range(1,9):
        x0=gx*70+rnd.uniform(-10,10); y0=60+gy*gy*22+rnd.uniform(-8,8); w=rnd.uniform(45,75); h=rnd.uniform(18,40)+gy*8
        if abs(x0+w/2)<8: continue
        A(f'<path d="{gpoly([(x0,y0),(x0+w,y0),(x0+w,y0+h),(x0,y0+h)])}" fill="{rnd.choice(cols)}" opacity=".8"/>')
A(f'<path d="{gpoly([(-200,3.5),(-3.5,3.5),(-3.5,58),(-200,58)])}" fill="#a3be6c"/>')     # NW corn
A(f'<path d="{gpoly([(3.5,3.5),(14,3.5),(14,60),(3.5,60)])}" fill="#9fb86a"/>')          # NE beans
A(f'<path d="{gpoly([(14,18),(80,18),(80,70),(14,70)])}" fill="#c5c47e"/>')              # NE pasture
A(f'<path d="{gpoly([(-200,-60),(-3.5,-60),(-3.5,-3.5),(-200,-3.5)])}" fill="#8faa5c"/>')  # SW corn, where we stand
A(f'<path d="{gpoly([(-200,-60),(-3.5,-60),(-3.5,-6),(-200,-6)])}" fill="#7d9a50" opacity=".7"/>')
A('</g>')
# roads: a winding lane north into the hills, a side road west that curves away north
A('<g filter="url(#an-wash2)">')
def catmull(cp,n=10):
    out=[]
    for i in range(len(cp)-1):
        p0=cp[max(i-1,0)];p1=cp[i];p2=cp[i+1];p3=cp[min(i+2,len(cp)-1)]
        for t in np.linspace(0,1,n,endpoint=False):
            t2,t3=t*t,t*t*t
            out.append(tuple(0.5*((2*p1[k])+(-p0[k]+p2[k])*t+(2*p0[k]-5*p1[k]+4*p2[k]-p3[k])*t2+(-p0[k]+3*p1[k]-3*p2[k]+p3[k])*t3) for k in (0,1)))
    return out+[cp[-1]]
NCP=[(0,-4),(0,25),(4,45),(18,70),(40,95),(55,125),(52,170),(35,230),(30,300),(55,400),(80,520),(60,700),(40,900),(30,1200)]
north=catmull(NCP,12)
west=[(x,0) for x in range(10,-60,-5)]+[(-60-22*math.sin(t/30)-t*.6, t*1.1) for t in range(0,300,6)]
east=[(x,0) for x in range(-4,200,5)]
south=[(0,y) for y in range(-60,0,5)]
for c in (south,east,west,north):
    A(f'<path d="{gpoly(strip(c,6.0))}" fill="#d4c7a6"/>')
# slop: an amoeboid puddle filling the crossroads
pts=[]
for k in range(48):
    a=2*math.pi*k/48; r=1+0.25*math.sin(3*a+0.6)+0.16*math.sin(5*a+2)+0.09*math.sin(9*a)
    pts.append((math.cos(a)*3.6*r, math.sin(a)*3.4*r))
A(f'<path d="{gpoly(pts)}" fill="#8f8748" opacity=".95"/>')
A(f'<path d="{gpoly(pts)}" fill="none" stroke="#5e5630" stroke-width=".8" opacity=".6"/>')
for (x,y,r) in [(4.6,1.2,.35),(-4.2,-2.6,.3),(1.5,-4.3,.28)]:
    A(f'<path d="{gpoly([(x+r*math.cos(t),y+r*.8*math.sin(t)) for t in np.linspace(0,6.28,14)])}" fill="#8f8748"/>')
A('</g>')
def shadow(cx,cy,rx,ry,op=.35):
    A(f'<path d="{gpoly([(cx+rx*math.cos(t),cy+ry*math.sin(t)) for t in np.linspace(0,6.28,24)])}" fill="#3d4a2e" opacity="{op}"/>')
A('<g filter="url(#an-wash2)">')
shadow(-9.6,-2.6,3.6,1.3); shadow(9.3,1.0,2.4,1.2); shadow(0.7,-0.5,1.0,.7,.4)
A('</g>')
A(f'<linearGradient id="an-haze" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e9eef0" stop-opacity="0"/><stop offset=".45" stop-color="#e9eef0" stop-opacity=".3"/><stop offset="1" stop-color="#e9eef0" stop-opacity="0"/></linearGradient>')
A(f'<rect x="0" y="{HZ-22:.1f}" width="{W}" height="34" fill="url(#an-haze)"/>')
A(f'<rect width="{W}" height="{H}" filter="url(#an-paper)" opacity=".12"/>')
# ---- sprites (metres, y negative = up), placed by depth ----
S=[]   # (depth, svg)
def sprite(pos, body, scale=1.0, crisp=False):
    c=cam(pos)
    if c[2]<NEAR: return
    x,y=scr(c); k=F/c[2]*scale
    g=f'<g transform="translate({x:.2f} {y:.2f}) scale({k:.3f})">{body}</g>'
    if crisp: g='<g filter="url(#an-crisp)">'+g+'</g>'
    S.append((c[2], g, crisp))
def screen_item(d,svg): S.append((d,svg,False))
def corn_plant(r):
    g=r.choice(["#5f8a3c","#6b9845","#557f35","#74a04c"]); hl="#8fb85d"
    leaves=[]
    for i,(ang,ln) in enumerate([(-150,.42),(-35,.4),(-120,.34),(-60,.36),(-95,.3)]):
        a=math.radians(ang+r.uniform(-12,12)); L=ln*r.uniform(.85,1.15)
        tx,ty=math.cos(a)*L,math.sin(a)*L*0.9-0.05*i
        mx,my=tx*.35,ty*.9-0.06
        leaves.append(f'<path d="M0 {-0.03*i:.2f} Q{mx-.03:.2f} {my:.2f} {tx:.2f} {ty:.2f} Q{mx+.03:.2f} {my+.05:.2f} 0 {-0.03*i+.02:.2f}Z" fill="{hl if i==4 else g}"/>')
    return ''.join(leaves)
_cr=random.Random(9); CORNS=[corn_plant(_cr) for _ in range(12)]
corn_old='<path d="M0 0 V-.42 M0 -.12 q-.16 -.04 -.26 -.2 M0 -.22 q.16 -.04 .26 -.18 M0 -.32 q-.13 -.03 -.2 -.14" fill="none" stroke="#5f8a3c" stroke-width=".03" stroke-linecap="round"/>'
for y in np.arange(-3.9,-9.5,-0.76):           # our field: the last rows before the road
    for x in np.arange(-3.9,-30,-0.7):
        if 2.5<depth((x,y,0))<30: sprite((x+random.uniform(-.1,.1),y,0),random.choice(CORNS))
for y in np.arange(3.9,26,0.76):              # across the side road
    for x in np.arange(-3.9,-50,-0.6 if y<10 else -1.4):
        if depth((x,y,0))<45: sprite((x,y,0),random.choice(CORNS))
soy='<ellipse cx="0" cy="-.12" rx=".2" ry=".12" fill="#6e9447"/>'
for y in np.arange(3.9,24,0.76):
    for x in np.arange(3.9,13.5,0.6): sprite((x,y,0),soy)
def tree(r,h,col):
    b=[f'<path d="M0 0 V{-h*.45:.2f}" stroke="#5e4630" stroke-width="{r*.14:.2f}"/>']
    cy=-h*.6
    for i in range(7):   # shadowed mass
        b.append(f'<circle cx="{random.uniform(-r*.6,r*.6):.2f}" cy="{cy+random.uniform(-r*.3,r*.45):.2f}" r="{random.uniform(r*.5,r*.8):.2f}" fill="{random.choice(["#3f5c33","#48663a","#4f6e3a"])}"/>')
    for i in range(6):   # sunlit tops, up and to the left
        b.append(f'<circle cx="{random.uniform(-r*.65,r*.25):.2f}" cy="{cy+random.uniform(-r*.6,0):.2f}" r="{random.uniform(r*.3,r*.55):.2f}" fill="{random.choice(["#6f9150","#7da05a","#89aa62"])}"/>')
    for i in range(3):
        b.append(f'<circle cx="{random.uniform(-r*.6,0):.2f}" cy="{cy+random.uniform(-r*.75,-r*.3):.2f}" r="{random.uniform(r*.15,r*.28):.2f}" fill="#a3bf74"/>')
    return ''.join(b)
G=["#5b7c42","#6a8b4b","#4f6e3a","#73925a"]
for x in range(-140,-30,7): sprite((x,62+random.uniform(-2,2),0),tree(3.2,9,G))      # shelterbelt
for y in range(70,180,9): sprite((44+random.uniform(-3,3),y,0),tree(3.4,10,G))
for i in range(26):                                                              # wooded draw
    t=i/25; sprite((70+40*math.sin(t*3)+random.uniform(-6,6), 120+t*260,0),tree(5,12,G))
cedar='<path d="M0 0 l-1.4 0 l1.4 -6 l1.4 6z" fill="#3f5e37"/>'
for x in range(-118,-86,4): sprite((x,138,0),cedar)
sprite((-104,130,0),'<path d="M-6 0 V-6 L0 -10.5 L6 -6 V0Z" fill="#b5473a" stroke="#5a5447" stroke-width=".3"/><path d="M-1.6 0 V-3.6 H1.6 V0" fill="#7a2e25"/>')
sprite((-93,132,0),'<rect x="-1.8" y="-14" width="3.6" height="14" rx="1.8" fill="#cfcabb" stroke="#5a5447" stroke-width=".3"/>')
sprite((-84,126,0),'<path d="M-4 0 V-4 L0 -7 L4 -4 V0Z" fill="#f4f0e4" stroke="#5a5447" stroke-width=".3"/>')
cow='<g stroke="#3e3a35" stroke-width=".05"><ellipse cx="0" cy="-1" rx="1.05" ry=".45" fill="#3e3a35"/><ellipse cx="-1.2" cy="-1.15" rx=".32" ry=".24" fill="#3e3a35"/><path d="M-.7 -.6 V0 M-.4 -.6 V0 M.5 -.6 V0 M.8 -.6 V0" stroke-width=".12"/></g>'
for (x,y) in [(22,34),(27,38),(31,33),(36,40)]: sprite((x,y,0),cow)
# poles, wire and the beacon: true 3D
POLES=[(-5,5),(5,-5)]
for (x,y) in POLES:
    a=proj((x,y,0)); b=proj((x,y,7.2)); c1=proj((x-.8,y-.8,6.9)); c2=proj((x+.8,y+.8,6.9)); d=depth((x,y,0))
    screen_item(d, f'<path d="M{a[0]:.1f} {a[1]:.1f} L{b[0]:.1f} {b[1]:.1f}" stroke="#7b5c3c" stroke-width="{max(.6,F*.24/d):.2f}" stroke-linecap="round"/>')
wire=[]
for t in np.linspace(0,1,40):
    x=-5+10*t; y=5-10*t; z=6.9-1.0*(1-(2*t-1)**2)
    if depth((x,y,z))>NEAR: wire.append(proj((x,y,z)))
screen_item(depth((0,0,6)),f'<path d="{path(wire,False)}" fill="none" stroke="#4a4639" stroke-width=".6"/>')
BEACON=(0,0,5.25)
sprite(BEACON,'<path d="M0 -.65 V-.4" stroke="#4a4639" stroke-width=".05"/><rect x="-.26" y="-.42" width=".52" height=".5" rx=".08" fill="#d8ac2a" stroke="#4a4639" stroke-width=".04"/><circle cx="0" cy="-.17" r=".15" fill="#fbeaa0" stroke="#4a4639" stroke-width=".025"/>')
# cones
conesvg='<path d="M-.16 0 L0 -.46 L.16 0Z" fill="#ef7a2a" stroke="#5a5447" stroke-width=".02"/><path d="M-.22 0 H.22" stroke="#c9520f" stroke-width=".06"/><path d="M-.09 -.2 H.09" stroke="#fff6e6" stroke-width=".05"/>'
for p in [(-3.9,1.6,0),(3.6,-2.6,0),(1.8,3.9,0)]: sprite(p,conesvg)
# the pickup, waiting on the side road (facing east), seen from its right side
truck='''<g stroke="#3e3a30" stroke-opacity=".75" stroke-width=".03" stroke-linejoin="round">
 <path d="M-2.7 -.45 V-1.08 H-.3 V-.45Z" fill="#b8473a"/>
 <path d="M-.3 -.45 V-1.82 H.85 L1.42 -1.2 H2.55 Q2.78 -1.15 2.78 -.92 V-.45Z" fill="#c24b3d"/>
 <path d="M-.14 -1.16 V-1.7 H.78 L1.24 -1.16Z" fill="#d6e6ec"/><path d="M.42 -1.7 V-1.16" stroke-width=".04"/>
 <path d="M-2.75 -.5 H2.8" stroke-width=".06"/><circle cx="2.66" cy="-.85" r=".08" fill="#fbeaa0"/>
 <path d="M-2.7 -1.08 H-.3 V-.9 H-2.7Z M-.3 -1.82 H.85 L1.42 -1.2 H2.55 Q2.78 -1.15 2.78 -1.02 H-.3Z" fill="#fff" opacity=".18" stroke="none"/>
 <path d="M-2.7 -.62 H2.78 V-.45 H-2.7Z" fill="#000" opacity=".2" stroke="none"/><path d="M.0 -1.66 L.3 -1.66 L.05 -1.22 L-.1 -1.22Z" fill="#fff" opacity=".6" stroke="none"/>
 <circle cx="-1.8" cy="-.38" r=".38" fill="#2e2e2e"/><circle cx="-1.8" cy="-.38" r=".15" fill="#a9a9a9"/>
 <circle cx="1.8" cy="-.38" r=".38" fill="#2e2e2e"/><circle cx="1.8" cy="-.38" r=".15" fill="#a9a9a9"/></g>'''
TRUCK=(-10.3,-1.6,0); sprite(TRUCK,truck,1.18,True)
bp=proj((-8.6,-1.6,2.6)); BEEP=bp
if GLOW: screen_item(depth(TRUCK)-.1,f'<text x="{bp[0]:.1f}" y="{bp[1]:.1f}" font-size="7" font-family="Georgia, serif" font-style="italic" fill="#4a4639">beep!</text>')
# the tractor, waiting on the lane north of the crossroads, facing south
tractor='''<g stroke="#4a4639" stroke-width=".04" stroke-linejoin="round">
 <path d="M-1.7 -.7 H.3 V-1.45 H-1.55Z" fill="#5f8f4e"/><path d="M-1.1 -1.45 V-2.1" stroke-width=".1"/>
 <path d="M.2 -1.25 V-2.55 H1.45 V-1.25" fill="#d6e6ec" fill-opacity=".7"/><path d="M.1 -2.6 H1.6" stroke-width=".1"/>
 <circle cx=".95" cy="-.78" r=".78" fill="#333"/><circle cx=".95" cy="-.78" r=".3" fill="#e0b93a"/>
 <circle cx="-1.25" cy="-.42" r=".42" fill="#333"/><circle cx="-1.25" cy="-.42" r=".16" fill="#e0b93a"/>
 <path d="M-1.7 -1.45 H.3 V-1.25 H-1.65Z" fill="#fff" opacity=".2" stroke="none"/><path d="M-1.7 -.85 H.3 V-.7 H-1.7Z" fill="#000" opacity=".18" stroke="none"/></g>'''
sprite((15.5,1.7,0),tractor,1.25,True)
# a hobo and a bike tourist heading away up the lane, backs to us
hobo='''<g transform="scale(.08)" stroke="#3e3a30" stroke-width=".7" stroke-linecap="round" stroke-linejoin="round">
 <path d="M-.4 -9 L-3.6 -4.6 L-4.4 0 M.8 -9 L3 -4.4 L5.6 -.6" fill="none" stroke="#4e4234" stroke-width="2"/>
 <path d="M-5.4 .2 h2.4 M4.8 -.4 l2.4 .6" stroke="#2e2a24" stroke-width="1.6"/>
 <path d="M-2.6 -8.4 Q.4 -7.4 3 -8.6 L2.2 -18.2 Q-.4 -19.4 -2.4 -17.8Z" fill="#7a6a52"/>
 <rect x="-1.4" y="-14" width="2.2" height="2.2" fill="#a08a5e" stroke-width=".35"/>
 <circle cx="1.2" cy="-20.6" r="2.3" fill="#c9a786"/><path d="M-1.8 -21.6 h6 M-.4 -21.6 q1.4 -3.4 3.6 0" fill="#4a4036" stroke-width=".9"/>
 <path d="M1.6 -17.2 L4.2 -13.6 L2.6 -17.6" fill="none" stroke="#6b5c46" stroke-width="1.5"/>
 <path d="M3.2 -18.2 L-6.6 -25.4" stroke="#8a6a44" stroke-width=".9"/>
 <path d="M-6.6 -25.4 v1.4" stroke-width=".5"/><circle cx="-7.2" cy="-22.4" r="2.5" fill="#c0392b" stroke-width=".5"/>
 <circle cx="-7.9" cy="-23" r=".45" fill="#fff" stroke="none"/><circle cx="-6.5" cy="-21.8" r=".45" fill="#fff" stroke="none"/><circle cx="-7.4" cy="-21.2" r=".4" fill="#fff" stroke="none"/>
 <path d="M-.6 -17.4 L-2 -13.8 L-1 -10.8" fill="none" stroke="#6b5c46" stroke-width="1.5"/></g>'''
cyclist='''<g transform="scale(.075)" stroke="#3e3a30" stroke-width=".7" stroke-linecap="round" stroke-linejoin="round" fill="none">
 <circle cx="-7.5" cy="-4.2" r="4.2" stroke-width=".9"/><circle cx="7.5" cy="-4.2" r="4.2" stroke-width=".9"/>
 <path d="M-7.5 -4.2 L-2 -4.2 L4 -11 L-3.4 -11 Z M4 -11 L7.5 -4.2 M-3.4 -11 L-4.2 -13.2 M4 -11 L4.6 -13.6 L7 -13.8 L7.4 -12.6" stroke="#3f6fa0" stroke-width="1"/>
 <path d="M-5.6 -13.4 h3" stroke-width="1.1"/>
 <rect x="-12.4" y="-10.6" width="5" height="4.8" rx="1" fill="#c4622d" stroke-width=".5"/><rect x="-11.6" y="-13.2" width="4" height="2.6" rx=".6" fill="#6a8c4a" stroke-width=".5"/>
 <path d="M-4.2 -13.6 L-1.6 -21.6" stroke="#2f5d8a" stroke-width="3.6"/><path d="M-1.4 -20.6 L5.6 -15" stroke="#2f5d8a" stroke-width="1.8"/>
 <path d="M-3.6 -13.6 L-.6 -9 L-2 -4.4" stroke="#3a3a3a" stroke-width="1.4"/>
 <circle cx="-.6" cy="-23.6" r="2.2" fill="#e9c3a0" stroke-width=".5"/><path d="M-3 -24.2 q2.4 -3.6 5 -.4z" fill="#e8c23a" stroke-width=".5"/></g>'''
sprite((7.5,42,0),'<g transform="scale(-1 1)">'+hobo+'</g>',2.9,True)
# the bike tourist wants to head up the lane after him, but is stuck at the crossroads behind the robot: one foot down
cyc_stop=cyclist.replace('<path d="M-3.6 -13.6 L-.6 -9 L-2 -4.4" stroke="#3a3a3a" stroke-width="1.4"/>','<path d="M-3.6 -13.6 L-.6 -9 L-2 -4.4" stroke="#3a3a3a" stroke-width="1.4"/><path d="M-3.8 -13.4 L-6.2 -6.6 L-5.4 0" stroke="#3a3a3a" stroke-width="1.4"/>')
sprite((1.9,-3.9,0),'<g transform="scale(-.8 1)">'+cyc_stop+'</g>',1.0,True)
# a hot-air balloon drifting over the hills
balloon='''<g stroke="#4a4639" stroke-width=".25">
 <path d="M0 -26 C-11 -26 -12 -12 -5 -6 L-2.2 -2.4 H2.2 L5 -6 C12 -12 11 -26 0 -26Z" fill="#e8c23a"/>
 <path d="M0 -26 C-6 -26 -6.5 -12 -2.6 -6 L-1.2 -2.4 H1.2 L2.6 -6 C6.5 -12 6 -26 0 -26Z" fill="#c0392b"/>
 <path d="M0 -26 C-2 -26 -2.2 -12 -.9 -6 L-.4 -2.4 H.4 L.9 -6 C2.2 -12 2 -26 0 -26Z" fill="#3f6fa0"/>
 <path d="M-11.3 -16 Q0 -13.6 11.3 -16" fill="none" stroke="#f6f0e2" stroke-width=".7" opacity=".8"/>
 <path d="M-2.2 -2.4 L-1.4 0 M2.2 -2.4 L1.4 0" stroke-width=".2"/><rect x="-1.5" y="0" width="3" height="2.2" rx=".3" fill="#9a7448"/></g>'''
sprite((-170,520,150),balloon,3.4)
# the mop-bucket robot in the middle of it all
st=[]; rr=random.Random(3)
for k in range(15):
    a=math.radians(195+k*10.5); ln=rr.uniform(8,13)
    x0=-31+math.cos(a)*1.3; y0=0; x1=x0+math.cos(a)*ln*.9; y1=y0+abs(math.sin(a))*ln*.33+2.4
    st.append(f'M{x0:.1f} {y0:.1f} Q{(x0+x1)/2+rr.uniform(-1.5,1.5):.1f} {(y0+y1)/2+rr.uniform(-1,1.5):.1f} {x1:.1f} {y1:.1f}')
sp=' '.join(st)
robot=f'''<g transform="scale(.026)" stroke="#3a3d42" stroke-width="1.1">
 <circle cx="-13" cy="-1" r="2.6" fill="#444"/><circle cx="13" cy="-1" r="2.6" fill="#444"/><circle cx="-7" cy=".2" r="2.6" fill="#444"/><circle cx="7" cy=".2" r="2.6" fill="#444"/>
 <path d="M-19 -24 H19 L16.5 -4.5 Q16 -2.5 13.5 -2.5 H-13.5 Q-16 -2.5 -16.5 -4.5Z" fill="#f2c230"/>
 <path d="M-20.5 -26 H20.5 V-22 H-20.5Z" fill="#e0aa1c"/>
 <path d="M-18 -26 Q-10 -30 -2 -26.5" fill="#8f8748" stroke-width=".8"/>
 <path d="M-17.5 -9 H17" stroke-width=".7" opacity=".5"/>
 <path d="M0 -26 V-36 H15 V-26" fill="#9aa1aa"/><path d="M2 -31 H13 M2 -28.5 H13" stroke-width=".7"/>
 <path d="M13 -35 L22 -58" stroke="#7d848d" stroke-width="2.2"/><path d="M19.5 -58.5 h5.5" stroke="#3a3d42" stroke-width="2.6"/>
 <path d="M-12 -26 Q-15 -34 -11 -38" fill="none" stroke-width="1.2"/><circle cx="-11" cy="-39.5" r="2.2" fill="#ffd23f"/>
 <ellipse cx="-6" cy="-15.5" rx="3.7" ry="5" fill="#26303b"/><ellipse cx="6" cy="-15.5" rx="3.7" ry="5" fill="#26303b"/>
 <circle cx="-5.4" cy="-18.5" r="1.5" fill="#fff" stroke="none"/><circle cx="6.6" cy="-18.5" r="1.5" fill="#fff" stroke="none"/>
 <circle cx="-7" cy="-13.8" r=".7" fill="#fff" stroke="none"/><circle cx="5" cy="-13.8" r=".7" fill="#fff" stroke="none"/>
 <path d="M-2.2 -7.6 q2.2 -1.6 4.4 0" fill="none" stroke-width=".9"/>
 <ellipse cx="-12" cy="-11" rx="2.2" ry="1.1" fill="#ef8f7a" stroke="none" opacity=".75"/><ellipse cx="12" cy="-11" rx="2.2" ry="1.1" fill="#ef8f7a" stroke="none" opacity=".75"/>
 <path d="M23 -30 q3 -4 2 -7 q-3 2 -2 7z" fill="#a8d8f0" stroke-width=".6"/>
 <path d="M-31 -1 L-10 -50" stroke="#9a7448" stroke-width="2.2"/>
 <path d="M-19 -17 Q-24 -16 -24.2 -18.4" fill="none" stroke="#8f959d" stroke-width="1.8"/><circle cx="-24.3" cy="-18.4" r="1.9" fill="#aeb3ba"/>
 <path d="M19 -20 Q8 -46 -15.4 -37.5" fill="none" stroke="#8f959d" stroke-width="1.8"/><circle cx="-15.4" cy="-37.5" r="1.9" fill="#aeb3ba"/>
 <path d="M-34 -2.5 l6 2.5 l-1.2 2.8 l-6 -2.5z" fill="#7b7f86" stroke-width=".6"/>
 <g fill="none" stroke-linecap="round"><path d="{sp}" stroke="#8b8470" stroke-width="2.6"/><path d="{sp}" stroke="#efe8d3" stroke-width="1.7"/></g></g>'''
sprite((0.3,0.2,0),robot,1.6,True)
# draw far to near; soft pencil for most things, a crisper line for the vehicles and the robot
cur=None
for d,svg,cr in sorted(S,key=lambda t:-t[0]):
    if cr: 
        if cur: A('</g>'); cur=None
        A('<g stroke-linecap="round" stroke-linejoin="round">'+svg+'</g>')
    else:
        if not cur: A('<g filter="url(#an-pencil)" stroke-linecap="round" stroke-linejoin="round">'); cur=True
        A(svg)
if cur: A('</g>')
bx,by=proj((0,0,5.08)); k=F/depth(BEACON)
if GLOW: A(f'<circle class="an-flash" cx="{bx:.1f}" cy="{by:.1f}" r="{k*1.4:.1f}" fill="url(#an-glow)"/><circle class="an-flash" cx="{bx:.1f}" cy="{by:.1f}" r="{k*.15:.2f}" fill="#ffd23f"/>')
A('</svg>')
open('/home/claude/mockups/scene5'+('' if GLOW else '_base')+'.svg','w').write('\n'.join(P))
import json; json.dump({'beep':list(map(float,BEEP)),'beacon':list(map(float,proj((0,0,5.08)))),'k':float(F/depth(BEACON))},open('/home/claude/mockups/beacon.json','w'))
print('truck', proj(TRUCK), 'robot', proj((0,0,0)), 'beacon', proj(BEACON), 'horizon', HZ, 'sprites', len(S))
