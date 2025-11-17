import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHART_DIR = os.path.join(BASE_DIR, "charts")
ANALYSIS_DIR = os.path.join(BASE_DIR, "analysis")

def analysis_results():
    items = []

    chart_files = [f for f in os.listdir(CHART_DIR) if f.endswith(".png")]

    for chart_file in chart_files:
        name, _ = os.path.splitext(chart_file)
        chart_url = f"/charts/{chart_file}"

        analysis_path = os.path.join(ANALYSIS_DIR, f"{name}.txt")

        if not os.path.exists(analysis_path):
            continue

        with open(analysis_path, "r", encoding="utf-8") as f:
            text = f.read()

        items.append({
            "name": name,
            "chart": chart_url,
            "analysis": text
        })

    return {"results": items}
