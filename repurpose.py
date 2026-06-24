#!/usr/bin/env python3
"""
Content Repurposer — turn one long-form piece (blog post / transcript / notes)
into a week of platform-ready content.

Works fully OFFLINE (deterministic extractive engine, no API key needed).
Optional --llm mode uses Anthropic API for higher-quality rewrites if
ANTHROPIC_API_KEY is set.

Usage:
    python repurpose.py input.md --out output_dir
    python repurpose.py input.md --out output_dir --llm   # optional, needs API key
"""
import argparse, os, re, csv, json, datetime, math
from collections import Counter

STOP = set("a an the and or but if then else for to of in on at by with from as is are was were be been being this that these those it its it's i you he she we they them his her their our your my me us do does did done have has had not no yes can will would should could may might must about into over under again more most other some such only own same so than too very s t can't don't isn't it's i'm you're we're they're".split())

def read_text(path):
    raw = open(path, encoding="utf-8").read()
    title = ""
    m = re.search(r'^#\s+(.+)$', raw, re.M)
    if m: title = m.group(1).strip()
    # strip markdown
    if m: raw = raw.replace(m.group(0), ' ', 1)  # drop H1 line from body so it doesn't merge
    t = re.sub(r'```.*?```', ' ', raw, flags=re.S)
    t = re.sub(r'!\[.*?\]\(.*?\)', ' ', t)
    t = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', t)
    t = re.sub(r'[#>*_`~]', ' ', t)
    t = re.sub(r'\s+', ' ', t).strip()
    if not title:
        title = t[:60].rsplit(' ',1)[0]
    return title, t

def sentences(text):
    parts = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in parts if len(s.strip()) > 25]

def word_freq(text):
    words = [w for w in re.findall(r"[a-zA-Z][a-zA-Z'-]+", text.lower()) if w not in STOP and len(w) > 2]
    return Counter(words)

def rank_sentences(sents, freq, n):
    scored = []
    for i, s in enumerate(sents):
        ws = re.findall(r"[a-zA-Z][a-zA-Z'-]+", s.lower())
        if not ws: continue
        score = sum(freq.get(w,0) for w in ws) / (len(ws)**0.6)
        scored.append((score, i, s))
    top = sorted(scored, reverse=True)[:n]
    return [s for _,_,s in sorted(top, key=lambda x:x[1])]  # preserve order

def keywords(freq, n=12):
    return [w for w,_ in freq.most_common(n)]

def hashtags(freq, n=8):
    tags = []
    for w,_ in freq.most_common(n*2):
        if len(w) >= 4 and w.isalpha():
            tags.append('#'+''.join(p.capitalize() for p in w.split('-')))
        if len(tags) >= n: break
    return tags

def truncate(s, n):
    if len(s) <= n: return s
    return s[:n-1].rsplit(' ',1)[0] + '…'

# ---------- platform formatters (deterministic) ----------
def make_thread(title, key_sents, tags):
    tweets = []
    tweets.append(f"{truncate(title,200)}\n\nA thread 🧵👇")
    for s in key_sents:
        s = s.strip()
        while len(s) > 270:
            cut = s[:270].rsplit(' ',1)[0]
            tweets.append(cut); s = s[len(cut):].strip()
        tweets.append(s)
    tweets.append("If this helped, repost the first tweet ♻️ and follow for more. "+ ' '.join(tags[:3]))
    n = len(tweets)
    return "\n\n---\n".join(f"{i+1}/{n}  {t}" for i,t in enumerate(tweets))

def make_linkedin(title, key_sents, tags):
    hook = f"{title}\n\nMost teams get this wrong. Here's what actually works:"
    body = "\n\n".join(f"→ {truncate(s,200)}" for s in key_sents[:5])
    cta = "\n\nWhich of these are you missing? Reply below.\n\n" + ' '.join(tags[:4])
    post = f"{hook}\n\n{body}{cta}"
    return truncate(post, 2900)

