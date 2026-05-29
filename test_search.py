from typing import Any

from ddg_extension.search import (
    AIModel,
    ImageColor,
    ImageLayout,
    ImageLicense,
    ImageSize,
    ImageType,
    SafeSearch,
    SummaryStyle,
    TimeLimit,
    VideoDuration,
    VideoLicense,
    VideoResolution,
    ai_chat,
    image_search,
    news_search,
    summary_prompt,
    text_search,
    video_search,
)


class FakeDDGS:
    def __init__(self) -> None:
        self.calls: list[tuple[str, dict[str, Any]]] = []

    def __enter__(self) -> "FakeDDGS":
        return self

    def __exit__(self, *_args: object) -> None:
        return None

    def text(self, query: str, **kwargs: Any) -> list[dict[str, Any]]:
        self.calls.append(("text", {"query": query, **kwargs}))
        return [
            {
                "title": "DuckDuckGo",
                "href": "https://duckduckgo.com",
                "body": "Privacy-focused search.",
            }
        ]

    def images(self, query: str, **kwargs: Any) -> list[dict[str, Any]]:
        self.calls.append(("images", {"query": query, **kwargs}))
        return [
            {
                "title": "Duck",
                "image": "https://example.com/duck.jpg",
                "url": "https://example.com",
            }
        ]

    def news(self, query: str, **kwargs: Any) -> list[dict[str, Any]]:
        self.calls.append(("news", {"query": query, **kwargs}))
        return [
            {
                "title": "News",
                "url": "https://example.com/news",
                "source": "Example",
            }
        ]

    def videos(self, query: str, **kwargs: Any) -> list[dict[str, Any]]:
        self.calls.append(("videos", {"query": query, **kwargs}))
        return [
            {
                "title": "Video",
                "content": "https://example.com/video",
                "publisher": "Example",
            }
        ]

    def chat(self, query: str, **kwargs: Any) -> str:
        self.calls.append(("chat", {"query": query, **kwargs}))
        return "AI response"


class FailingDDGS:
    def __enter__(self) -> "FailingDDGS":
        return self

    def __exit__(self, *_args: object) -> None:
        return None

    def text(self, _query: str, **_kwargs: Any) -> list[dict[str, Any]]:
        raise RuntimeError("network unavailable")


def test_text_search_returns_structured_results_and_passes_arguments() -> None:
    fake = FakeDDGS()

    response = text_search(
        "python",
        region="us-en",
        safesearch=SafeSearch.OFF,
        timelimit=TimeLimit.WEEK,
        max_results=3,
        ddgs_factory=lambda: fake,
    )

    assert response == {
        "ok": True,
        "kind": "text",
        "keywords": "python",
        "results": [
            {
                "title": "DuckDuckGo",
                "href": "https://duckduckgo.com",
                "body": "Privacy-focused search.",
            }
        ],
    }
    assert fake.calls == [
        (
            "text",
            {
                "query": "python",
                "region": "us-en",
                "safesearch": "off",
                "timelimit": "w",
                "max_results": 3,
            },
        )
    ]


def test_text_search_infers_result_limit_from_query_when_default_is_used() -> None:
    fake = FakeDDGS()

    response = text_search(
        "give me list of today's AI news with detailed analysis. only show 3 results",
        ddgs_factory=lambda: fake,
    )

    assert response["ok"] is True
    assert response["keywords"] == "give me list of today's AI news with detailed analysis"
    assert fake.calls == [
        (
            "text",
            {
                "query": "give me list of today's AI news with detailed analysis",
                "region": "wt-wt",
                "safesearch": "moderate",
                "timelimit": None,
                "max_results": 3,
            },
        )
    ]


def test_explicit_max_results_overrides_query_limit() -> None:
    fake = FakeDDGS()

    response = text_search(
        "python only show 3 results",
        max_results=5,
        ddgs_factory=lambda: fake,
    )

    assert response["ok"] is True
    assert response["keywords"] == "python only show 3 results"
    assert fake.calls[0][1]["max_results"] == 5


