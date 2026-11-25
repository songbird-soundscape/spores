import math, random
random.seed(11)
W,H=320,160; VY=66
P=[]; A=P.append
def persp(y): return max(0.02,(y-VY)/(160-VY))
# winding lane: straight through the crossroads, then curving off into the hills
def lane_cx(y):
    if y>=92: return 160
    t=(92-y)/(92-(VY+1))
    return 160+30*math.sin(t*math.pi*1.25)*t**0.8
def lane_hw(y): return 1.0+(y-VY)*0.47
def cross_cy(x):
    d=abs(x-160)/160
    return 104-26*d**1.4+2.5*math.sin((x-160)/22)*d
def cross_hw(x): return 0.6+5.4*persp(cross_cy(x))**0.9*1.6
def poly(points): return 'M'+' L'.join(f'{x:.1f} {y:.1f}' for x,y in points)+'Z'
A('''<svg class="an-scene" viewBox="0 0 320 160" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Watercolour of low rolling Nebraska farm country: winding roads meet at a crossroads under a flashing yellow light, where a grey mop-bucket robot mops up a puddle of slop while a pickup and a tractor wait">
<defs>
 <filter id="an-wash" x="-5%" y="-5%" width="110%" height="110%">
  <feTurbulence type="fractalNoise" baseFrequency="0.022" numOctaves="3" seed="7" result="w"/>
  <feDisplacementMap in="SourceGraphic" in2="w" scale="5.5" xChannelSelector="R" yChannelSelector="G" result="d"/>
  <feGaussianBlur in="d" stdDeviation=".9"/>
 </filter>
 <filter id="an-wash2" x="-5%" y="-5%" width="110%" height="110%">
  <feTurbulence type="fractalNoise" baseFrequency="0.03" numOctaves="3" seed="5" result="w"/>
  <feDisplacementMap in="SourceGraphic" in2="w" scale="3.5" xChannelSelector="R" yChannelSelector="G" result="d"/>
  <feGaussianBlur in="d" stdDeviation=".8"/>
 </filter>
 <filter id="an-pencil" x="-5%" y="-5%" width="110%" height="110%">
  <feTurbulence type="fractalNoise" baseFrequency="0.06" numOctaves="2" seed="3" result="w"/>
  <feDisplacementMap in="SourceGraphic" in2="w" scale="1.2" xChannelSelector="R" yChannelSelector="G" result="d"/><feGaussianBlur in="d" stdDeviation=".28"/>
 </filter>
 <filter id="an-paper"><feTurbulence type="fractalNoise" baseFrequency="1.6" numOctaves="1" seed="2"/><feColorMatrix values="0 0 0 0 .55  0 0 0 0 .5  0 0 0 0 .42  0 0 0 -1.2 .9"/></filter>
 <linearGradient id="an-sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#a9c9de"/><stop offset=".55" stop-color="#d6e2e0"/><stop offset="1" stop-color="#f4e6c6"/></linearGradient>
 <radialGradient id="an-glow"><stop offset="0" stop-color="#ffd23f" stop-opacity=".9"/><stop offset="1" stop-color="#ffd23f" stop-opacity="0"/></radialGradient>
</defs>
<rect width="320" height="160" fill="#f6f0e2"/>
<g filter="url(#an-wash)" opacity=".96">
 <rect width="320" height="70" fill="url(#an-sky)"/>
 <ellipse cx="58" cy="20" rx="30" ry="7" fill="#fbf8f0" opacity=".9"/><ellipse cx="80" cy="15" rx="18" ry="6.5" fill="#fbf8f0" opacity=".9"/>
 <ellipse cx="236" cy="28" rx="34" ry="6" fill="#fbf8f0" opacity=".8"/><ellipse cx="258" cy="24" rx="16" ry="5" fill="#fbf8f0" opacity=".8"/>
 <ellipse cx="150" cy="8" rx="40" ry="4" fill="#c5dbe8" opacity=".6"/>
 <path d="M0 60 Q30 55 70 58 Q120 53 170 57 Q230 52 280 56 Q300 55 320 57 V70 H0Z" fill="#a9bdb6"/>
 <path d="M0 65 Q40 60 100 64 Q150 60 200 63 T320 62 V100 H0Z" fill="#b8c886"/>
 <path d="M0 67 Q40 63 84 66 L88 74 Q40 71 0 75Z" fill="#d0bc72"/>
 <path d="M204 63 Q250 60 304 63 L306 69 Q252 66 202 69Z" fill="#a2ba6c"/>
 <path d="M236 71 Q282 68 320 70 V80 Q278 77 240 80Z" fill="#d6c27c"/>
 <path d="M0 78 Q50 74 104 78 L118 88 Q60 84 0 88Z" fill="#a6bf6e"/>
 <path d="M206 82 Q262 78 320 81 V94 Q262 90 210 95Z" fill="#cdb873"/>
 <path d="M0 100 Q160 96 320 100 V160 H0Z" fill="#adc673"/>
 <!-- wooded draws and shelterbelts -->
 <path d="M212 62 Q220 68 216 74 Q208 80 220 87 Q232 94 228 99 Q246 98 244 90 Q238 82 228 77 Q224 69 222 62Z" fill="#5f7f45"/>
 <path d="M22 66 Q60 63 98 66 L98 69 Q60 66 22 69Z" fill="#587a41"/>
 <path d="M252 63 Q282 61 314 63 L314 66 Q282 64 252 66Z" fill="#587a41"/>
 <path d="M96 74 Q104 78 100 85 Q94 92 102 98 L112 98 Q106 91 110 84 Q114 76 106 72Z" fill="#5f7f45"/>
</g>
<g filter="url(#an-wash)">''')
def clump(cx,cy,n,spread,rmin,rmax,cols):
    for _ in range(n):
        A(f'<circle cx="{cx+random.uniform(-spread,spread):.1f}" cy="{cy+random.uniform(-spread*.35,spread*.35):.1f}" r="{random.uniform(rmin,rmax):.1f}" fill="{random.choice(cols)}" opacity=".9"/>')