def make_instagram(title, key_sents, tags):
    cap = f"{truncate(title,120)}\n\n{truncate(key_sents[0],180) if key_sents else ''}\n\nSave this for later 📌\n\n" + ' '.join(tags)
    return truncate(cap, 2100)

def make_newsletter(title, key_sents):
    subject = truncate(title, 60)
    body = f"Subject: {subject}\n\nHi there,\n\n" + " ".join(key_sents[:3]) + "\n\nRead the full piece here: [LINK]\n\n— [YOUR NAME]"
    return body

def make_seo(title, sents):
    meta_title = truncate(title, 60)
    meta_desc = truncate(sents[0] if sents else title, 155)
    return f"SEO Title ({len(meta_title)} chars): {meta_title}\nMeta Description ({len(meta_desc)} chars): {meta_desc}"

def make_calendar(outdir, start=None):
    start = start or datetime.date.today()
    plan = [
        ("X/Twitter thread","twitter_thread.txt","09:00"),
        ("LinkedIn post","linkedin_post.txt","08:30"),
        ("Instagram caption","instagram_caption.txt","12:00"),
        ("Newsletter","newsletter.txt","07:00"),
        ("LinkedIn: repost best point as standalone","-","08:30"),
        ("X: quote-tweet thread w/ new angle","-","09:00"),
        ("Recap carousel / round-up","-","11:00"),
    ]
    rows=[]
    for i,(piece,asset,t) in enumerate(plan):
        d = start + datetime.timedelta(days=i)
        rows.append([d.isoformat(), d.strftime('%a'), t, piece, asset, "Draft"])
    path=os.path.join(outdir,"posting_calendar.csv")
    with open(path,'w',newline='') as f:
        w=csv.writer(f); w.writerow(["Date","Day","Time","Piece","Asset file","Status"]); w.writerows(rows)
    return path

# ---------- optional LLM enhancement ----------
def llm_enhance(title, text):
    import anthropic  # noqa
    client = anthropic.Anthropic()
    prompt = f"""Repurpose this article into: (1) a Twitter/X thread, (2) a LinkedIn post,
(3) an Instagram caption with hashtags, (4) a newsletter blurb, (5) SEO title+meta.
Keep the author's voice. Article:\n\nTITLE: {title}\n\n{text[:6000]}"""
    msg = client.messages.create(model="claude-sonnet-4-6", max_tokens=2000,
        messages=[{"role":"user","content":prompt}])
    return msg.content[0].text

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("--out", default="repurposed")
    ap.add_argument("--llm", action="store_true")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    title, text = read_text(args.input)
    sents = sentences(text)
    freq = word_freq(text)
    key = rank_sentences(sents, freq, 6)
    tags = hashtags(freq)

    if args.llm and os.environ.get("ANTHROPIC_API_KEY"):
        try:
            open(os.path.join(args.out,"llm_output.md"),"w").write(llm_enhance(title,text))
            print("LLM enhancement written to llm_output.md")
        except Exception as e:
            print(f"[llm skipped: {e}]")

    outputs = {
        "twitter_thread.txt": make_thread(title, key, tags),
        "linkedin_post.txt": make_linkedin(title, key, tags),
        "instagram_caption.txt": make_instagram(title, key, tags),
        "newsletter.txt": make_newsletter(title, key),
        "seo_meta.txt": make_seo(title, sents),
    }
    for fn, content in outputs.items():
        open(os.path.join(args.out, fn), "w", encoding="utf-8").write(content)
    cal = make_calendar(args.out)
    summary = {"title": title, "source_words": len(text.split()),
               "key_points": len(key), "keywords": keywords(freq),
               "files": list(outputs)+["posting_calendar.csv"]}
    open(os.path.join(args.out,"summary.json"),"w").write(json.dumps(summary,indent=2,ensure_ascii=False))
    print(f"✓ Repurposed '{title}' → {len(outputs)+1} assets in {args.out}/")
    for f in list(outputs)+[os.path.basename(cal)]: print("  -", f)

if __name__ == "__main__":
    main()
