from collections.abc import Callable, Iterable
from enum import Enum
import re
from typing import Any

from ddgs import DDGS


MIN_RESULTS = 1
MAX_RESULTS = 25
DEFAULT_MAX_RESULTS = 10
RESULT_LIMIT_PATTERNS = (
    re.compile(
        r"\b(?:only\s+)?(?:show|return|list)\s+(?P<count>\d{1,2})\s+"
        r"(?:results?|items?|links?)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:top|first|latest)\s+(?P<count>\d{1,2})\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?P<count>\d{1,2})\s+(?:results?|items?|links?)\s*(?:only)?\b",
        re.IGNORECASE,
    ),
)


class SafeSearch(str, Enum):
    ON = "on"
    MODERATE = "moderate"
    OFF = "off"


class TimeLimit(str, Enum):
    DAY = "d"
    WEEK = "w"
    MONTH = "m"
    YEAR = "y"


class ImageSize(str, Enum):
    SMALL = "Small"
    MEDIUM = "Medium"
    LARGE = "Large"
    WALLPAPER = "Wallpaper"


class ImageColor(str, Enum):
    COLOR = "color"
    MONOCHROME = "Monochrome"
    RED = "Red"
    ORANGE = "Orange"
    YELLOW = "Yellow"
    GREEN = "Green"
    BLUE = "Blue"
    PURPLE = "Purple"
    PINK = "Pink"
    BROWN = "Brown"
    BLACK = "Black"
    GRAY = "Gray"
    TEAL = "Teal"
    WHITE = "White"


class ImageType(str, Enum):
    PHOTO = "photo"
    CLIPART = "clipart"
    GIF = "gif"
    TRANSPARENT = "transparent"
    LINE = "line"


class ImageLayout(str, Enum):
    SQUARE = "Square"
    TALL = "Tall"
    WIDE = "Wide"


class ImageLicense(str, Enum):
    ANY = "any"
    PUBLIC = "Public"
    SHARE = "Share"
    SHARE_COMMERCIALLY = "ShareCommercially"
    MODIFY = "Modify"
    MODIFY_COMMERCIALLY = "ModifyCommercially"


class VideoResolution(str, Enum):
    HIGH = "high"
    STANDARD = "standard"


class VideoDuration(str, Enum):
    SHORT = "short"
    MEDIUM = "medium"
    LONG = "long"


class VideoLicense(str, Enum):
    CREATIVE_COMMON = "creativeCommon"
    YOUTUBE = "youtube"


class AIModel(str, Enum):
    GPT_4O_MINI = "gpt-4o-mini"
    LLAMA_3_3_70B = "llama-3.3-70b"
    CLAUDE_3_HAIKU = "claude-3-haiku"
    O3_MINI = "o3-mini"
    MISTRAL_SMALL_3 = "mistral-small-3"


class SummaryStyle(str, Enum):
    BRIEF = "brief"
    DETAILED = "detailed"


SearchResponse = dict[str, Any]
DDGSFactory = Callable[[], Any]


def normalize_search_request(keywords: str, max_results: int) -> tuple[str, int]:
    if max_results != DEFAULT_MAX_RESULTS:
        return keywords, max_results

    for pattern in RESULT_LIMIT_PATTERNS:
        match = pattern.search(keywords)
        if not match:
            continue

        normalized_keywords = pattern.sub("", keywords, count=1)
        normalized_keywords = re.sub(r"\s+", " ", normalized_keywords).strip(" .,")
        return normalized_keywords or keywords, int(match.group("count"))

    return keywords, max_results


def validate_max_results(max_results: int) -> str | None:
    if MIN_RESULTS <= max_results <= MAX_RESULTS:
        return None
    return f"max_results must be between {MIN_RESULTS} and {MAX_RESULTS}"


def success(kind: str, keywords: str, results: Iterable[dict[str, Any]]) -> SearchResponse:
    return {
        "ok": True,
        "kind": kind,
        "keywords": keywords,
        "results": list(results),
    }


def failure(kind: str, message: str) -> SearchResponse:
    return {
        "ok": False,
        "kind": kind,
        "error": message,
        "results": [],
    }


def text_search(
    keywords: str,
    *,
    region: str = "wt-wt",
    safesearch: SafeSearch = SafeSearch.MODERATE,
    timelimit: TimeLimit | None = None,
    max_results: int = 10,
    ddgs_factory: DDGSFactory = DDGS,
) -> SearchResponse:
    keywords, max_results = normalize_search_request(keywords, max_results)
    validation_error = validate_max_results(max_results)
    if validation_error:
        return failure("text", validation_error)

    try:
        with ddgs_factory() as ddgs:
            results = ddgs.text(
                keywords,
                region=region,
                safesearch=safesearch.value,
                timelimit=timelimit.value if timelimit else None,
                max_results=max_results,
            )
        return success("text", keywords, results)
    except Exception as exc:
        return failure("text", f"Error performing text search: {exc}")


