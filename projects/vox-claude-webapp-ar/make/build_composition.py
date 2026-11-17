import json, math, os, random
W, H = 1080, 1920
import os as _os
_PROJ = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
ROOT = _os.path.join(_PROJ, "hyperframes")
os.makedirs(f"{ROOT}/compositions", exist_ok=True)

FONTS = ""
LOCAL_FONTS = open(f"{ROOT}/vendor/fonts-local.css", encoding="utf-8").read()

BASE = """
:root{
  --ink:#0B0B0C; --paper:#F4F1EA; --accent:#FFD400; --dim:#4A4A4E; --faint:#1A1A1D;
  --ar:'Cairo',sans-serif; --mono:'JetBrains Mono',monospace;
}
*{margin:0;padding:0;box-sizing:border-box;}
html,body{width:1080px;height:1920px;background:var(--ink);}
.clip{position:absolute;inset:0;width:1080px;height:1920px;background:var(--ink);overflow:hidden;}
#root{position:absolute;inset:0;width:1080px;height:1920px;background:var(--ink);overflow:hidden;}
/* safe area: ~270 top, ~670 bottom, ~65 sides */
.safe{position:absolute;left:65px;top:270px;width:950px;height:980px;}
.ar{font-family:var(--ar);color:var(--paper);direction:rtl;}
.ltr{font-family:var(--mono);direction:ltr;unicode-bidi:isolate;}
.eyebrow{position:absolute;top:0;right:0;font-family:var(--mono);font-size:30px;
  color:#8A8A90;text-transform:none;}
.eyebrow-ar{position:absolute;top:0;right:0;font-family:var(--ar);font-size:32px;
  color:#8A8A90;direction:rtl;font-weight:700;}
.sq{border-radius:0;}
"""

def doc(cid, body, css, script):
    return f"""<!doctype html>
<html lang="ar" dir="rtl">
<head><meta charset="utf-8">{FONTS}
<style>{LOCAL_FONTS}{BASE}{css}</style></head>
<body>
<div id="root" data-composition-id="{cid}" data-width="{W}" data-height="{H}">
{body}
</div>
<script src="vendor/gsap.min.js"></script>
<script>
(function(){{
  var tl = gsap.timeline({{paused:true}});
{script}
  window.__timelines = window.__timelines || {{}};
  window.__timelines["{cid}"] = tl;
}})();
</script>
</body></html>
"""

def words(text, cls, idp):
    return "".join(f'<span class="{cls}" id="{idp}{i}">{w}</span>' for i,w in enumerate(text.split(" ")))

FILES = {}

# ───────────────────────── sc1 — the typed line
t = "كتبتَ سطراً واحداً، ثم انتظرت."
n1 = len(t.split(" "))
FILES["sc1"] = doc("sc1",
 f"""<div class="safe">
  <div class="eyebrow-ar">أنت</div>
  <div class="promptline ar" id="pl" dir="rtl">{words(t,"w","w")}<span class="cursor sq" id="cur"></span></div>
 </div>""",
 """.promptline{position:absolute;top:720px;right:0;width:950px;text-align:right;
   font-size:56px;font-weight:400;line-height:1.6;}
 .w{opacity:0;display:inline-block;margin-left:14px;}
 .cursor{display:inline-block;width:22px;height:48px;background:var(--accent);
   vertical-align:-6px;opacity:0;}""",
 "\n".join([f'  tl.to("#w{i}",{{opacity:1,duration:0.01}},{0.25+i*0.42:.2f});' for i in range(n1)])
 + f'\n  tl.to("#cur",{{opacity:1,duration:0.01}},{0.25+n1*0.42:.2f});'
 + f'\n  tl.to("#cur",{{opacity:0.15,duration:0.3,repeat:5,yoyo:true,ease:"steps(1)"}},{0.25+n1*0.42+0.3:.2f});')

