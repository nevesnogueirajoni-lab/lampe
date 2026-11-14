const C=D.map((x,i)=>({i,theme:x[0],q:x[1],n:x[2],ref:x[3],sens:x[4]}));
const THEMES=[...new Set(C.map(c=>c.theme))];
const BK=["Genèse","Exode","Lévitique","Nombres","Deutéronome","Josué","Juges","Ruth","1 Samuel","2 Samuel","1 Rois","2 Rois","1 Chroniques","2 Chroniques","Esdras","Néhémie","Esther","Job","Psaume","Proverbes","Ecclésiaste","Chant de Salomon","Isaïe","Jérémie","Lamentations","Ézéchiel","Daniel","Osée","Joël","Amos","Abdias","Jonas","Michée","Nahum","Habacuc","Sophonie","Aggée","Zacharie","Malachie","Matthieu","Marc","Luc","Jean","Actes","Romains","1 Corinthiens","2 Corinthiens","Galates","Éphésiens","Philippiens","Colossiens","1 Thessaloniciens","2 Thessaloniciens","1 Timothée","2 Timothée","Tite","Philémon","Hébreux","Jacques","1 Pierre","2 Pierre","1 Jean","2 Jean","3 Jean","Jude","Révélation"];
const MODES={ou:"Où est-ce écrit ?",quoi:"Que dit ce texte ?",qb:"Question biblique"};
function link(ref){const m=ref.match(/^(.+?) (\d+):(\d+)/);if(!m)return"#";const n=BK.indexOf(m[1])+1;if(!n)return"#";const p=(x,l)=>String(x).padStart(l,"0");return"https://www.jw.org/finder?wtlocale=F&prefer=lang&pub=nwtsty&bible="+p(n,2)+p(m[2],3)+p(m[3],3)}
const $=s=>document.querySelector(s);const esc=t=>String(t).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const sh=a=>{a=a.slice();for(let i=a.length-1;i>0;i--){const j=Math.random()*(i+1)|0;[a[i],a[j]]=[a[j],a[i]]}return a};
const today=()=>{const d=new Date();return d.getFullYear()+"-"+String(d.getMonth()+1).padStart(2,"0")+"-"+String(d.getDate()).padStart(2,"0")};
/* ---------- état ---------- */
let S={};try{S=JSON.parse(localStorage.getItem("txt_s")||"{}")}catch(e){}
function norm(){S.th=S.th||[];S.lv=S.lv||1;S.mode=S.mode||"mix";S.k=S.k||{};S.T=S.T||{};S.H=S.H||{};S.tot=S.tot||0;S.good=S.good||0;S.len=S.len||10;S.L=S.L||{}}
norm();
let DB=null,DOC=null,wTimer=null,writing=false,dirty=false;
function save(){try{localStorage.setItem("txt_s",JSON.stringify(S))}catch(e){}if(DOC){dirty=true;clearTimeout(wTimer);wTimer=setTimeout(flush,1500)}}
async function flush(){if(!DOC||writing||!dirty)return;writing=true;dirty=false;try{await DOC.set({s:JSON.stringify(S),maj:Date.now()})}catch(e){}writing=false;if(dirty)flush()}
(async()=>{try{if(!window.claude)return;const db=await claude.use("db");const user=await claude.use("user");if(!db||!user)return;const id=await user.id();if(!id)return;
 DOC=db.doc("progres/"+id);let done=false;const t=setTimeout(()=>{done=true},10000);
 const snap=await DOC.get();clearTimeout(t);if(done)return;const d=snap&&(snap.data?snap.data():snap);
 if(d&&d.s){const R=JSON.parse(d.s);if((R.tot||0)>=(S.tot||0)){S=R;norm();try{localStorage.setItem("txt_s",JSON.stringify(S))}catch(e){}}else{dirty=true;flush()}}else if(S.tot){dirty=true;flush()}
 $("#sync").textContent="☁️ Progrès sauvegardés sur ton compte";if(!cur&&!LS)view(curView)}catch(e){}})();
