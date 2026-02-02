import json
import os
from flask import Flask, render_template, request, redirect, abort, Response

app = Flask(__name__)

# =========================
# BASE DIR
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# =========================
# BASE URL
# =========================
BASE_URL = "https://top3pick.in"

# =========================
# DATA LOAD FUNCTIONS
# =========================
def load_data():
    with open(os.path.join(BASE_DIR, "data", "data.json"), "r", encoding="utf-8") as f:
        data = json.load(f)

    # Ensure every product has an `image` key to avoid template errors.
    default_image = "/static/no-image.png"
    for collection in ("mobiles", "bikes"):
        for item in data.get(collection, []):
            if "image" not in item or not item.get("image"):
                item["image"] = default_image

    return data

def load_clicks():
    with open(os.path.join(BASE_DIR, "data", "clicks.json"), "r", encoding="utf-8") as f:
        return json.load(f)

def save_clicks(data):
    with open(os.path.join(BASE_DIR, "data", "clicks.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

# =========================
# HELPERS
# =========================
def overall_score(item):
    values = [v for v in item.values() if isinstance(v, int)]
    return sum(values) / len(values) if values else 0

def add_badges(top3):
    badges = ["Top Choice", "Best Alternative", "Good Option"]
    for i, item in enumerate(top3):
        if i < len(badges):
            item["badge"] = badges[i]

# =========================
# HOME PAGE
# =========================
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        category = request.form.get("category")
        budget = int(request.form.get("budget"))
        use = request.form.get("use")

        db = load_data()
        items = db["mobiles"] if category == "mobile" else db["bikes"]
        items = [i for i in items if i.get("price", 0) <= budget]

        if not items:
            return render_template(
                "result.html",
                top3=[],
                others=[],
                message="No options found 😕",
                category=category,
                budget=budget,
                use=use
            )

        items.sort(
            key=overall_score if use == "overall" else lambda x: x.get(use, 0),
            reverse=True
        )

        top3 = items[:3]
        add_badges(top3)

        return render_template(
            "result.html",
            top3=top3,
            others=items[3:],
            category=category.capitalize(),
            budget=budget,
            use=use.capitalize(),
            seo_title=f"Top 3 Best {category.capitalize()} Under ₹{budget}",
            seo_desc=f"Compare top 3 best {category}s under ₹{budget} in India"
        )

    return render_template(
        "index.html",
        seo_title="Top 3 Best Options in India",
        seo_desc="Compare top 3 mobiles and bikes in India before buying"
    )

# =========================
# SEO FRIENDLY URL
# =========================
@app.route("/<category>/<int:budget>/<use>")
def seo_page(category, budget, use):
    if category not in ["mobile", "bike"]:
        abort(404)

    db = load_data()
    items = db["mobiles"] if category == "mobile" else db["bikes"]
    items = [i for i in items if i.get("price", 0) <= budget]

    if not items:
        return render_template(
            "result.html",
            top3=[],
            others=[],
            message="No results found",
            category=category,
            budget=budget,
            use=use
        )

    items.sort(
        key=overall_score if use == "overall" else lambda x: x.get(use, 0),
        reverse=True
    )

    top3 = items[:3]
    add_badges(top3)

    return render_template(
        "result.html",
        top3=top3,
        others=items[3:],
        category=category.capitalize(),
        budget=budget,
        use=use.capitalize(),
        seo_title=f"Top 3 Best {category.capitalize()} Under ₹{budget} for {use.capitalize()}",
        seo_desc=f"Best {category}s under ₹{budget} for {use} in India"
    )

# =========================
# CLICK TRACKING
# =========================
@app.route("/go/<platform>")
def go(platform):
    clicks = load_clicks()

    if platform in clicks:
        clicks[platform] += 1
        save_clicks(clicks)

    if platform == "amazon":
        return redirect("https://www.amazon.in/")
    elif platform == "flipkart":
        return redirect("https://www.flipkart.com/")
    return redirect("/")

@app.route("/click-stats")
def click_stats():
    return load_clicks()

# =========================
# ROBOTS.TXT  ✅ (MOST IMPORTANT FIX)
# =========================
@app.route("/robots.txt")
def robots_txt():
    return Response(
        f"""User-agent: *\nAllow: /\n\nSitemap: {BASE_URL}/sitemap.xml\n""",
        mimetype="text/plain"
    )

# =========================
# SITEMAP.XML
# =========================
@app.route("/sitemap.xml")
def sitemap():
    db = load_data()
    urls = set()
    urls.add(f"{BASE_URL}/")

    uses = ["overall", "gaming", "camera", "battery"]

    for m in db.get("mobiles", []):
        for use in uses:
            urls.add(f"{BASE_URL}/mobile/{m['price']}/{use}")

    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

    for url in sorted(urls):
        xml.append(f"<url><loc>{url}</loc></url>")

    xml.append('</urlset>')
    return Response("\n".join(xml), mimetype="application/xml")

# =========================
# RUN APP
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