# ───────────────────────── sc2 — the empty box
FILES["sc2"] = doc("sc2",
 """<div class="safe">
  <div class="eyebrow-ar">ما حدث فعلاً</div>
  <div class="hdr ar" id="hdr" dir="rtl">كتبتَ سطراً واحداً، ثم انتظرت.</div>
  <div class="arrow sq" id="arr"></div><div class="ahead" id="ah"></div>
  <div class="box sq" id="box"><span class="boxlab ar">أمر واحد</span><div class="strike sq" id="str"></div></div>
 </div>""",
 """.hdr{position:absolute;top:60px;right:0;width:950px;text-align:right;
   font-size:32px;font-weight:400;color:var(--paper);opacity:0.4;
   font-family:var(--ar);direction:rtl;}
 .arrow{position:absolute;top:470px;right:40px;height:3px;width:0;background:var(--paper);}
 .ahead{position:absolute;top:458px;right:252px;width:0;height:0;opacity:0;
   border-top:14px solid transparent;border-bottom:14px solid transparent;
   border-right:20px solid var(--paper);}
 .box{position:absolute;top:370px;right:300px;width:360px;height:210px;
   border:3px solid var(--paper);opacity:0;display:flex;align-items:center;justify-content:center;}
 .boxlab{font-family:var(--ar);font-size:40px;font-weight:700;color:var(--paper);opacity:0.75;}
 .strike{position:absolute;top:100px;right:-30px;height:9px;width:0;background:var(--accent);
   transform:rotate(6deg);transform-origin:right center;}""",
 """  tl.to("#box",{opacity:1,duration:0.01},0.30);
  tl.to("#arr",{width:220,duration:0.55,ease:"steps(6)"},0.45);
  tl.to("#ah",{opacity:1,duration:0.01},1.00);
  tl.to("#str",{width:420,duration:0.26,ease:"steps(3)"},2.35);""")

# ───────────────────────── sc3 — THE RING (first of two)
cx, cy, R = 475, 520, 330
ang = [-90, 30, 150]
pos = [(cx + R*math.cos(math.radians(a)), cy + R*math.sin(math.radians(a))) for a in ang]
LAB = ["يقرأ", "ينفّذ", "يتحقّق"]
LR = R + 78
lpos = [(cx + LR*math.cos(math.radians(a)), cy + LR*math.sin(math.radians(a))) for a in ang]
seg = []
for i in range(3):
    x1,y1 = pos[i]; x2,y2 = pos[(i+1)%3]
    mx,my = (x1+x2)/2, (y1+y2)/2
    ln = math.hypot(x2-x1, y2-y1)
    rot = math.degrees(math.atan2(y2-y1, x2-x1))
    seg.append((mx,my,ln,rot))

nodes = "".join(f'<div class="node sq" id="nd{i}" style="left:{x-26:.0f}px;top:{y-26:.0f}px"></div>' for i,(x,y) in enumerate(pos))
segs  = "".join(f'<div class="seg sq" id="sg{i}" style="left:{mx:.0f}px;top:{my:.0f}px;'
                f'transform:translate(-50%,-50%) rotate({rot:.2f}deg);--len:{ln:.0f}px"></div>'
                for i,(mx,my,ln,rot) in enumerate(seg))
LTR_ = ["translate(-50%,-115%)","translate(-6%,-20%)","translate(-94%,-20%)"]
labs  = "".join(f'<div class="plab ar" id="lb{i}" style="left:{x:.0f}px;top:{y:.0f}px;'
                f'transform:{LTR_[i]}">{LAB[i]}</div>'
                for i,(x,y) in enumerate(lpos))
