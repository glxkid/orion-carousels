import json,html,re,sys,os
from playwright.sync_api import sync_playwright
D=os.path.dirname(os.path.abspath(__file__))
css=open(D+'/style.css').read()
data=json.load(open(D+'/carousels.json'))
only=sys.argv[1:]
def m(t):
    t=html.escape(t).replace('|','<br>')
    return re.sub(r'\*(.+?)\*',r'<span class="or">\1</span>',t)
def top(i,n): return f'<div class="top"><div class="logo"><div class="ring"></div>Orion</div><div class="num">{i:02d} / {n:02d}</div></div>'
def sw(t): return f'<div class="sowhat"><b>So what</b><span>{m(t)}</span></div>' if t else ''
def slide(s,i,n):
    k=s['type']; h=top(i,n)
    if k=='cover':
        return f'<div class="s" id="s{i}">{h}<div class="main" style="justify-content:flex-start;padding-top:90px"><div class="tag"><i></i>{m(s["tag"])}</div><h1>{m(s["h"])}</h1><p class="lead" style="max-width:860px">{m(s["lead"])}</p></div><div class="swipe">Swipe <div class="arrow">→</div></div></div>'
    if k=='cta':
        return f'<div class="s" id="s{i}">{h}<div class="main"><div class="tag"><i></i>Saw it on Instagram?</div><h2>Get the<br>workflow<br><span class="or">from the reel.</span></h2><p class="lead">Agentic workflows that find your next customers. A person approves everything.</p><div class="row"><span class="pill o" style="font-size:36px;padding:16px 34px">orionagencies.com</span></div></div><div class="sowhat"><b>Follow</b><span>@orion.agencies for AI every week.</span></div></div>'
    body=f'<div class="tag"><i></i>{m(s["tag"])}</div><h2{" style=font-size:96px" if s.get("small") else ""}>{m(s["h"])}</h2>'
    if k=='stats':
        body+='<div class="stats">'+''.join(f'<div class="stat"><div class="v{" or" if j==0 else ""}">{html.escape(v)}</div><div class="l">{m(l)}</div></div>' for j,(v,l) in enumerate(s['stats']))+'</div>'
    if k=='list':
        body+='<div class="items">'+''.join(f'<div class="item"><div class="ic">{html.escape(ic)}</div><div><div class="t">{m(t)}</div><div class="d">{m(d)}</div></div></div>' for ic,t,d in s['items'])+'</div>'
    if s.get('lead'): body+=f'<p class="lead">{m(s["lead"])}</p>'
    if s.get('pills'): body+='<div class="row">'+''.join(f'<span class="pill{" o" if j==0 else ""}">{html.escape(p)}</span>' for j,p in enumerate(s['pills']))+'</div>'
    return f'<div class="s" id="s{i}">{h}<div class="main">{body}</div>{sw(s.get("sowhat"))}</div>'
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1080,'height':1350})
    for c in data:
        if only and c['id'] not in only: continue
        sl=c['slides']+[{'type':'cta'}]; n=len(sl)
        doc=f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body>'+''.join(slide(s,i+1,n) for i,s in enumerate(sl))+'</body></html>'
        od=f'{D}/img/{c["id"]}'; os.makedirs(od,exist_ok=True)
        pg.set_content(doc); pg.wait_for_timeout(300)
        for i in range(n):
            pg.locator(f'#s{i+1}').screenshot(path=f'{od}/{i+1}.jpg',type='jpeg',quality=88)
        print(c['id'],n,'slides')
    b.close()
