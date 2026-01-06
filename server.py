"""
Think & Show MCP Server
AI 응답을 시각화하는 MCP 서버
"""

import json
import urllib.parse
import os
import base64
from typing import Optional, Literal

import httpx
from mcp.server.fastmcp import FastMCP


class Config:
    MERMAID_BASE_URL = os.environ.get("MERMAID_BASE_URL", "https://mermaid.ink")
    MERMAID_LIVE_URL = os.environ.get("MERMAID_LIVE_URL", "https://mermaid.live")
    QUICKCHART_URL = os.environ.get("QUICKCHART_URL", "https://quickchart.io/chart")
    QUICKCHART_MAX_URL_LENGTH = int(os.environ.get("QUICKCHART_MAX_URL_LENGTH", "8000"))
    HTTP_TIMEOUT = int(os.environ.get("HTTP_TIMEOUT", "10"))
    DEFAULT_CHART_WIDTH = int(os.environ.get("DEFAULT_CHART_WIDTH", "500"))
    DEFAULT_CHART_HEIGHT = int(os.environ.get("DEFAULT_CHART_HEIGHT", "300"))


CHART_THEMES = {
    "light": {"background": "#ffffff", "font": "#333333", "grid": "rgba(0, 0, 0, 0.1)"},
    "dark": {"background": "#1e1e1e", "font": "#ffffff", "grid": "rgba(255, 255, 255, 0.1)"},
    "kakao": {"background": "#fee500", "font": "#191919", "grid": "rgba(0, 0, 0, 0.1)"}
}

COLOR_PALETTES = {
    "default": [
        "rgba(54, 162, 235, 0.7)", "rgba(255, 99, 132, 0.7)",
        "rgba(75, 192, 192, 0.7)", "rgba(255, 206, 86, 0.7)",
        "rgba(153, 102, 255, 0.7)", "rgba(255, 159, 64, 0.7)",
    ],
    "pastel": [
        "rgba(174, 198, 207, 0.7)", "rgba(255, 179, 186, 0.7)",
        "rgba(186, 255, 201, 0.7)", "rgba(255, 255, 186, 0.7)",
        "rgba(186, 225, 255, 0.7)", "rgba(255, 198, 255, 0.7)",
    ],
    "vibrant": [
        "rgba(0, 123, 255, 0.8)", "rgba(220, 53, 69, 0.8)",
        "rgba(40, 167, 69, 0.8)", "rgba(255, 193, 7, 0.8)",
        "rgba(111, 66, 193, 0.8)", "rgba(253, 126, 20, 0.8)",
    ]
}

TABLE_STYLES = {
    "default": {"header_bg": "#4CAF50", "header_color": "white", "highlight_bg": "#E3F2FD", "border": "#ddd"},
    "dark": {"header_bg": "#333333", "header_color": "white", "highlight_bg": "#444444", "border": "#555555"},
    "kakao": {"header_bg": "#fee500", "header_color": "#191919", "highlight_bg": "#fff9c4", "border": "#e0e0e0"}
}


# Initialize MCP Server
mcp = FastMCP("Think & Show")


def encode_mermaid(diagram: str) -> str:
    return base64.urlsafe_b64encode(diagram.encode()).decode()


def get_color_palette(name: str = "default") -> list[str]:
    return COLOR_PALETTES.get(name, COLOR_PALETTES["default"])


def get_chart_theme(name: str = "light") -> dict:
    return CHART_THEMES.get(name, CHART_THEMES["light"])


def get_table_style(name: str = "default") -> dict:
    return TABLE_STYLES.get(name, TABLE_STYLES["default"])