FILES["sc3"] = doc("sc3",
 f"""<div class="safe">
  <div class="ringwrap" id="rw">{segs}{nodes}</div>
  {labs}
 </div>""",
 """.ringwrap{position:absolute;inset:0;}
 .node{position:absolute;width:52px;height:52px;background:var(--paper);opacity:0;}
 .seg{position:absolute;height:3px;width:0;background:var(--paper);opacity:0.85;}
 .plab{position:absolute;font-family:var(--ar);
   font-size:46px;font-weight:900;color:var(--paper);opacity:0;direction:rtl;white-space:nowrap;}""",
 "\n".join(
   [f'  tl.to("#nd{i}",{{opacity:1,duration:0.01}},{0.50+i*0.90:.2f});' for i in range(3)] +
   [f'  tl.to("#lb{i}",{{opacity:1,duration:0.01}},{0.60+i*0.90:.2f});' for i in range(3)] +
   [f'  tl.to("#sg{i}",{{width:{seg[i][2]:.0f},duration:0.45,ease:"steps(5)"}},{2.55+i*0.28:.2f});' for i in range(3)] +
   ['  tl.to("#rw",{rotation:360,duration:1.7,ease:"steps(20)",transformOrigin:"475px 520px"},4.05);',
    '  tl.to(["#lb0","#lb1","#lb2"],{opacity:0.18,duration:0.18},3.95);',
    '  tl.to(["#lb0","#lb1","#lb2"],{opacity:1,duration:0.18},5.72);']))

# ───────────────────────── sc4 — the file tree
random.seed(1917)
rows=[]; lit=[2,0,0,0]
ROWN=86
litrows = [21, 34, 52, 67]
for i in range(ROWN):
    indent = random.choice([0,0,40,40,80,120])
    wd = random.randint(190, 760)
    y = 120 + i*20
    isl = i in litrows
    rows.append(f'<div class="row sq{" lit" if isl else ""}" id="rw{i}" '
                f'style="top:{y}px;left:{54+indent}px;width:{wd}px"></div>')
tree = "".join(rows)
sweep_t = {r:(0.55 + 3.5*((120+r*20)/(120+ROWN*20))) for r in litrows}
FILES["sc4"] = doc("sc4",
 f"""<div class="treebleed">{tree}</div>
 <div class="safe"><div class="eyebrow ltr">grep</div></div>
 <div class="sweep sq" id="sw"></div>""",
 """.treebleed{position:absolute;inset:0;}
 .row{position:absolute;height:8px;background:var(--faint);}
 .row.lit{background:var(--accent);opacity:0;height:10px;}
 .sweep{position:absolute;left:0;top:0;width:1080px;height:2px;background:var(--accent);
   opacity:0.9;transform:translateY(-20px);}""",
 "\n".join([f'  tl.fromTo("#sw",{{y:-20}},{{y:1930,duration:3.6,ease:"none"}},0.5);'] +
   [f'  tl.to("#rw{r}",{{opacity:1,duration:0.01}},{sweep_t[r]:.2f});' for r in litrows] +
   ['  tl.to("#sw",{opacity:0,duration:0.01},4.2);']))

# ───────────────────────── sc5 — the diff
DIFF = [("ctx","  const app = express();"),
        ("del","- app.get('/', home);"),
        ("add","+ app.get('/', auth, home);"),
        ("add","+ app.use(session(cfg));"),
        ("del","- // TODO: login"),
        ("add","+ app.post('/login', login);"),
        ("ctx","  app.listen(3000);")]
dl = "".join(f'<div class="dline {k} sq" id="dl{i}"><span class="ltr">{v}</span></div>'
             for i,(k,v) in enumerate(DIFF))
FILES["sc5"] = doc("sc5",
 f"""<div class="safe">
  <div class="eyebrow-ar">يعدّل، لا يقترح</div>
  <div class="diff" data-hold>{dl}</div>
 </div>""",
 """.diff{position:absolute;top:300px;left:0;width:760px;}
 .dline{opacity:0;font-family:var(--mono);font-size:30px;line-height:1.9;
   padding-left:18px;border-left:6px solid transparent;direction:ltr;text-align:left;}
 .dline.add{color:var(--accent);border-left-color:var(--accent);}
 .dline.del{color:var(--dim);text-decoration:line-through;border-left-color:var(--dim);}
 .dline.ctx{color:#9A9AA0;}""",
 "\n".join([f'  tl.to("#dl{i}",{{opacity:1,duration:0.01}},{0.4+i*0.26:.2f});' for i in range(len(DIFF))]))