def image_search(
    keywords: str,
    *,
    region: str = "wt-wt",
    safesearch: SafeSearch = SafeSearch.MODERATE,
    timelimit: TimeLimit | None = None,
    size: ImageSize | None = None,
    color: ImageColor | None = None,
    type_image: ImageType | None = None,
    layout: ImageLayout | None = None,
    license_image: ImageLicense | None = None,
    max_results: int = 10,
    ddgs_factory: DDGSFactory = DDGS,
) -> SearchResponse:
    keywords, max_results = normalize_search_request(keywords, max_results)
    validation_error = validate_max_results(max_results)
    if validation_error:
        return failure("image", validation_error)

    try:
        with ddgs_factory() as ddgs:
            results = ddgs.images(
                keywords,
                region=region,
                safesearch=safesearch.value,
                timelimit=timelimit.value if timelimit else None,
                size=size.value if size else None,
                color=color.value if color else None,
                type_image=type_image.value if type_image else None,
                layout=layout.value if layout else None,
                license_image=license_image.value if license_image else None,
                max_results=max_results,
            )
        return success("image", keywords, results)
    except Exception as exc:
        return failure("image", f"Error performing image search: {exc}")


def news_search(
    keywords: str,
    *,
    region: str = "wt-wt",
    safesearch: SafeSearch = SafeSearch.MODERATE,
    timelimit: TimeLimit | None = None,
    max_results: int = 10,
    ddgs_factory: DDGSFactory = DDGS,
) -> SearchResponse:
    keywords, max_results = normalize_search_request(keywords, max_results)
    validation_error = validate_max_results(max_results)
    if validation_error:
        return failure("news", validation_error)

    try:
        with ddgs_factory() as ddgs:
            results = ddgs.news(
                keywords,
                region=region,
                safesearch=safesearch.value,
                timelimit=timelimit.value if timelimit else None,
                max_results=max_results,
            )
        return success("news", keywords, results)
    except Exception as exc:
        return failure("news", f"Error performing news search: {exc}")


def video_search(
    keywords: str,
    *,
    region: str = "wt-wt",
    safesearch: SafeSearch = SafeSearch.MODERATE,
    timelimit: TimeLimit | None = None,
    resolution: VideoResolution | None = None,
    duration: VideoDuration | None = None,
    license_videos: VideoLicense | None = None,
    max_results: int = 10,
    ddgs_factory: DDGSFactory = DDGS,
) -> SearchResponse:
    keywords, max_results = normalize_search_request(keywords, max_results)
    validation_error = validate_max_results(max_results)
    if validation_error:
        return failure("video", validation_error)

    try:
        with ddgs_factory() as ddgs:
            results = ddgs.videos(
                keywords,
                region=region,
                safesearch=safesearch.value,
                timelimit=timelimit.value if timelimit else None,
                resolution=resolution.value if resolution else None,
                duration=duration.value if duration else None,
                license_videos=license_videos.value if license_videos else None,
                max_results=max_results,
            )
        return success("video", keywords, results)
    except Exception as exc:
        return failure("video", f"Error performing video search: {exc}")


def ai_chat(
    keywords: str,
    *,
    model: AIModel = AIModel.GPT_4O_MINI,
    ddgs_factory: DDGSFactory = DDGS,
) -> SearchResponse:
    try:
        with ddgs_factory() as ddgs:
            if not hasattr(ddgs, "chat"):
                return failure("ai_chat", "DuckDuckGo AI chat is not supported by ddgs")
            result = ddgs.chat(keywords, model=model.value)
        return {
            "ok": True,
            "kind": "ai_chat",
            "keywords": keywords,
            "model": model.value,
            "response": result,
        }
    except Exception as exc:
        return failure("ai_chat", f"Error during AI chat: {exc}")


def summary_prompt(
    query: str,
    *,
    style: SummaryStyle = SummaryStyle.BRIEF,
    max_results: int = 10,
    ddgs_factory: DDGSFactory = DDGS,
) -> str:
    validation_error = validate_max_results(max_results)
    if validation_error:
        return f"Error generating summary: {validation_error}"

    try:
        with ddgs_factory() as ddgs:
            results = ddgs.text(query, max_results=max_results)
    except Exception as exc:
        return f"Error generating summary: {exc}"

    detail_prompt = " Give extensive details." if style == SummaryStyle.DETAILED else ""
    results_text = "\n\n".join(
        f"Title: {result.get('title', 'No title')}\n"
        f"URL: {result.get('href', 'No URL')}\n"
        f"Description: {result.get('body', 'No description')}"
        for result in results
    )

    return (
        f"Here are the search results for '{query}'. "
        f"Please summarize them{detail_prompt}:\n\n{results_text}"
    )
