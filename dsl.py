import json,glob
D=[];c=None
txt=''.join(open(p,encoding='utf-8').read() for p in sorted(glob.glob('part*.txt')))
for ln in txt.split('\n'):
    if not ln.strip(): continue
    if ln.startswith('=== '): c=dict(id=ln[4:].strip(),slides=[]); D.append(c); continue
    if ln.startswith('caption: '): c['caption']=ln[9:].replace('~','\n'); continue
    if ln.startswith('tags: '): c['tags']=ln[6:]; continue
    f=ln.split(' ;; '); t=f[0]
    if t=='cover': s=dict(type=t,tag=f[1],h=f[2],lead=f[3])
    elif t=='point': s=dict(type=t,tag=f[1],h=f[2],lead=f[3],sowhat=f[4] or None,pills=f[5].split('/') if f[5] else None)
    elif t=='stats': s=dict(type=t,tag=f[1],h=f[2],lead=f[3],sowhat=f[4] or None,stats=[tuple(x.split('=',1)) for x in f[5:]])
    elif t=='list': s=dict(type=t,tag=f[1],h=f[2],sowhat=f[3] or None,lead=f[4] or None,items=[tuple(x.split('=',2)) for x in f[5:]])
    if t=='point' and len(f)>6 and f[6].strip()=='S': s['small']=True
    if c['id']=='c01-ai-weekly-oct9' and len(c['slides'])==3: s['small']=True
    c['slides'].append(s)
json.dump(D,open('carousels.json','w'),ensure_ascii=False)
print(len(D),'carousels')
