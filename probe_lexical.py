"""
Exploratory: does a keyword (BM25) signal separate answerable questions from
unanswerable ones better than embedding distance? It does not (see README, "The
Improvement"). For each question it prints the best embedding distance, the top
BM25 score, and the share of the question's words found in the top BM25 chunk.

    python probe_lexical.py
"""
import sys,re; sys.path.insert(0,'.')
import store, questions, stress
from ingest import load_documents
from chunker import split_documents
from rank_bm25 import BM25Okapi
STOP=set("a an the is are of to in on at for and or how what which who where when do does can i my me it there this that with from be as by about much many long".split())
def toks(t): 
    out=[]
    for w in re.findall(r"[a-z0-9$]+", t.lower()):
        if w in STOP: continue
        if len(w)>3 and w.endswith("s") and not w.endswith("ss"): w=w[:-1]
        out.append(w)
    return out
chunks=split_documents(load_documents())
bm=BM25Okapi([toks(c.text) for c in chunks])
def lex(q):
    qt=toks(q); sc=bm.get_scores(qt); i=int(sc.argmax())
    have=set(toks(chunks[i].text)); cov=sum(t in have for t in set(qt))/max(1,len(set(qt)))
    return sc[i],cov,chunks[i].source
groups=[("IN",[x["question"] for x in questions.QUESTIONS]+[q for q,_ in stress.STRESS]),("OUT",questions.OUT_OF_SCOPE+stress.NEAR_MISS)]
for g,qs in groups:
    for q in qs:
        r=store.search(q,top_k=5); s,c,src=lex(q)
        print(f"{g} dist {r[0].distance:.3f}  bm25 {s:5.2f}  cover {c:.2f}  {q}   [{src}]")