G=["#5b7c42","#6a8b4b","#4f6e3a","#73925a"]
for x in range(24,98,5): clump(x,66.5,2,2,1.6,2.6,G)
for x in range(254,314,5): clump(x,63.5,2,2,1.3,2.1,G)
for (x,y) in [(216,66),(214,74),(220,82),(228,90),(234,95),(238,90),(226,78)]: clump(x,y,4,5,1.8,3.2,G)
for (x,y) in [(104,76),(100,84),(102,92),(106,97)]: clump(x,y,4,4,1.6,3,G)
for x in range(30,62,4): A(f'<path d="M{x} 78 l2.2 -7 l2.2 7z" fill="#3f5e37" opacity=".9"/>')
A('</g><g filter="url(#an-wash2)">')
# roads painted as washes
L=[];R=[]
ys=[160-i*0.5 for i in range(int((160-(VY+1))/0.5))]
for y in ys: L.append((lane_cx(y)-lane_hw(y),y)); R.append((lane_cx(y)+lane_hw(y),y))
A(f'<path d="{poly(L+R[::-1])}" fill="#d4c7a6" opacity=".95"/>')
T=[];B=[]
for i in range(0,321,2):
    x=i; c=cross_cy(x); h=cross_hw(x); T.append((x,c-h)); B.append((x,c+h))
A(f'<path d="{poly(T+B[::-1])}" fill="#d4c7a6" opacity=".95"/>')
# amoeboid slop puddle
pts=[]
cx0,cy0=158,104.5
for k in range(36):
    a=2*math.pi*k/36
    r=1+0.28*math.sin(3*a+0.6)+0.18*math.sin(5*a+2)+0.1*math.sin(8*a)
    pts.append((cx0+math.cos(a)*25*r, cy0+math.sin(a)*6.2*r))
d='M'+' '.join(f'{x:.1f} {y:.1f}' for x,y in pts[:1])+' '+' '.join(f'Q{pts[k][0]:.1f} {pts[k][1]:.1f} {(pts[k][0]+pts[(k+1)%36][0])/2:.1f} {(pts[k][1]+pts[(k+1)%36][1])/2:.1f}' for k in range(36))+'Z'
A(f'<path d="{d}" fill="#8f8748" opacity=".95"/>')
A(f'<path d="{d}" fill="none" stroke="#5e5630" stroke-width="1" opacity=".6"/>')
A('<ellipse cx="190" cy="108" rx="3" ry="1" fill="#8f8748" opacity=".8"/><ellipse cx="128" cy="101" rx="2.2" ry=".8" fill="#8f8748" opacity=".8"/>')
A('</g>')
# paper grain over the washes
A('<rect width="320" height="160" filter="url(#an-paper)" opacity=".12"/>')
A('<g filter="url(#an-pencil)" stroke-linecap="round" stroke-linejoin="round" stroke="#5a5447">')
# farmstead
A('<path d="M40 82 V75 L46 70 L52 75 V82Z" fill="#b5473a" stroke-width=".5" opacity=".95"/><path d="M44 82 V78 H48 V82" fill="#7a2e25" stroke-width=".3"/>')
A('<rect x="54" y="72" width="4" height="10" rx="2" fill="#cfcabb" stroke-width=".4"/><path d="M62 82 V77 L66 74 L70 77 V82Z" fill="#f4f0e4" stroke-width=".4"/>')
# faint road edges and centre dashes
A(f'<path d="{"M"+" L".join(f"{x:.1f} {y:.1f}" for x,y in L)}" fill="none" stroke-width=".45" opacity=".35"/>')
A(f'<path d="{"M"+" L".join(f"{x:.1f} {y:.1f}" for x,y in R)}" fill="none" stroke-width=".45" opacity=".35"/>')
dash=[]
for y in [y for y in ys if y<92 or y>114]:
    if int(y*2)%9<4: x=lane_cx(y); dash.append(f'M{x:.1f} {y:.1f} l0 -.5')
