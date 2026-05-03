from __future__ import annotations

import re
from collections.abc import Callable, Iterator
from dataclasses import dataclass
from typing import Any
from urllib.parse import urljoin

DXSBB_BASE_URL = "https://www.dxsbb.com"
DXSBB_LIST_LINK_SELECTOR = ".listBox a[href^='/news/'], .listBox2news a[href^='/news/']"
DXSBB_NEXT_PAGE_SELECTOR = ".listNav a[href]"


@dataclass(frozen=True)
class DxsbbArticleLink:
    url: str
    title: str


def link_title(link: Any) -> str:
    for selector in ("h3::text", "img::attr(alt)"):
        value = link.css(selector).get()
        if value and value.strip():
            return value.strip()
    return " ".join(part.strip() for part in link.css("::text").getall() if part.strip())


def iter_article_links(
    response: Any,
    *,
    predicate: Callable[[str], bool] | None = None,
) -> Iterator[DxsbbArticleLink]:
    seen_urls: set[str] = set()
    for link in response.css(DXSBB_LIST_LINK_SELECTOR):
        href = link.attrib.get("href", "").strip()
        title = link_title(link)
        if not href or not title or (predicate is not None and not predicate(title)):
            continue

        url = urljoin(DXSBB_BASE_URL, href)
        if url in seen_urls:
            continue
        seen_urls.add(url)
        yield DxsbbArticleLink(url=url, title=title)


def next_list_page_url(response: Any) -> str | None:
    for link in response.css(DXSBB_NEXT_PAGE_SELECTOR):
        href = link.attrib.get("href", "").strip()
        link_text = "".join(link.css("img::attr(alt), ::text").getall())
        if href and "下一页" in link_text:
            return urljoin(DXSBB_BASE_URL, href)
    return None


def normalized_text(node: Any) -> str:
    parts = []
    for text in node.css("::text").getall():
        value = re.sub(r"\s+", " ", text.replace("\xa0", " ")).strip()
        if value:
            parts.append(value)
    return "\n".join(parts)
