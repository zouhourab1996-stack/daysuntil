"""Post-build pass: repair relative links that would 404 (e.g. '../..slug/', variant-relative 'weeks/')."""
import os,re,sys
OUT=sys.argv[1] if len(sys.argv)>1 else os.path.join(os.path.dirname(__file__),'..','docs')
OUT=os.path.abspath(OUT)
def exists(base,href):
    h=href.split('#')[0].split('?')[0]
    if not h: return True
    p=os.path.normpath(os.path.join(base,h))
    return os.path.exists(p) or os.path.exists(os.path.join(p,'index.html'))
fixed=broken=0
for root,_,files in os.walk(OUT):
    for f in files:
        if not f.endswith('.html'): continue
        fp=os.path.join(root,f); t=open(fp,encoding='utf8').read()
        t2=re.sub(r'href="((?:\.\./)*\.\.)(?=[a-z0-9])',r'href="\1/',t)
        def rep(m):
            global broken
            h=m.group(1)
            if re.match(r'(https?:|mailto:|#|/|data:|javascript:)',h) or exists(root,h): return m.group(0)
            for up in ('../','../../'):
                if exists(root,up+h): return f'href="{up}{h}"'
            broken+=1; return m.group(0)
        t2=re.sub(r'href="([^"]*)"',rep,t2)
        if t2!=t: open(fp,'w',encoding='utf8').write(t2); fixed+=1
print(f'fix_links: {fixed} files repaired, {broken} links still unresolved')