A(f'<path d="{" ".join(dash)}" stroke="#f0dd96" stroke-width="{.9}" opacity=".9"/>')
# corn rows
VX=160
for side in (-1,1):
    for k in range(1,14):
        ex=160+side*(34+k*15)
        def pt(t):
            y=114+46*t; x=VX+(ex-VX)*(y-VY)/(160-VY); return x,y
        for i in range(6):
            t=(i+0.5)/6; x,y=pt(t)
            if abs(x-160)<lane_hw(y)+3: continue
            h=1.6+4.6*t
            A(f'<path d="M{x:.1f} {y:.1f} v{-h:.1f} M{x:.1f} {y-h*.45:.1f} l{-h*.35:.1f} {-h*.3:.1f} M{x:.1f} {y-h*.65:.1f} l{h*.35:.1f} {-h*.3:.1f}" stroke="#5f8a3c" stroke-width="{.3+.45*t:.2f}" opacity=".8"/>')
# poles, wire, beacon right above the crossroads
A('<path d="M116 104 V24 M204 104 V24" stroke="#7b5c3c" stroke-width="1.7"/><path d="M113 27 H119 M201 27 H207" stroke="#7b5c3c" stroke-width="1.1"/>')
A('<path d="M116 27 Q160 38 204 27" fill="none" stroke-width=".65"/>')
A('<path d="M160 33 V35" stroke-width=".6"/><rect x="154.5" y="35" width="11" height="10" rx="2" fill="#d8ac2a" stroke-width=".7"/><circle cx="160" cy="40" r="3" fill="#fbeaa0" stroke-width=".45"/>')
# vehicles on the curving cross road, sized by distance
def vehicle(x,kind):
    y=cross_cy(x); s=0.55+0.6*persp(y)
    if kind=="pickup":
        A(f'<g stroke-width=".5" transform="translate({x:.1f} {y+2:.1f}) scale({s:.2f})"><path d="M-11 -5 h8 l2 -3 h6 l2 3 h4 v5 h-22z" fill="#b8473a"/><path d="M0 -6.4 h4.6 l1.6 2.4 h-6.2z" fill="#d6e6ec"/><circle cx="-6.5" cy=".4" r="1.9" fill="#3a3a3a"/><circle cx="6.5" cy=".4" r="1.9" fill="#3a3a3a"/></g>')
    else:
        A(f'<g stroke-width=".5" transform="translate({x:.1f} {y+2:.1f}) scale({s:.2f})"><rect x="-6" y="-5" width="12" height="5" rx="1" fill="#5f8f4e"/><rect x="1" y="-10" width="6" height="6" rx="1" fill="#d6e6ec"/><circle cx="4" cy=".5" r="3.2" fill="#3a3a3a"/><circle cx="4" cy=".5" r="1.2" fill="#e0b93a"/><circle cx="-4" cy="1.5" r="2" fill="#3a3a3a"/><path d="M-4 -5 v-3" stroke-width="1"/></g>')
vehicle(96,"pickup"); vehicle(226,"tractor")
A(f'<text x="80" y="{cross_cy(96)-8:.1f}" font-size="5.5" font-family="Georgia, serif" font-style="italic" fill="#5a5447" stroke="none">beep</text>')
for (x,y) in [(262,77),(276,79),(290,76)]:
    A(f'<g stroke-width=".3"><ellipse cx="{x}" cy="{y}" rx="2.3" ry="1.2" fill="#3e3a35"/><ellipse cx="{x-2.5}" cy="{y-.6}" rx=".85" ry=".7" fill="#3e3a35"/><path d="M{x-1.5} {y+1} v1.2 M{x+1.5} {y+1} v1.2"/></g>')
