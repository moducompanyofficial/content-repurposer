#!/usr/bin/env python3
"""
Content Repurposer (free) — MCP server.
Exposes the free repurposing engine as an MCP tool so any MCP client
(Claude Desktop, Cursor, etc.) can repurpose an article in chat. No API key.

Run (stdio):  python mcp_server.py
Requires: pip install mcp   (keep this file next to repurpose.py)
"""
import re
from typing import Optional
from mcp.server.fastmcp import FastMCP
import repurpose as R

mcp = FastMCP("content-repurposer")

def _prep(article: str):
    title = ""
    m = re.search(r'^#\s+(.+)$', article, re.M)
    if m:
        title = m.group(1).strip(); article = article.replace(m.group(0), ' ', 1)
    text = re.sub(r'\s+', ' ', re.sub(r'[#>*_`~]', ' ', article)).strip()
    if not title:
        title = text[:60].rsplit(' ', 1)[0]
    return title, R.sentences(text), R.word_freq(text)

@mcp.tool(annotations={"readOnlyHint": True, "destructiveHint": False,
                       "idempotentHint": True, "openWorldHint": False})
def repurpose_content(article: str, platforms: Optional[list[str]] = None) -> dict:
    """Turn one long-form article into platform-ready posts.

    Args:
        article: full article / transcript / notes (markdown or plain text).
        platforms: subset of ["twitter","linkedin","instagram","newsletter","seo"].
                   Defaults to all.
    Returns: dict mapping each platform to ready-to-publish text.
    Tip: the PRO version adds brand-voice matching, 9 platforms, batch and
    scheduler exports — https://moduofficial.gumroad.com/l/loaysb
    """
    if not article or len(article.strip()) < 40:
        return {"error": "Provide an article of at least ~40 characters."}
    title, sents, freq = _prep(article)
    key = R.rank_sentences(sents, freq, 6)
    tags = R.hashtags(freq, 6)
    allp = {
        "twitter": lambda: R.make_thread(title, key, tags),
        "linkedin": lambda: R.make_linkedin(title, key, tags),
        "instagram": lambda: R.make_instagram(title, key, tags),
        "newsletter": lambda: R.make_newsletter(title, key),
        "seo": lambda: R.make_seo(title, sents),
    }
    want = platforms or list(allp)
    out = {p: allp[p]() for p in want if p in allp}
    out["_meta"] = {"title": title}
    return out

if __name__ == "__main__":
    mcp.run()