def test_image_search_passes_filter_arguments() -> None:
    fake = FakeDDGS()

    response = image_search(
        "ducks",
        safesearch=SafeSearch.ON,
        timelimit=TimeLimit.DAY,
        size=ImageSize.LARGE,
        color=ImageColor.BLUE,
        type_image=ImageType.PHOTO,
        layout=ImageLayout.WIDE,
        license_image=ImageLicense.PUBLIC,
        max_results=2,
        ddgs_factory=lambda: fake,
    )

    assert response["ok"] is True
    assert response["kind"] == "image"
    assert fake.calls[0] == (
        "images",
        {
            "query": "ducks",
            "region": "wt-wt",
            "safesearch": "on",
            "timelimit": "d",
            "size": "Large",
            "color": "Blue",
            "type_image": "photo",
            "layout": "Wide",
            "license_image": "Public",
            "max_results": 2,
        },
    )


def test_news_search_passes_arguments() -> None:
    fake = FakeDDGS()

    response = news_search(
        "goose",
        region="uk-en",
        safesearch=SafeSearch.MODERATE,
        timelimit=TimeLimit.MONTH,
        max_results=4,
        ddgs_factory=lambda: fake,
    )

    assert response["ok"] is True
    assert fake.calls == [
        (
            "news",
            {
                "query": "goose",
                "region": "uk-en",
                "safesearch": "moderate",
                "timelimit": "m",
                "max_results": 4,
            },
        )
    ]


def test_video_search_passes_filter_arguments() -> None:
    fake = FakeDDGS()

    response = video_search(
        "python tutorial",
        resolution=VideoResolution.HIGH,
        duration=VideoDuration.SHORT,
        license_videos=VideoLicense.YOUTUBE,
        max_results=1,
        ddgs_factory=lambda: fake,
    )

    assert response["ok"] is True
    assert fake.calls[0] == (
        "videos",
        {
            "query": "python tutorial",
            "region": "wt-wt",
            "safesearch": "moderate",
            "timelimit": None,
            "resolution": "high",
            "duration": "short",
            "license_videos": "youtube",
            "max_results": 1,
        },
    )


def test_ai_chat_returns_model_and_response() -> None:
    fake = FakeDDGS()

    response = ai_chat(
        "explain mcp",
        model=AIModel.O3_MINI,
        ddgs_factory=lambda: fake,
    )

    assert response == {
        "ok": True,
        "kind": "ai_chat",
        "keywords": "explain mcp",
        "model": "o3-mini",
        "response": "AI response",
    }
    assert fake.calls == [
        ("chat", {"query": "explain mcp", "model": "o3-mini"})
    ]


def test_summary_prompt_uses_search_results() -> None:
    fake = FakeDDGS()

    prompt = summary_prompt(
        "privacy search",
        style=SummaryStyle.DETAILED,
        ddgs_factory=lambda: fake,
    )

    assert "Please summarize them Give extensive details" in prompt
    assert "Title: DuckDuckGo" in prompt
    assert "URL: https://duckduckgo.com" in prompt
    assert fake.calls == [("text", {"query": "privacy search", "max_results": 10})]


def test_invalid_max_results_returns_error_without_calling_ddgs() -> None:
    fake = FakeDDGS()

    response = text_search("python", max_results=0, ddgs_factory=lambda: fake)

    assert response == {
        "ok": False,
        "kind": "text",
        "error": "max_results must be between 1 and 25",
        "results": [],
    }
    assert fake.calls == []


def test_ddgs_error_returns_structured_failure() -> None:
    response = text_search("python", ddgs_factory=FailingDDGS)

    assert response == {
        "ok": False,
        "kind": "text",
        "error": "Error performing text search: network unavailable",
        "results": [],
    }
