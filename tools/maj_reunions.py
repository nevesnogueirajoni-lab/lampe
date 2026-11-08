#!/usr/bin/env python3
"""Mise à jour du programme des réunions de Lampe depuis wol.jw.org, sans navigateur.

Usage : python3 tools/maj_reunions.py [nb_semaines=20] [--fixtures fichier.json]
Sortie (stdout) : {"maj": "AAAA-MM-JJ", "source": "wol.jw.org", "w": {"2027-5": {...}}, "erreurs": [...]}

Reprend exactement l'extraction de la version qui tournait dans Chrome.
Dépendances : beautifulsoup4 (+ lxml si présent).
"""
import datetime as dt
import json
import re
import sys
import time
import urllib.error
import urllib.request

from bs4 import BeautifulSoup

BASE = "https://wol.jw.org"
ARGS = [a for i, a in enumerate(sys.argv[1:], 1) if not a.startswith("--") and not sys.argv[i - 1].startswith("--")]
NB = int(ARGS[0]) if ARGS else 20
FIX = None
if "--fixtures" in sys.argv:
    FIX = json.load(open(sys.argv[sys.argv.index("--fixtures") + 1], encoding="utf-8"))

try:
    import lxml  # noqa: F401
    PARSER = "lxml"
except ImportError:
    PARSER = "html.parser"


def T(s):
    return re.sub(r"\s+", " ", (s or "").strip())


def get(u):
    if FIX is not None:
        if u not in FIX:
            raise RuntimeError("fixture absente : " + u)
        return FIX[u]
    req = urllib.request.Request(BASE + u, headers={
        "User-Agent": "Mozilla/5.0 (Lampe; mise a jour hebdomadaire)",
        "Accept-Language": "fr",
    })
    for i in range(3):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            if i == 2:
                raise
        except Exception:
            if i == 2:
                raise
        time.sleep(3 * (i + 1))


def doc(u):
    h = get(u)
    return None if h is None else BeautifulSoup(h, PARSER)


N = ['Genèse', 'Exode', 'Lévitique', 'Nombres', 'Deutéronome', 'Josué', 'Juges', 'Ruth', '1 Samuel', '2 Samuel',
     '1 Rois', '2 Rois', '1 Chroniques', '2 Chroniques', 'Esdras', 'Néhémie', 'Esther', 'Job', 'Psaumes', 'Proverbes',
     'Ecclésiaste', 'Chant de Salomon', 'Isaïe', 'Jérémie', 'Lamentations', 'Ézéchiel', 'Daniel', 'Osée', 'Joël',
     'Amos', 'Abdias', 'Jonas', 'Michée', 'Nahum', 'Habacuc', 'Sophonie', 'Aggée', 'Zacharie', 'Malachie', 'Matthieu',
     'Marc', 'Luc', 'Jean', 'Actes', 'Romains', '1 Corinthiens', '2 Corinthiens', 'Galates', 'Éphésiens',
     'Philippiens', 'Colossiens', '1 Thessaloniciens', '2 Thessaloniciens', '1 Timothée', '2 Timothée', 'Tite',
     'Philémon', 'Hébreux', 'Jacques', '1 Pierre', '2 Pierre', '1 Jean', '2 Jean', '3 Jean', 'Jude', 'Révélation']
UP = [n.upper() for n in N]
PN = ".parNum, [data-pnum]"


def weeks(n):
    out, seen, today = [], set(), dt.date.today()
    for i in range(n):
        y, w, _ = (today + dt.timedelta(days=7 * i)).isocalendar()
        if (y, w) not in seen:
            seen.add((y, w))
            out.append((y, w))
    return out