# ───────────────────────── sc6 — the test bar
FILES["sc6"] = doc("sc6",
 """<div class="safe">
  <div class="eyebrow-ar">أحمر ← أخضر</div>
  <div class="barwrap sq">
    <div class="fill sq red" id="f1"></div>
    <div class="fill sq red" id="f2"></div>
    <div class="fill sq grn" id="f3" data-hold></div>
  </div>
  <div class="ctr ltr" id="c1">1</div>
  <div class="ctr ltr" id="c2">2</div>
  <div class="ctr ltr" id="c3">3</div>
 </div>""",
 """.barwrap{position:absolute;top:450px;left:95px;width:760px;height:64px;
   border:3px solid #2A2A2E;overflow:hidden;}
 .fill{position:absolute;left:0;top:0;height:100%;width:0;}
 .red{background:#E03131;} .grn{background:#2FBF5B;}
 .ctr{position:absolute;top:560px;left:95px;font-family:var(--mono);font-size:34px;
   color:#8A8A90;opacity:0;}
 #c2{left:150px;} #c3{left:205px;}""",
 """  tl.to("#f1",{width:760,duration:0.62,ease:"steps(7)"},0.45);
  tl.to("#c1",{opacity:1,duration:0.01},1.07);
  tl.to("#f1",{opacity:0,duration:0.01},1.35);
  tl.to("#f2",{width:760,duration:0.46,ease:"steps(5)"},1.45);
  tl.to("#c2",{opacity:1,duration:0.01},1.91);
  tl.to("#f2",{opacity:0,duration:0.01},2.15);
  tl.to("#f3",{width:760,duration:0.34,ease:"steps(4)"},2.25);
  tl.to("#c3",{opacity:1,duration:0.01},2.59);""")

# ───────────────────────── sc7 — THE RING, SPLIT (hero)
R7 = 356
pos7 = [(cx + R7*math.cos(math.radians(a)), cy - 60 + R7*math.sin(math.radians(a))) for a in ang]
seg7=[]
for i in range(3):
    x1,y1 = pos7[i]; x2,y2 = pos7[(i+1)%3]
    seg7.append(((x1+x2)/2,(y1+y2)/2, math.hypot(x2-x1,y2-y1), math.degrees(math.atan2(y2-y1,x2-x1))))
nodes7 = "".join(f'<div class="node7 sq" id="n7{i}" style="left:{x-30:.0f}px;top:{y-30:.0f}px"></div>' for i,(x,y) in enumerate(pos7))
segs7  = "".join(f'<div class="seg7 sq" style="left:{mx:.0f}px;top:{my:.0f}px;'
                 f'width:{ln:.0f}px;transform:translate(-50%,-50%) rotate({rot:.2f}deg)"></div>'
                 for (mx,my,ln,rot) in seg7)
mx,my,ln,rot = seg7[2]
FILES["sc7"] = doc("sc7",
 f"""<div class="safe">
  <div class="ring7">{segs7}{nodes7}
    <div class="segfill sq" id="sf" style="left:{mx:.0f}px;top:{my:.0f}px;
      transform:translate(-50%,-50%) rotate({rot:.2f}deg);"></div>
  </div>
  <div class="editorial ar" id="ed" dir="rtl" data-hold>نصف العمل</div>
 </div>""",
 """.ring7{position:absolute;inset:0;}
 .seg7{position:absolute;height:3px;background:var(--paper);opacity:0.85;}
 .node7{position:absolute;width:60px;height:60px;background:var(--paper);}
 .segfill{position:absolute;height:22px;width:0;background:var(--accent);}
 .editorial{position:absolute;top:780px;right:0;width:950px;text-align:center;
   font-family:var(--ar);font-size:104px;font-weight:900;color:var(--paper);opacity:0;}""",
 f"""  tl.to("#sf",{{width:{ln:.0f},duration:0.5,ease:"steps(6)"}},1.15);
  tl.to("#n7{2}",{{scale:1.25,duration:0.01,transformOrigin:"50% 50%"}},1.65);
  tl.to("#ed",{{opacity:1,duration:0.01}},1.95);""")

