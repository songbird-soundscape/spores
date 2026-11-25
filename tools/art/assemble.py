import json,base64,io,re
from PIL import Image
b=json.load(open('beacon.json'))
im=Image.open('painted.jpg').resize((800,400),Image.LANCZOS); buf=io.BytesIO(); im.save(buf,'JPEG',quality=78,optimize=True,progressive=True)
data=base64.b64encode(buf.getvalue()).decode(); print(len(buf.getvalue())//1024,'KB')
bx,by=b['beacon']; k=b['k']; ex,ey=b['beep']
svg=f'''<svg class="an-scene" viewBox="0 0 320 160" role="img" aria-label="A painting, seen from a cornfield at eye height: a red pickup waits at a country crossroads where a yellow mop-bucket robot mops a puddle of slop under a flashing yellow light; a tractor waits across the way, a hobo and a bike tourist head off up the lane toward low hills, and a hot-air balloon drifts overhead">
<defs><radialGradient id="an-glow"><stop offset="0" stop-color="#ffd23f" stop-opacity=".85"/><stop offset="1" stop-color="#ffd23f" stop-opacity="0"/></radialGradient></defs>
<image href="data:image/jpeg;base64,{data}" width="320" height="160"/>
<text x="{ex:.1f}" y="{ey:.1f}" font-size="7" font-family="Georgia, serif" font-style="italic" fill="#3e3a30">beep!</text>
<circle class="an-flash" cx="{bx:.1f}" cy="{by:.1f}" r="{k*1.4:.1f}" fill="url(#an-glow)"/><circle class="an-flash" cx="{bx:.1f}" cy="{by:.1f}" r="{k*.15:.2f}" fill="#ffe680"/>
</svg>'''
open('scene6.svg','w').write(svg)
s=open('ai-notice.html').read()
arts=list(re.finditer(r'<div class="an-art">.*?</svg>\s*</div>',s,flags=re.S)); assert len(arts)==2
for m,v in reversed(list(zip(arts,[svg,svg.replace('an-glow','an2-glow')]))): s=s[:m.start()]+'<div class="an-art">'+v+'</div>'+s[m.end():]
open('ai-notice.html','w').write(s)
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    br=p.chromium.launch(); pg=br.new_page(viewport={'width':960,'height':480})
    pg.set_content('<html><body style="margin:0">'+svg.replace('<svg ','<svg width="960" height="480" ')+'</body></html>'); pg.wait_for_timeout(500); pg.screenshot(path='scene-large.png'); br.close()
