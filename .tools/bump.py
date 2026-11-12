#!/usr/bin/env python3
"""Danh so phien ban wiki moi (chay truoc moi lan commit): ghi version.json + hang WIKI_VER trong cac trang
+ gan ?v=<ver> vao moi anh img/*.png -> trinh duyet dang giu ban cu se tu tai lai (xem script WIKI_VER trong <head>)."""
import re, json, time, os, sys
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ver = time.strftime('%Y%m%d%H%M%S')
PAGES = ['index.html', 'bando.html']
SNIP = ("<script>/*wiki-ver*/(function(){var V='%s';function chk(){fetch('version.json?t='+Date.now(),{cache:'no-store'})"
        ".then(function(r){return r.json()}).then(function(j){if(!j||!j.v||j.v===V)return;var k='wikiReload_'+j.v;"
        "try{if(sessionStorage.getItem(k))return;sessionStorage.setItem(k,'1')}catch(e){}"
        "var u=new URL(location.href);u.searchParams.set('v',j.v);location.replace(u.toString())}).catch(function(){})}"
        "chk();document.addEventListener('visibilitychange',function(){if(!document.hidden)chk()});setInterval(chk,300000)})();</script>")
for p in PAGES:
    f = os.path.join(root, p)
    s = open(f, encoding='utf8').read()
    s = re.sub(r"<script>/\*wiki-ver\*/.*?</script>", '', s, flags=re.S)
    s = s.replace('<head>', '<head>\n' + (SNIP % ver), 1)
    s = re.sub(r"(img/[A-Za-z0-9_\-]+\.png)(\?v=[0-9A-Za-z]+)?", lambda m: m.group(1) + '?v=' + ver, s)
    open(f, 'w', encoding='utf8').write(s)
json.dump({'v': ver}, open(os.path.join(root, 'version.json'), 'w'))
print('wiki version', ver)
