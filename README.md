# Think & Show MCP Server

An MCP (Model Context Protocol) server that visualizes AI responses as charts, diagrams, and tables.

## 🎯 Problem It Solves

Instead of AI responding with walls of text, it shows results visually.

### Before (Traditional AI Response)
```
The MacBook Air and MacBook Pro differ in several ways.
In terms of performance, the MacBook Pro features the M3 Pro 
or M3 Max chip, delivering higher performance. Meanwhile, 
the MacBook Air uses the M3 chip...
(endless wall of text continues)
```

### After (With Think & Show)
→ Clean comparison table + performance radar chart

---

## 🛠️ Available Tools

| Tool | Purpose | Output |
|------|---------|--------|
| `draw_logic_flow` | Processes, algorithms, system flows | Mermaid diagram |
| `plot_data_chart` | Number comparisons, trends, distributions | Chart.js chart |
| `render_mindmap` | Concept organization, brainstorming | Mermaid mindmap |
| `generate_table` | Option comparisons, information organization | Markdown/HTML table |

---

## 🚀 Quick Start

### Local Development
```bash
# Clone
git clone https://github.com/Freon-Gas/think-and-show-mcp.git
cd think-and-show-mcp

# Install dependencies
pip install -r requirements.txt

# Run
python server.py
```

### Claude Desktop Integration

Add to `claude_desktop_config.json`:

**Windows:**
```json
{
  "mcpServers": {
    "think-and-show": {
      "command": "python",
      "args": ["C:\\path\\to\\server.py"]
    }
  }
}
```

**macOS/Linux:**
```json
{
  "mcpServers": {
    "think-and-show": {
      "command": "python3",
      "args": ["/path/to/server.py"]
    }
  }
}
```

---

## 📡 Deployed Endpoint
```
SSE: https://think-and-show-mcp.onrender.com/sse
```

---

## 🎨 Supported Themes

| Theme | Description |
|-------|-------------|
| `light` | Light background (default) |
| `dark` | Dark mode |
| `kakao` | Kakao style (yellow) |

---

## 📝 Usage Examples

### Create a Chart
```json
{
  "chart_type": "bar",
  "labels": ["Jan", "Feb", "Mar"],
  "datasets": [{"label": "Sales", "data": [100, 150, 200]}],
  "title": "Monthly Sales"
}
```

### Create a Flowchart
```json
{
  "diagram_code": "flowchart TD\n    A[Start] --> B{Condition}\n    B -->|Yes| C[Execute]\n    B -->|No| D[End]",
  "diagram_type": "flowchart"
}
```

### Create a Mindmap
```json
{
  "central_topic": "MCP Server",
  "branches": [
    {"name": "Tools", "children": ["draw_flow", "plot_chart"]},
    {"name": "Themes", "children": ["light", "dark", "kakao"]}
  ]
}
```

### Create a Comparison Table
```json
{
  "headers": ["Feature", "Option A", "Option B"],
  "rows": [
    ["Price", "$100", "$150"],
    ["Performance", "Good", "Excellent"]
  ],
  "title": "Options Comparison"
}
```

---

## 🔧 Environment Variables (Optional)

| Variable | Default | Description |
|----------|---------|-------------|
| `MERMAID_BASE_URL` | `https://mermaid.ink` | Mermaid rendering server |
| `QUICKCHART_URL` | `https://quickchart.io/chart` | QuickChart server |
| `DEFAULT_CHART_WIDTH` | `500` | Default chart width (px) |
| `DEFAULT_CHART_HEIGHT` | `300` | Default chart height (px) |

---

## 📁 Project Structure
```
think-and-show-mcp/
├── server.py           # Main MCP server
├── requirements.txt    # Python dependencies
├── render.yaml         # Render deployment config
├── README.md           # Documentation
└── LICENSE             # MIT License
```

---

## 🏆 PlayMCP Submission

- **MCP Name**: Think & Show
- **Category**: Productivity / Visualization
- **SSE Endpoint**: `https://think-and-show-mcp.onrender.com/sse`

---

## 📄 License

[MIT License](LICENSE) - Free to use, modify, and distribute.

---

## 🤝 Contributing

Issues and PRs are welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing`)
5. Open a Pull Request