A('<path d="M122 14 q2.5 -2.5 5 0 q2.5 -2.5 5 0 M138 20 q1.8 -1.8 3.6 0 q1.8 -1.8 3.6 0" fill="none" stroke-width=".55"/>')
for (x,y) in [(124,109),(194,104)]:
    A(f'<path d="M{x} {y} l2.2 -7 l2.2 7z" fill="#ef7a2a" stroke-width=".45"/><path d="M{x-1.2} {y} h6.6" stroke="#c9520f" stroke-width="1.1"/><path d="M{x+.9} {y-3.6} h2.6" stroke="#fff6e6" stroke-width=".9"/>')
# a bike tourist and, behind, a hobo with a bindle: both heading away from the whole business, off along the right-hand road
def on_cross(x): return x, cross_cy(x)
x,y=on_cross(300); k=0.5+0.5*persp(y)
A(f'''<g transform="translate({x:.1f} {y+1.5:.1f}) scale({k*.55:.2f})" stroke-width=".9">
 <circle cx="-7" cy="-3.5" r="3.5" fill="none"/><circle cx="7" cy="-3.5" r="3.5" fill="none"/>
 <path d="M-7 -3.5 L-2 -3.5 L3 -9 L-3 -9 Z M3 -9 L7 -3.5 M-3 -9 l-1 -2 M3 -9 l.6 -2 h2" fill="none"/>
 <rect x="-10.5" y="-9" width="4.6" height="4.2" rx="1" fill="#c4622d"/><rect x="-9.8" y="-12" width="3.6" height="2.6" rx=".6" fill="#3f6fa0"/>
 <path d="M-3 -10 l2.2 -7 l4.4 1.6" fill="none" stroke="#3f6fa0" stroke-width="2.2"/>
 <path d="M-2 -11 l1.6 4 l-1 3.4" fill="none" stroke="#3a3a3a" stroke-width="1.2"/>
 <circle cx="-.4" cy="-19.6" r="2.1" fill="#e9c3a0"/><path d="M-2.6 -20.2 q2.2 -3.4 4.6 -.4z" fill="#e8c23a"/></g>''')
x,y=on_cross(268); k=0.5+0.5*persp(y)
A(f'''<g transform="translate({x:.1f} {y+1.5:.1f}) scale({k*.6:.2f})" stroke-width=".9">
 <path d="M-1 0 l1.6 -7 M3 0 l-1.6 -7" stroke="#5a4a3a" stroke-width="1.6"/>
 <path d="M-2.6 -7 q2.8 1.4 5.6 0 l-.4 -9.4 q-2.4 -1.4 -4.8 0z" fill="#7a6a52"/><rect x="-1.6" y="-12" width="2" height="2" fill="#a08a5e" stroke-width=".4"/>
 <circle cx=".6" cy="-18.6" r="2.2" fill="#c9a786"/><path d="M-2.6 -19.8 h6.4 M-1.2 -19.8 q1.8 -3.2 3.8 0" fill="#4a4036" stroke-width=".9"/>
 <path d="M1.6 -15 l-3 -3 l-6 -3" fill="none" stroke="#8a6a44" stroke-width="1"/><circle cx="-8" cy="-21.4" r="2.6" fill="#c0392b" stroke-width=".5"/>
 <circle cx="-8.7" cy="-22" r=".45" fill="#fff" stroke="none"/><circle cx="-7.3" cy="-20.8" r=".45" fill="#fff" stroke="none"/>
 <path d="M2.2 -14.4 l2 5" stroke="#7a6a52" stroke-width="1.1"/></g>''')
# the mop-bucket robot: a classic yellow wringer bucket on castors, scaled to the pickup and tractor
BX,BY,BS=160,108.5,0.5
st=[]
for k in range(15):
    a=math.radians(195+k*10.5); ln=random.uniform(8,13)
    x0=-31+math.cos(a)*1.3; y0=0
    x1=x0+math.cos(a)*ln*.9; y1=y0+abs(math.sin(a))*ln*.33+2.4
    st.append(f'M{x0:.1f} {y0:.1f} Q{(x0+x1)/2+random.uniform(-1.5,1.5):.1f} {(y0+y1)/2+random.uniform(-1,1.5):.1f} {x1:.1f} {y1:.1f}')
sp=' '.join(st)
A(f'''<g stroke="#3a3d42" stroke-width="1.1" transform="translate({BX} {BY}) scale({BS})">
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
 <g fill="none" stroke-linecap="round"><path d="{sp}" stroke="#8b8470" stroke-width="2.6"/><path d="{sp}" stroke="#efe8d3" stroke-width="1.7"/></g>
</g>''')
A('</g>')
A('<circle class="an-flash" cx="160" cy="40" r="11" fill="url(#an-glow)"/><circle class="an-flash" cx="160" cy="40" r="2.6" fill="#ffd23f"/>')
A('</svg>')
open('scene4.svg','w').write('\n'.join(P))