@mcp.tool()
async def draw_logic_flow(
    diagram_code: str,
    diagram_type: Literal["flowchart", "sequence", "state", "er", "gantt"] = "flowchart",
    theme: Literal["default", "dark", "forest", "neutral"] = "default",
    title: Optional[str] = None
) -> dict:
    """
    프로세스, 코드 로직, 의사결정 흐름을 다이어그램으로 시각화합니다.
    
    Use this tool when explaining processes, system architecture, 
    decision flows, or any step-by-step logic.
    
    Args:
        diagram_code: Mermaid.js syntax diagram code
        diagram_type: Type of diagram (flowchart, sequence, state, er, gantt)
        theme: Visual theme (default, dark, forest, neutral)
        title: Optional title for the diagram
    
    Returns:
        Dictionary with image_url and edit_url for the diagram
    """
    themed_code = f"%%{{init: {{'theme': '{theme}'}}}}%%\n{diagram_code}"
    encoded = encode_mermaid(themed_code)
    
    image_url = f"{Config.MERMAID_BASE_URL}/img/{encoded}"
    edit_url = f"{Config.MERMAID_LIVE_URL}/edit#base64:{encoded}"
    
    async with httpx.AsyncClient(timeout=Config.HTTP_TIMEOUT) as client:
        try:
            response = await client.head(image_url)
            accessible = response.status_code == 200
        except Exception:
            accessible = False
    
    return {
        "success": True,
        "type": "diagram",
        "diagram_type": diagram_type,
        "title": title,
        "image_url": image_url,
        "edit_url": edit_url,
        "accessible": accessible,
        "theme": theme
    }


@mcp.tool()
async def plot_data_chart(
    chart_type: Literal["bar", "line", "pie", "doughnut", "radar", "scatter", "horizontalBar"],
    labels: list[str],
    datasets: list[dict],
    title: Optional[str] = None,
    theme: Literal["light", "dark", "kakao"] = "light",
    color_palette: Literal["default", "pastel", "vibrant"] = "default",
    width: int = 500,
    height: int = 300
) -> dict:
    """
    데이터를 차트로 시각화합니다.
    
    Use this tool for comparing numbers, showing trends over time,
    or displaying proportions and distributions.
    
    Args:
        chart_type: Type of chart (bar, line, pie, doughnut, radar, scatter, horizontalBar)
        labels: X-axis labels list (e.g., ["Jan", "Feb", "Mar"])
        datasets: List of datasets. Each dataset format:
            {"label": "Sales", "data": [100, 150, 200]}
        title: Optional chart title
        theme: Color theme (light, dark, kakao)
        color_palette: Color palette (default, pastel, vibrant)
        width: Image width in pixels
        height: Image height in pixels
    
    Returns:
        Dictionary with image_url for the chart
    """
    theme_config = get_chart_theme(theme)
    colors = get_color_palette(color_palette)
    
    for i, ds in enumerate(datasets):
        if "backgroundColor" not in ds:
            ds["backgroundColor"] = colors[i % len(colors)]
        if "borderColor" not in ds:
            ds["borderColor"] = ds["backgroundColor"].replace("0.7", "1").replace("0.8", "1")
    
    chart_config = {
        "type": chart_type,
        "data": {"labels": labels, "datasets": datasets},
        "options": {
            "responsive": False,
            "plugins": {"legend": {"labels": {"color": theme_config["font"]}}},
            "scales": {} if chart_type in ["pie", "doughnut", "radar"] else {
                "x": {"ticks": {"color": theme_config["font"]}, "grid": {"color": theme_config["grid"]}},
                "y": {"ticks": {"color": theme_config["font"]}, "grid": {"color": theme_config["grid"]}}
            }
        }
    }
    
    if title:
        chart_config["options"]["plugins"]["title"] = {
            "display": True, "text": title, "color": theme_config["font"], "font": {"size": 16}
        }
    
    chart_json = json.dumps(chart_config)
    params = {"c": chart_json, "w": width, "h": height, "bkg": theme_config["background"]}
    chart_url = f"{Config.QUICKCHART_URL}?{urllib.parse.urlencode(params)}"
    
    if len(chart_url) > Config.QUICKCHART_MAX_URL_LENGTH:
        return {"success": False, "error": "Chart data too large. Reduce data points."}
    
    return {
        "success": True,
        "type": "chart",
        "chart_type": chart_type,
        "title": title,
        "image_url": chart_url,
        "theme": theme,
        "dimensions": {"width": width, "height": height}
    }