# ───────────────────────── sc8 — the tally
marks=[]; COLS=10; ROWS=5
for r in range(ROWS):
    for c in range(COLS):
        i=r*COLS+c
        marks.append(f'<div class="tk sq" id="tk{i}" style="left:{40+c*88}px;top:{150+r*120}px"></div>')
tally="".join(marks)
TN=COLS*ROWS
# accelerating stamp times: from 2/s to 8/s
ts=[]; t0=0.30; gap=0.42
for i in range(TN):
    ts.append(t0); gap = max(0.055, gap*0.90); t0 += gap
FILES["sc8"] = doc("sc8",
 f"""<div class="safe">
  <div class="eyebrow-ar">حتى تنتهي المهمة</div>
  <div class="tgrid">{tally}</div>
  <div class="hirow sq" id="hr" data-hold></div>
 </div>""",
 """.tgrid{position:absolute;inset:0;}
 .tk{position:absolute;width:10px;height:86px;background:var(--paper);opacity:0;}
 .hirow{position:absolute;left:28px;top:620px;width:0;height:100px;background:var(--accent);
   opacity:0.22;}""",
 "\n".join([f'  tl.to("#tk{i}",{{opacity:1,duration:0.01}},{ts[i]:.2f});' for i in range(TN)] +
   [f'  tl.to("#hr",{{width:884,duration:0.22,ease:"steps(3)"}},{ts[-1]+0.25:.2f});']))

# ───────────────────────── sc9 — two controls (after the whip)
snaps = "".join(f'<div class="snap sq" id="sp{i}" style="left:{i*16}px;top:{i*-14}px;'
                f'opacity:{1-0.14*i:.2f}"></div>' for i in range(5))
FILES["sc9"] = doc("sc9",
 f"""<div class="whip" id="wp" data-hold>
 <div class="safe">
  <div class="eyebrow-ar">مقاطعة · تعديلات محفوظة</div>
  <div class="key sq" id="ky"><span class="ltr">Esc</span></div>
  <div class="you ar" id="yu" dir="rtl">أنت</div>
  <div class="stack" id="st">{snaps}</div>
 </div></div>""",
 """.whip{position:absolute;inset:0;}
 .key{position:absolute;top:380px;right:40px;width:200px;height:200px;
   border:4px solid var(--paper);display:flex;align-items:center;justify-content:center;
   font-family:var(--mono);font-size:44px;color:var(--paper);}
 .you{position:absolute;top:462px;right:330px;width:120px;text-align:center;
   font-family:var(--ar);font-size:36px;font-weight:700;color:#8A8A90;}
 .stack{position:absolute;top:420px;left:60px;width:300px;height:220px;}
 .snap{position:absolute;width:230px;height:150px;border:3px solid var(--paper);
   background:var(--ink);}""",
 """  tl.fromTo("#wp",{x:1080},{x:0,duration:0.22,ease:"steps(4)"},0);
  tl.to("#ky",{y:12,scale:0.97,duration:0.09,transformOrigin:"50% 50%"},1.6);
  tl.to("#ky",{y:0,scale:1,duration:0.12},1.72);
  tl.to("#st",{x:70,duration:0.5,ease:"steps(6)"},2.1);
  tl.to("#wp",{opacity:0,duration:0.45},7.0);""")

