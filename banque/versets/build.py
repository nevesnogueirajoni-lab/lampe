import json,re,random,collections,sys
cards=[];theme=q=None
for ln in open('cartes.txt',encoding='utf-8'):
    ln=ln.rstrip('\n')
    if not ln or ln.startswith('# '): continue
    if ln.startswith('## '): theme=ln[3:].strip(); continue
    if ln.startswith('? '): q=ln[2:].strip(); continue
    n,ref,sens=ln.split('|',2)
    cards.append(dict(id=len(cards)+1,theme=theme,question=q,niveau=int(n),ref=ref.strip(),sens=sens.strip()))
json.dump(cards,open('versets.json','w',encoding='utf-8'),ensure_ascii=False,indent=0)
th=collections.Counter(c['theme'] for c in cards); lv=collections.Counter(c['niveau'] for c in cards)
refs=collections.Counter(c['ref'] for c in cards)
print(len(cards),'cartes |',len(th),'thèmes |',len(set(c['question'] for c in cards)),'questions bibliques | niveaux',dict(lv),'| refs uniques',len(refs))
for t,n in th.items(): print(' ',n,t)
