from __future__ import annotations

from scrapling.parser import Adaptor

from gaokao_vault.spiders.dxsbb import iter_article_links, link_title, next_list_page_url, normalized_text


def test_iter_article_links_extracts_titles_and_next_page() -> None:
    response = Adaptor(
        content="""
        <div class="listBox">
          <a href="/news/117345.html" target="_blank">
            <div class="b"><h3>2025安徽高考志愿填报时间和截止时间</h3><p class="time">2025-6-12</p></div>
          </a>
          <a href="/news/57188.html" target="_blank">
            <img alt="2025高考志愿填报指南手册" />
          </a>
        </div>
        <div class="listNav"><a href="/news/list_916_2.html"><img alt="下一页" /></a></div>
        """,
        url="https://www.dxsbb.com/news/list_916.html",
    )

    links = list(iter_article_links(response))

    assert [link.title for link in links] == [
        "2025安徽高考志愿填报时间和截止时间",
        "2025高考志愿填报指南手册",
    ]
    assert links[0].url == "https://www.dxsbb.com/news/117345.html"
    assert next_list_page_url(response) == "https://www.dxsbb.com/news/list_916_2.html"


def test_link_title_falls_back_to_visible_text() -> None:
    response = Adaptor(
        content='<a href="/news/1.html">专项计划招生是什么意思</a>',
        url="https://www.dxsbb.com/news/list_976.html",
    )

    assert link_title(response.css("a")[0]) == "专项计划招生是什么意思"


def test_normalized_text_collapses_article_text() -> None:
    response = Adaptor(
        content="""
        <div class="content">
          <p>报名时间: 2026年4月10日至2026年4月30日.</p>
          <p>招生专业: 数学类, 物理学类.</p>
        </div>
        """,
        url="https://www.dxsbb.com/news/70169.html",
    )

    assert normalized_text(response.css(".content")[0]) == (
        "报名时间: 2026年4月10日至2026年4月30日.\n招生专业: 数学类, 物理学类."
    )