@mcp.tool()
async def render_mindmap(
    central_topic: str,
    branches: list[dict],
    theme: Literal["default", "dark", "forest", "neutral"] = "default",
    title: Optional[str] = None
) -> dict:
    """
    개념, 아이디어, 계층구조를 마인드맵으로 시각화합니다.
    
    Use this tool for organizing concepts, brainstorming results,
    or showing hierarchical relationships.
    
    Args:
        central_topic: The central theme of the mindmap
        branches: List of branches. Each branch format:
            {"name": "Branch Name", "children": ["Child 1", "Child 2"]}
        theme: Visual theme (default, dark, forest, neutral)
        title: Optional title
    
    Returns:
        Dictionary with image_url and edit_url for the mindmap
    """
    lines = [
        f"%%{{init: {{'theme': '{theme}'}}}}%%",
        "mindmap",
        f"  root(({central_topic}))"
    ]
    
    for branch in branches:
        branch_name = branch.get("name", "")
        children = branch.get("children", [])
        lines.append(f"    {branch_name}")
        for child in children:
            lines.append(f"      {child}")
    
    diagram_code = "\n".join(lines)
    encoded = encode_mermaid(diagram_code)
    
    image_url = f"{Config.MERMAID_BASE_URL}/img/{encoded}"
    edit_url = f"{Config.MERMAID_LIVE_URL}/edit#base64:{encoded}"
    
    return {
        "success": True,
        "type": "mindmap",
        "title": title or central_topic,
        "image_url": image_url,
        "edit_url": edit_url,
        "theme": theme,
        "branch_count": len(branches)
    }


@mcp.tool()
async def generate_table(
    headers: list[str],
    rows: list[list[str]],
    title: Optional[str] = None,
    format: Literal["markdown", "html"] = "markdown",
    style: Literal["default", "dark", "kakao"] = "default",
    highlight_column: Optional[int] = None
) -> dict:
    """
    정보를 구조화된 비교표로 생성합니다.
    
    Use this tool for comparing options, organizing information,
    or presenting pros and cons.
    
    Args:
        headers: Column headers (e.g., ["Feature", "Option A", "Option B"])
        rows: Row data. Each row must match header count.
            Example: [["Price", "$100", "$150"], ["Speed", "Fast", "Faster"]]
        title: Optional table title
        format: Output format (markdown, html)
        style: Visual style (default, dark, kakao)
        highlight_column: Column index to highlight (0-based, optional)
    
    Returns:
        Dictionary with formatted table string
    """
    if not headers or not rows:
        return {"success": False, "error": "Headers and rows cannot be empty."}
    
    col_count = len(headers)
    for i, row in enumerate(rows):
        if len(row) != col_count:
            return {"success": False, "error": f"Row {i+1} column count mismatch."}
    
    table_style = get_table_style(style)
    
    if format == "markdown":
        lines = []
        if title:
            lines.append(f"### {title}\n")
        lines.append("| " + " | ".join(headers) + " |")
        separators = [":---:" if highlight_column == i else "---" for i in range(col_count)]
        lines.append("| " + " | ".join(separators) + " |")
        for row in rows:
            if highlight_column is not None:
                row = [f"**{cell}**" if i == highlight_column else cell for i, cell in enumerate(row)]
            lines.append("| " + " | ".join(row) + " |")
        table_string = "\n".join(lines)
    else:
        s = table_style
        lines = []
        if title:
            lines.append(f"<h3>{title}</h3>")
        lines.append('<table style="border-collapse: collapse; width: 100%;">')
        lines.append("  <thead><tr>")
        for i, h in enumerate(headers):
            bg = s["highlight_bg"] if highlight_column == i else s["header_bg"]
            lines.append(f'    <th style="border: 1px solid {s["border"]}; padding: 8px; background-color: {bg}; color: {s["header_color"]};">{h}</th>')
        lines.append("  </tr></thead><tbody>")
        for row in rows:
            lines.append("    <tr>")
            for i, cell in enumerate(row):
                bg = s["highlight_bg"] if highlight_column == i else "transparent"
                weight = "bold" if highlight_column == i else "normal"
                lines.append(f'      <td style="border: 1px solid {s["border"]}; padding: 8px; background-color: {bg}; font-weight: {weight};">{cell}</td>')
            lines.append("    </tr>")
        lines.append("  </tbody></table>")
        table_string = "\n".join(lines)
    
    return {
        "success": True,
        "type": "table",
        "format": format,
        "title": title,
        "table": table_string,
        "dimensions": {"columns": col_count, "rows": len(rows)}
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(mcp.sse_app(), host="0.0.0.0", port=port)