def semaine(y, w):
    d = doc(f"/fr/wol/meetings/r30/lp-f/{y}/{w}")
    if d is None:
        return None
    ls = [(T(a.get_text()), a.get("href") or "") for a in d.find_all("a")]
    ls = [x for x in ls if re.search(r"/wol/d/r30/lp-f/\d+$", x[1])]
    vm = next((x for x in ls if re.search(r"Cahier Vie et ministère", x[0], re.I)), None)
    tg = next((x for x in ls if re.search(r"Tour de Garde \(étude\)", x[0], re.I)), None)
    o = {}
    if vm:
        o["d"] = T(re.sub(r"\s*Cahier Vie et ministère.*$", "", vm[0], flags=re.I))
    if tg:
        o["tg"] = re.sub(r"\s*La Tour de Garde \(étude\).*$", "", tg[0])
        o["tgd"] = tg[1].split("/")[-1]
        td = doc(tg[1])
        ta = td.select_one("#article") if td else None
        if ta:
            o["tgp"] = len(ta.select(PN))
            hs, cur = [], None
            for el in ta.find_all(["h2", "p"]):
                if el.name == "h2":
                    cur = T(el.get_text())
                    continue
                pn = el.select_one(PN)
                if pn and cur:
                    t0, cur = cur, None
                    if "RÉPONDRAIS" not in t0:
                        num = pn.get("data-pnum") or T(pn.get_text())
                        hs.append([t0[:1] + t0[1:].lower(), int(re.sub(r"\D", "", num) or 0)])
            o["tgh"] = hs
    if vm:
        o["vm"] = vm[1].split("/")[-1]
        vd = doc(vm[1])
        a = vd.select_one("#article") if vd else None
        if a:
            H = [T(x.get_text()) for x in a.find_all(["h1", "h2", "h3"])]
            m = re.match(r"^(.+?)\s+(\d+)(?:-(\d+))?$", H[1] if len(H) > 1 else "")
            b = UP.index(m.group(1)) + 1 if m and m.group(1) in UP else 0
            if b > 0:
                o["b"] = b
                o["c"] = list(range(int(m.group(2)), int(m.group(3) or m.group(2)) + 1))
            ji = next((i for i, x in enumerate(H) if x.startswith("JOYAUX")), -1)
            o["j"] = re.sub(r"^1\.\s*", "", H[ji + 1] if 0 <= ji + 1 < len(H) else "")
            pv = []
            for h in a.find_all("h3"):
                H3 = T(h.get_text())
                if not re.match(r"^\d+\.\s", H3):
                    continue
                n, txt = h.find_next_sibling(), ""
                while n is not None and n.name not in ("h1", "h2", "h3") and len(txt) < 400:
                    txt += " " + T(n.get_text())
                    n = n.find_next_sibling()
                txt = re.sub(r"\s*(APPLIQUE-TOI AU MINISTÈRE|VIE CHRÉTIENNE)\b.*$", "", txt)
                txt = re.sub(r"\s*Ta réponse", "", txt).strip()
                mm = re.match(r"^\((\d+) min\)\s*", txt)
                pv.append([int(H3.split(".")[0]), re.sub(r"^\d+\.\s*", "", H3),
                           int(mm.group(1)) if mm else None, (txt[mm.end():] if mm else txt)[:95]])
            o["pv"] = pv
            o["p"] = [x[1] for x in pv if x[0] >= 4 and not x[1].startswith("Étude biblique de l")]
    return o if (o.get("vm") or o.get("tgd")) else None


def main():
    W, err = {}, []
    liste = weeks(NB)
    if "--semaines" in sys.argv:
        liste = [tuple(map(int, k.split("-"))) for k in sys.argv[sys.argv.index("--semaines") + 1].split(",")]
    for y, w in liste:
        try:
            o = semaine(y, w)
            if o:
                W[f"{y}-{w}"] = o
        except Exception as e:  # une semaine en erreur n'arrête pas les autres
            err.append(f"{y}-{w} : {e}")
        if FIX is None:
            time.sleep(0.8)  # politesse envers le site
    print(json.dumps({"maj": dt.date.today().isoformat(), "source": "wol.jw.org", "w": W, "erreurs": err},
                     ensure_ascii=False, separators=(",", ":")))


if __name__ == "__main__":
    main()
