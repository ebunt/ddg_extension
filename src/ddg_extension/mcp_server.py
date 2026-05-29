from mcp.server.fastmcp import FastMCP

from ddg_extension.search import (
    AIModel,
    ImageColor,
    ImageLayout,
    ImageLicense,
    ImageSize,
    ImageType,
    SafeSearch,
    SearchResponse,
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


mcp = FastMCP("ddg-mcp")


@mcp.prompt(name="search-results-summary")
def search_results_summary(
    query: str,
    style: SummaryStyle = SummaryStyle.BRIEF,
) -> str:
    """Create a prompt that asks an LLM to summarize DuckDuckGo results."""
    return summary_prompt(query, style=style)


@mcp.tool(name="ddg-text-search")
def ddg_text_search(
    keywords: str,
    region: str = "wt-wt",
    safesearch: SafeSearch = SafeSearch.MODERATE,
    timelimit: TimeLimit | None = None,
    max_results: int = 10,
) -> SearchResponse:
    """Search the web for text results using DuckDuckGo."""
    return text_search(
        keywords,
        region=region,
        safesearch=safesearch,
        timelimit=timelimit,
        max_results=max_results,
    )


@mcp.tool(name="ddg-image-search")
def ddg_image_search(
    keywords: str,
    region: str = "wt-wt",
    safesearch: SafeSearch = SafeSearch.MODERATE,
    timelimit: TimeLimit | None = None,
    size: ImageSize | None = None,
    color: ImageColor | None = None,
    type_image: ImageType | None = None,
    layout: ImageLayout | None = None,
    license_image: ImageLicense | None = None,
    max_results: int = 10,
) -> SearchResponse:
    """Search the web for images using DuckDuckGo."""
    return image_search(
        keywords,
        region=region,
        safesearch=safesearch,
        timelimit=timelimit,
        size=size,
        color=color,
        type_image=type_image,
        layout=layout,
        license_image=license_image,
        max_results=max_results,
    )


@mcp.tool(name="ddg-news-search")
def ddg_news_search(
    keywords: str,
    region: str = "wt-wt",
    safesearch: SafeSearch = SafeSearch.MODERATE,
    timelimit: TimeLimit | None = None,
    max_results: int = 10,
) -> SearchResponse:
    """Search for news articles using DuckDuckGo."""
    return news_search(
        keywords,
        region=region,
        safesearch=safesearch,
        timelimit=timelimit,
        max_results=max_results,
    )


@mcp.tool(name="ddg-video-search")
def ddg_video_search(
    keywords: str,
    region: str = "wt-wt",
    safesearch: SafeSearch = SafeSearch.MODERATE,
    timelimit: TimeLimit | None = None,
    resolution: VideoResolution | None = None,
    duration: VideoDuration | None = None,
    license_videos: VideoLicense | None = None,
    max_results: int = 10,
) -> SearchResponse:
    """Search for videos using DuckDuckGo."""
    return video_search(
        keywords,
        region=region,
        safesearch=safesearch,
        timelimit=timelimit,
        resolution=resolution,
        duration=duration,
        license_videos=license_videos,
        max_results=max_results,
    )


@mcp.tool(name="ddg-ai-chat")
def ddg_ai_chat(
    keywords: str,
    model: AIModel = AIModel.GPT_4O_MINI,
) -> SearchResponse:
    """Chat with DuckDuckGo AI."""
    return ai_chat(keywords, model=model)


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