/* ---------- statistiques ---------- */
const kk=i=>S.k[i]||[0,0,0];
const mastered=i=>{const k=kk(i);return k[0]>=2&&k[2]>=2};   // k = [bonnes, erreurs, série de bonnes actuelle]
const weak=i=>{const k=kk(i);return k[1]>0&&k[2]<2};
function themeStats(){return THEMES.map(t=>{const cs=C.filter(c=>c.theme===t);let g=0,b=0,m=0,seen=0;cs.forEach(c=>{const k=kk(c.i);g+=k[0];b+=k[1];if(k[0]+k[1])seen++;if(mastered(c.i))m++});return{t,n:cs.length,g,b,m,seen,acc:g+b?g/(g+b):null}})}
function weight(c){const k=kk(c.i);if(!(k[0]+k[1]))return 2;if(weak(c.i))return 4+k[1];if(mastered(c.i))return .4;return 1.2}
function pick(P,avoid){let Q=P.filter(c=>!avoid.has(c.i));if(!Q.length)Q=P;let t=Q.reduce((s,c)=>s+weight(c),0),r=Math.random()*t;for(const c of Q){r-=weight(c);if(r<=0)return c}return Q[0]}
function pool(){if(cur&&cur.only)return C.filter(c=>cur.only.includes(c.i));return C.filter(c=>c.n<=S.lv&&(!S.th.length||S.th.includes(c.theme)))}
function distract(c,key,n){const same=sh(C.filter(x=>x.theme===c.theme&&x[key]!==c[key]&&x.ref!==c.ref));const other=sh(C.filter(x=>x.theme!==c.theme&&x[key]!==c[key]&&x.ref!==c.ref));const out=[],seen=new Set([c[key]]);for(const x of same.concat(other)){if(!seen.has(x[key])){seen.add(x[key]);out.push(x[key])}if(out.length===n)break}return out}
/* ---------- vues ---------- */
let cur=null,curView="cours";
function view(v){curView=v;document.querySelectorAll(".tab").forEach(t=>t.classList.toggle("on",t.dataset.v===v));({cours:cours,jeu:setup,fiches:fiches,stats:stats})[v]();window.scrollTo(0,0)}
document.querySelectorAll(".tab").forEach(t=>t.onclick=()=>{cur=null;LS=null;view(t.dataset.v)});
function filters(){return`<div class="box"><p class="lbl">Thèmes (aucun = tous)</p><div class="chips">${THEMES.map(t=>`<button class="chip ${S.th.includes(t)?"on":""}" data-t="${esc(t)}">${esc(t)}</button>`).join("")}</div>
<p class="lbl" style="margin-top:14px">Niveau</p><div class="row">${[[1,"Incontournables"],[2,"+ Courants"],[3,"Tous"]].map(([n,l])=>`<button class="chip ${S.lv===n?"on":""}" data-lv="${n}">${l}</button>`).join("")}</div></div>`}
function bindF(after){document.querySelectorAll("[data-t]").forEach(b=>b.onclick=()=>{const t=b.dataset.t;S.th=S.th.includes(t)?S.th.filter(x=>x!==t):S.th.concat(t);save();after()});document.querySelectorAll("[data-lv]").forEach(b=>b.onclick=()=>{S.lv=+b.dataset.lv;save();after()})}
function setup(){const P=pool();const wk=C.filter(c=>weak(c.i)).length;
$("#v").innerHTML=(wk?`<div class="box hint"><b>🎯 ${wk} texte${wk>1?"s":""} à revoir</b><br>Une séance ciblée sur tes erreurs t'aidera à les fixer.<button class="big" id="focus" style="background:var(--acc2)">Séance ciblée</button></div>`:"")+filters()+`<div class="box"><p class="lbl">Type de questions</p><div class="row">${[["mix","Mélange"]].concat(Object.entries(MODES)).map(([m,l])=>`<button class="chip ${S.mode===m?"on":""}" data-m="${m}">${l}</button>`).join("")}</div>
<p class="lbl" style="margin-top:14px">Longueur de la séance</p><div class="row">${[10,20,30].map(n=>`<button class="chip ${S.len===n?"on":""}" data-len="${n}">${n} questions</button>`).join("")}</div>
<button class="big" id="go">Commencer (${P.length} textes)</button></div>`;
bindF(setup);document.querySelectorAll("[data-m]").forEach(b=>b.onclick=()=>{S.mode=b.dataset.m;save();setup()});document.querySelectorAll("[data-len]").forEach(b=>b.onclick=()=>{S.len=+b.dataset.len;save();setup()});
$("#go").onclick=()=>start(null);if($("#focus"))$("#focus").onclick=()=>start(C.filter(c=>weak(c.i)).map(c=>c.i))}
function start(only){curView="jeu";document.querySelectorAll(".tab").forEach(t=>t.classList.toggle("on",t.dataset.v==="jeu"));cur={n:0,ok:0,only,seen:new Set(),miss:[],len:only?Math.min(S.len,Math.max(only.length,5)):S.len};ask()}
function ask(){if(cur.n>=cur.len)return bilan();const P=pool();if(!P.length){cur=null;setup();return}const c=pick(P,cur.seen);cur.seen.add(c.i);
let m=S.mode==="mix"?sh(["ou","quoi","qb"])[0]:S.mode;let q,ans,opts;
if(m==="ou"){q=`« ${esc(c.sens)} »<div class="ask">Où est-ce écrit ?</div>`;ans=c.ref;opts=distract(c,"ref",3)}
else if(m==="quoi"){q=`Que dit <b>${esc(c.ref)}</b> en gros ?`;ans=c.sens;opts=distract(c,"sens",3)}
else{q=`${esc(c.q)}<div class="ask">Quel texte y répond ?</div>`;ans=c.ref;const o=sh(C.filter(x=>x.theme!==c.theme&&x.ref!==c.ref));opts=[];const seen=new Set([ans]);for(const x of o){if(!seen.has(x.ref)){seen.add(x.ref);opts.push(x.ref)}if(opts.length===3)break}}
const all=sh(opts.concat(ans));
$("#v").innerHTML=`<div class="box"><div class="bar"><span>${cur.n+1} / ${cur.len}</span><span>✅ ${cur.ok}</span></div><div class="prog"><i style="width:${100*cur.n/cur.len}%"></i></div><div class="theme">${esc(c.theme)} · ${MODES[m]}</div><div class="q">${q}</div>${all.map((o,k)=>`<button class="opt" data-k="${k}">${esc(o)}</button>`).join("")}<div id="fb"></div></div><button class="ghost" id="stop">Arrêter la séance</button>`;
$("#stop").onclick=()=>{cur.n?bilan():(cur=null,view("jeu"))};
document.querySelectorAll(".opt").forEach(b=>b.onclick=()=>{if(b.dataset.done)return;document.querySelectorAll(".opt").forEach(x=>{x.dataset.done=1;if(all[x.dataset.k]===ans)x.classList.add("ok")});const good=all[b.dataset.k]===ans;if(!good)b.classList.add("ko");
const k=kk(c.i).slice();if(good){k[0]++;k[2]=(k[2]||0)+1}else{k[1]++;k[2]=0}S.k[c.i]=k;
const T=S.T[m]||[0,0];good?T[0]++:T[1]++;S.T[m]=T;S.tot++;if(good)S.good++;
const d=today(),h=S.H[d]||[0,0,0];h[0]++;if(good)h[1]++;h[2]=C.filter(x=>mastered(x.i)).length;S.H[d]=h;save();
cur.n++;if(good)cur.ok++;else cur.miss.push(c.i);
$("#fb").innerHTML=`<div class="fb">${good?"<b>Bravo !</b>":'<span class="bad"><b>Pas tout à fait.</b></span>'} <b style="color:var(--ink)">${esc(c.ref)}</b> : ${esc(c.sens)}<br><a class="lk" href="${link(c.ref)}" target="_blank" rel="noopener">Lire le verset ↗</a></div><button class="next" id="nx">${cur.n>=cur.len?"Voir le bilan":"Suivante →"}</button>`;$("#nx").onclick=ask})}
function bilan(){const pc=Math.round(100*cur.ok/Math.max(1,cur.n));const miss=[...new Set(cur.miss)];
$("#v").innerHTML=`<div class="box" style="text-align:center"><div style="font-size:46px">${pc>=80?"🌟":pc>=50?"👍":"💪"}</div><div class="q" style="margin:4px 0">${cur.ok} / ${cur.n} bonnes réponses</div><p class="sub">${pc>=80?"Excellent, continue comme ça !":pc>=50?"Bon travail. Les textes ratés reviendront plus souvent.":"Pas de souci : on retient en répétant. Refais une séance ciblée."}</p></div>
${miss.length?`<div class="box"><p class="lbl">À revoir de cette séance</p>${miss.map(i=>card(C[i])).join("")}</div>`:""}
<button class="big" id="again">Nouvelle séance</button>${miss.length?`<button class="big" id="redo" style="background:var(--acc2)">Revoir mes erreurs</button>`:""}<button class="ghost" id="tostats">Voir mes progrès</button>`;
const only=miss;cur=null;$("#again").onclick=()=>start(null);if($("#redo"))$("#redo").onclick=()=>start(only);$("#tostats").onclick=()=>view("stats")}
function card(c){const k=kk(c.i);return`<div class="card"><a class="r lk" href="${link(c.ref)}" target="_blank" rel="noopener">${esc(c.ref)}</a><span class="lv">${["","★★★","★★","★"][c.n]}</span>${k[0]+k[1]?`<span class="lv">${k[0]}✓ ${k[1]}✗</span>`:""}<div class="s">${esc(c.sens)}</div></div>`}
function fiches(){const P=pool();let h=filters()+`<div class="box">`;let lastT="",lastQ="";for(const c of P){if(c.theme!==lastT){h+=`<h3 style="margin:16px 0 0">${esc(c.theme)}</h3>`;lastT=c.theme;lastQ=""}if(c.q!==lastQ){h+=`<div class="qb">${esc(c.q)}</div>`;lastQ=c.q}h+=card(c)}$("#v").innerHTML=h+`</div>`;bindF(fiches)}
/* ---------- graphiques ---------- */
function lineChart(pts,{max=100,suffix="%",color="var(--acc)",h=150}={}){if(pts.length<1)return"<p class='sub'>Pas encore assez de données.</p>";const W=320,pad=26,n=pts.length;const X=i=>pad+(n===1?(W-pad*2)/2:i*(W-pad*2)/(n-1)),Y=v=>h-20-(v/max)*(h-40);
let grid="";for(let g=0;g<=4;g++){const v=max*g/4,y=Y(v);grid+=`<line x1="${pad}" x2="${W-6}" y1="${y}" y2="${y}" stroke="#eee3d8"/><text x="2" y="${y+4}" font-size="9" fill="#8a7f76">${Math.round(v)}${suffix}</text>`}
const path=pts.map((p,i)=>(i?"L":"M")+X(i)+" "+Y(p.v)).join(" ");const area=path+` L${X(n-1)} ${h-20} L${X(0)} ${h-20} Z`;
const lab=pts.map((p,i)=>(n<=8||i%Math.ceil(n/7)===0||i===n-1)?`<text x="${X(i)}" y="${h-5}" font-size="9" text-anchor="middle" fill="#8a7f76">${p.l}</text>`:"").join("");
return`<svg viewBox="0 0 ${W} ${h}" width="100%">${grid}<path d="${area}" fill="${color}" opacity=".12"/><path d="${path}" fill="none" stroke="${color}" stroke-width="2.5" stroke-linejoin="round"/>${pts.map((p,i)=>`<circle cx="${X(i)}" cy="${Y(p.v)}" r="3.2" fill="${color}"/>`).join("")}${lab}</svg>`}
function stats(){const days=Object.keys(S.H).sort().slice(-30);const fmt=d=>d.slice(8)+"/"+d.slice(5,7);
const acc=days.map(d=>({l:fmt(d),v:Math.round(100*S.H[d][1]/Math.max(1,S.H[d][0]))}));const mast=days.map(d=>({l:fmt(d),v:S.H[d][2]||0}));const vol=days.map(d=>({l:fmt(d),v:S.H[d][0]}));
const TS=themeStats();const tried=TS.filter(t=>t.seen);const nM=C.filter(c=>mastered(c.i)).length;
const order=tried.slice().sort((a,b)=>(a.acc-b.acc)||(a.m/a.n-b.m/b.n));
/* diagnostic */
const diag=[];if(!S.tot)diag.push("Fais ta première séance : l'appli analysera ensuite tes points forts et tes points faibles.");else{
 const ord4=order.filter(t=>t.g+t.b>=4);if(ord4.length){const order=ord4;const w=order[0];if(w.acc<.75)diag.push(`Ton thème le plus difficile : <b>${esc(w.t)}</b> (${Math.round(100*w.acc)} % de réussite).`);const best=order[order.length-1];if(order.length>1&&best.acc>=.8)diag.push(`Ton point fort : <b>${esc(best.t)}</b> (${Math.round(100*best.acc)} %).`)}
 const tm=Object.entries(S.T).filter(([m,t])=>t[0]+t[1]>=5).map(([m,t])=>({m,a:t[0]/(t[0]+t[1])}));if(tm.length>1){tm.sort((a,b)=>a.a-b.a);if(tm[tm.length-1].a-tm[0].a>.15){const lo=tm[0].m;diag.push(lo==="ou"?"Tu comprends bien le sens des textes, mais tu as plus de mal à retrouver <b>où ils sont écrits</b>. Entraîne-toi en mode « Où est-ce écrit ? ».":lo==="quoi"?"Tu situes bien les références, mais tu as plus de mal à te rappeler <b>ce qu'elles disent</b>. Entraîne-toi en mode « Que dit ce texte ? ».":"Tu as plus de mal à choisir <b>le texte qui répond à une question</b> : c'est l'exercice le plus proche de la prédication. Entraîne-toi en mode « Question biblique ».")}}
 if(days.length>=4){const a=days.slice(-3),b=days.slice(-6,-3);const r=ds=>{let n=0,g=0;ds.forEach(d=>{n+=S.H[d][0];g+=S.H[d][1]});return n?g/n:null};const ra=r(a),rb=r(b);if(ra!=null&&rb!=null){if(ra-rb>.05)diag.push(`📈 Tu progresses : ${Math.round(100*rb)} % → ${Math.round(100*ra)} % sur tes derniers jours d'entraînement.`);else if(rb-ra>.05)diag.push(`📉 Petite baisse récente (${Math.round(100*rb)} % → ${Math.round(100*ra)} %) : une séance ciblée t'aidera.`)}}
 const untouched=TS.filter(t=>!t.seen).length;if(untouched)diag.push(`${untouched} thème${untouched>1?"s":""} pas encore essayé${untouched>1?"s":""}.`)}
const wl=C.filter(c=>weak(c.i)).sort((a,b)=>kk(b.i)[1]-kk(a.i)[1]).slice(0,12);
$("#v").innerHTML=`<div class="stat"><div><b>${S.good}</b>bonnes réponses</div><div><b style="color:var(--ko)">${S.tot-S.good}</b>erreurs</div><div><b>${S.tot?Math.round(100*S.good/S.tot):0} %</b>réussite</div><div><b>${nM}</b>maîtrisés</div></div>
<div class="box" style="margin-top:14px"><p class="lbl">Mon bilan</p>${diag.map(d=>`<p class="dg">${d}</p>`).join("")}${wl.length?`<button class="big" id="focus" style="background:var(--acc2)">Séance ciblée sur mes erreurs</button>`:""}</div>
<div class="box"><p class="lbl">Réussite par jour</p>${lineChart(acc)}</div>
<div class="box"><p class="lbl">Textes maîtrisés (sur ${C.length})</p>${lineChart(mast,{max:Math.max(10,Math.ceil(Math.max(1,...mast.map(p=>p.v))/10)*10),suffix:"",color:"var(--ok)"})}<p class="sub" style="margin:6px 0 0">Un texte est maîtrisé après au moins 2 bonnes réponses d'affilée.</p></div>
<div class="box"><p class="lbl">Questions par jour</p>${lineChart(vol,{max:Math.max(10,Math.ceil(Math.max(1,...vol.map(p=>p.v))/10)*10),suffix:"",color:"var(--acc2)"})}</div>
<div class="box"><p class="lbl">Par type de question</p>${Object.entries(MODES).map(([m,l])=>{const t=S.T[m]||[0,0],n=t[0]+t[1],a=n?t[0]/n:0;return`<div class="hb"><div class="hbl"><span>${l}</span><span>${n?t[0]+" ✓ · "+t[1]+" ✗ · "+Math.round(100*a)+" %":"—"}</span></div><div class="hbb"><i style="width:${100*a}%;background:${a>=.8?"var(--ok)":a>=.5?"var(--acc)":"var(--ko)"}"></i></div></div>`}).join("")}</div>
<div class="box"><p class="lbl">Par thème (du plus difficile au plus maîtrisé)</p>${order.concat(TS.filter(t=>!t.seen)).map(t=>`<div class="hb" data-tt="${esc(t.t)}"><div class="hbl"><span>${esc(t.t)}</span><span>${t.acc==null?"pas essayé":t.g+" ✓ · "+t.b+" ✗"+(t.g+t.b>=3?" · "+Math.round(100*t.acc)+" %":" · trop tôt pour juger")}</span></div><div class="hbb"><i style="width:${t.acc==null?0:100*t.acc}%;background:${t.acc==null||t.g+t.b<3?"#cfc6bd":t.acc>=.8?"var(--ok)":t.acc>=.5?"var(--acc)":"var(--ko)"}"></i></div></div>`).join("")}<p class="sub" style="margin:8px 0 0">Touche un thème pour t'entraîner dessus.</p></div>
${wl.length?`<div class="box"><p class="lbl">Textes à revoir en priorité</p>${wl.map(card).join("")}</div>`:""}`;
if($("#focus"))$("#focus").onclick=()=>start(C.filter(c=>weak(c.i)).map(c=>c.i));
document.querySelectorAll("[data-tt]").forEach(e=>e.onclick=()=>{S.th=[e.dataset.tt];S.lv=3;save();start(null)})}