# ───────────────────────── sc10 — the close
c1 = "ليس أمراً واحداً ينفَّذ."
c2 = "حلقة تدور، وأنت فيها."
n_a, n_b = len(c1.split(" ")), len(c2.split(" "))
FILES["sc10"] = doc("sc10",
 f"""<div class="fadein" id="fi" data-hold>
 <div class="safe">
  <div class="cl1 ar" id="cl1" dir="rtl">{words(c1,"a","a")}</div>
  <div class="cl2 ar" id="cl2" dir="rtl">{words(c2,"b","b")}<span class="ringmark sq" id="rm"></span></div>
 </div>
 <div class="wm" id="wm"><span class="ig">◉</span><span class="ltr">a7med.breiki</span></div>
 </div>""",
 """.fadein{position:absolute;inset:0;}
 .cl1{position:absolute;top:300px;right:0;width:950px;text-align:center;
   font-size:76px;font-weight:700;line-height:1.5;color:#B8B5AE;}
 .cl2{position:absolute;top:530px;right:0;width:950px;text-align:center;
   font-size:82px;white-space:nowrap;font-weight:900;line-height:1.5;color:var(--paper);}
 .a,.b{opacity:0;display:inline-block;margin-left:16px;}
 .ringmark{display:inline-block;width:34px;height:34px;border:5px solid var(--accent);
   vertical-align:2px;opacity:0;margin-right:18px;}
 .wm{position:absolute;bottom:420px;left:0;width:1080px;text-align:center;
   font-family:var(--mono);font-size:28px;color:#FFFFFF;opacity:0;}
 .ig{margin-right:12px;}""",
 "\n".join(['  tl.fromTo("#fi",{opacity:0},{opacity:1,duration:0.35,ease:"none"},0);'] +
   [f'  tl.to("#a{i}",{{opacity:1,duration:0.01}},{0.45+i*0.26:.2f});' for i in range(n_a)] +
   [f'  tl.to("#b{i}",{{opacity:1,duration:0.01}},{0.45+n_a*0.26+0.45+i*0.28:.2f});' for i in range(n_b)] +
   [f'  tl.to("#rm",{{opacity:1,duration:0.01}},{0.45+n_a*0.26+0.45+n_b*0.28+0.2:.2f});',
    '  tl.to("#wm",{opacity:0.4,duration:1.2,ease:"none"},3.5);']))

for cid, html in FILES.items():
    open(f"{ROOT}/compositions/{cid}.html","w",encoding="utf-8").write(html)

DUR = {"sc1":4.5,"sc2":4.5,"sc3":6.5,"sc4":6.5,"sc5":6.0,"sc6":7.5,"sc7":6.5,"sc8":5.5,"sc9":7.5,"sc10":5.0}
mounts=[]; t=0.0
for cid in ["sc1","sc2","sc3","sc4","sc5","sc6","sc7","sc8","sc9","sc10"]:
    mounts.append(f'  <div class="clip" id="m-{cid}" data-composition-id="m-{cid}" '
                  f'data-composition-src="compositions/{cid}.html" '
                  f'data-start="{t:g}" data-duration="{DUR[cid]:g}" data-track-index="0"></div>')
    t += DUR[cid]
assert abs(t-60.0) < 1e-6, t

index = f"""<!doctype html>
<html lang="ar" dir="rtl">
<head><meta charset="utf-8">{FONTS}<style>{LOCAL_FONTS}{BASE}</style></head>
<body data-composition-id="root" data-start="0" data-duration="60"
      data-width="{W}" data-height="{H}">
{chr(10).join(mounts)}
  <audio id="score" class="clip" src="assets/score.m4a"
         data-start="0" data-duration="60" data-volume="1"
         data-fade-in="0.35" data-fade-out="0.8" data-track-index="1"></audio>
<script src="vendor/gsap.min.js"></script>
<script>
(function(){{
  var tl = gsap.timeline({{paused:true}});
  tl.to({{}},{{duration:60}},0);
  window.__timelines = window.__timelines || {{}};
  window.__timelines["root"] = tl;
}})();
</script>
</body></html>
"""
open(f"{ROOT}/index.html","w",encoding="utf-8").write(index)

meta = {"name":"vox-claude-webapp-ar","width":W,"height":H,"fps":30,"duration":60,
        "composition":"index.html"}
json.dump(meta, open(f"{ROOT}/meta.json","w"), indent=2)
print("wrote", len(FILES), "sub-compositions + index.html | total", t, "s")
