import json
cards=json.load(open('versets.json',encoding='utf-8'))
data=json.dumps([[c['theme'],c['question'],c['niveau'],c['ref'],c['sens']] for c in cards],ensure_ascii=False,separators=(',',':'))
css='''
:root{--bg:#fbf7f2;--card:#fff;--ink:#2a2420;--soft:#8a7f76;--acc:#e8875a;--acc2:#6a8caf;--ok:#3f9a6b;--ko:#d0574b;--line:#eee3d8}
*{box-sizing:border-box}body{margin:0;font-family:-apple-system,system-ui,"Segoe UI",sans-serif;background:var(--bg);color:var(--ink)}
.wrap{max-width:560px;margin:0 auto;padding:18px 16px 60px}
h1{font-size:26px;margin:4px 0 2px}.sub{color:var(--soft);margin:0 0 14px;font-size:14px;line-height:1.4}
#sync{font-size:12px;color:var(--soft);margin:-8px 0 12px}
.tabs{display:flex;gap:6px;margin-bottom:14px;flex-wrap:wrap}.tab{border:0;padding:9px 14px;border-radius:999px;background:#fff;color:var(--ink);font-weight:600;box-shadow:0 1px 3px #0001;cursor:pointer;font-size:15px}
.tab.on{background:var(--ink);color:#fff}
.box{background:var(--card);border-radius:20px;padding:18px;box-shadow:0 4px 18px #0000000d;margin-bottom:14px}
.hint{background:#eef3f9}
.lbl{font-size:12px;text-transform:uppercase;letter-spacing:.06em;color:var(--soft);margin:0 0 8px;font-weight:700}
.chips{display:flex;flex-wrap:wrap;gap:6px}.chip{border:1px solid var(--line);background:#fff;border-radius:999px;padding:6px 11px;font-size:13px;cursor:pointer;color:var(--ink)}
.chip.on{background:var(--acc);border-color:var(--acc);color:#fff}
.row{display:flex;gap:6px;flex-wrap:wrap}
.big{width:100%;border:0;border-radius:16px;padding:15px;font-size:17px;font-weight:700;background:var(--acc);color:#fff;cursor:pointer;margin-top:10px}
.ghost{width:100%;border:0;border-radius:14px;padding:12px;font-size:15px;font-weight:600;background:#fff;color:var(--ink);box-shadow:0 1px 3px #0001;cursor:pointer;margin-top:10px}
.q{font-size:19px;line-height:1.4;font-weight:650;margin:6px 0 14px}.ask{font-weight:500;color:var(--soft);margin-top:4px;font-size:16px}
.theme{font-size:11px;color:var(--acc);font-weight:700;text-transform:uppercase;letter-spacing:.05em;margin-top:10px}
.prog{height:6px;background:#f3ebe3;border-radius:6px;overflow:hidden}.prog i{display:block;height:100%;background:var(--acc);border-radius:6px}
.opt{display:block;width:100%;text-align:left;border:2px solid var(--line);background:#fff;border-radius:14px;padding:12px 14px;margin:8px 0;font-size:16px;cursor:pointer;color:var(--ink);line-height:1.35}
.opt.ok{border-color:var(--ok);background:#eaf6ef}.opt.ko{border-color:var(--ko);background:#fbeceb}
.fb{margin-top:10px;font-size:15px;line-height:1.45}.fb b{color:var(--ok)}.fb .bad{color:var(--ko)}
.bar{display:flex;justify-content:space-between;align-items:center;color:var(--soft);font-size:14px;margin-bottom:8px}
a.lk{color:var(--acc2);font-weight:600;text-decoration:none}
.next{border:0;background:var(--ink);color:#fff;border-radius:14px;padding:12px 18px;font-size:16px;font-weight:700;margin-top:12px;cursor:pointer;width:100%}
.card{border-bottom:1px solid var(--line);padding:10px 0}.card:last-child{border:0}.card .r{font-weight:700}.card .s{color:#4d443d;font-size:15px;margin-top:2px}
.lv{display:inline-block;font-size:11px;border-radius:6px;padding:1px 6px;margin-left:6px;background:#f3ebe3;color:var(--soft)}
.qb{font-weight:700;margin:14px 0 4px;color:var(--acc2)}
.stat{display:flex;gap:10px}.stat div{flex:1;background:#fff;border-radius:16px;padding:12px 6px;text-align:center;box-shadow:0 1px 3px #0001;font-size:12px;color:var(--soft)}.stat b{display:block;font-size:22px;color:var(--ink)}
.dg{margin:6px 0;line-height:1.45;font-size:15px}
.hb{margin:10px 0;cursor:pointer}.hbl{display:flex;justify-content:space-between;font-size:14px;gap:8px}.hbl span:last-child{color:var(--soft);white-space:nowrap;font-size:12px}
.hbb{height:9px;background:#f3ebe3;border-radius:6px;overflow:hidden;margin-top:4px}.hbb i{display:block;height:100%;border-radius:6px}
.steps{display:flex;gap:6px;margin-bottom:12px}.steps span{flex:1;text-align:center;font-size:12px;padding:6px 2px;border-radius:999px;background:#f3ebe3;color:var(--soft);font-weight:600}.steps span.on{background:var(--acc);color:#fff}.steps span.done{background:#eaf6ef;color:var(--ok)}
.bigref{font-size:28px;font-weight:800;margin:6px 0 8px;color:var(--ink)}
.tip{background:#fff7e8;border-radius:14px;padding:10px 12px;margin:10px 0;font-size:15px;line-height:1.45}.tip.book{background:#eef3f9}
.flip{min-height:200px;border:2px dashed var(--line);border-radius:18px;padding:18px;cursor:pointer;text-align:center}.flip .tip{text-align:left}.tap{color:var(--soft);font-size:13px;margin-top:18px}
.half{width:auto;flex:1;margin-top:0}.ok2{background:var(--ok)}.ko2{background:#fff;color:var(--ko);border:2px solid var(--ko)}
.les{display:flex;justify-content:space-between;align-items:center;gap:8px;padding:9px 0;border-bottom:1px solid var(--line);cursor:pointer;font-size:15px}.les small{display:block;color:var(--soft);font-size:12px;margin-top:2px}
.peg{display:inline-block;background:#f3ebe3;border-radius:8px;padding:3px 8px;margin:3px 4px 0 0;font-size:13px}
'''
js=open('page.js',encoding='utf-8').read()+'\n'+open('cours.js',encoding='utf-8').read()+'\nview("cours");'
AST={l.split('|',1)[0]:l.split('|',1)[1].strip() for l in open('astuces.txt',encoding='utf-8') if '|' in l}
astj=json.dumps(AST,ensure_ascii=False,separators=(',',':'))
html=f'''<!DOCTYPE html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Textes à retenir</title><style>{css}</style></head><body><div class="wrap">
<h1>📖 Textes à retenir</h1><p class="sub">Retrouve où c'est écrit et ce que ça dit en gros, thème par thème.</p><div id="sync"></div>
<div class="tabs"><button class="tab on" data-v="cours">Cours</button><button class="tab" data-v="jeu">Quiz</button><button class="tab" data-v="fiches">Fiches</button><button class="tab" data-v="stats">Progrès</button></div>
<div id="v"></div></div>
<script>
const D={data};
const AST={astj};
{js}
</script></body></html>'''
open('textes.html','w',encoding='utf-8').write(html);print(len(html))
