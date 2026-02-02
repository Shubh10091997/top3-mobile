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
# BUDGET MAPPINGS
# =========================
BUDGET_DISPLAY = {
    8000: "8k",
    10000: "10k",
    15000: "15k",
    20000: "20k"
}

BUDGET_REVERSE = {v: k for k, v in BUDGET_DISPLAY.items()}

USE_NAMES = {
    "overall": "Best Overall",
    "gaming": "Best for Gaming",
    "camera": "Best Camera",
    "battery": "Best Battery"
}

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

def render_results(category, budget, use, db=None):
    """Helper function to render results page"""
    if db is None:
        db = load_data()
    
    items = db["mobiles"] if category == "mobile" else db["bikes"]
    items = [i for i in items if i.get("price", 0) <= budget]

    if not items:
        return render_template(
            "result.html",
            top3=[],
            others=[],
            message="No results found 😕",
            category=category,
            budget=budget,
            use=use,
            breadcrumb_category=category.capitalize(),
            breadcrumb_use=USE_NAMES.get(use, use.capitalize())
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
        breadcrumb_category=category.capitalize(),
        breadcrumb_use=USE_NAMES.get(use, use.capitalize()),
        seo_title=f"Top 3 Best {category.capitalize()} Under ₹{budget} for {USE_NAMES.get(use, use.capitalize())}",
        seo_desc=f"Compare the best {category}s under ₹{budget} in India for {use}. Expert recommendations."
    )

# =========================
# HOME PAGE
# =========================
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        category = request.form.get("category")
        budget = int(request.form.get("budget"))
        use = request.form.get("use")
        
        # Redirect to clean GET URL
        return redirect(f"/{category}/{budget}/{use}")

    return render_template(
        "index.html",
        seo_title="Top 3 Best Options in India",
        seo_desc="Compare top 3 mobiles and bikes in India before buying"
    )

# =========================
# SLUG-BASED FRIENDLY ROUTES (e.g., /best-mobiles/under-8k)
# =========================
@app.route("/best-<category>")
def best_category_root(category):
    """Route: /best-mobiles"""
    category_map = {"mobiles": "mobile", "bikes": "bike"}
    cat = category_map.get(category, None)
    
    if not cat:
        abort(404)
    
    # Default to 10k budget and overall rating
    return render_results(cat, 10000, "overall")

@app.route("/best-<category>/under-<budget_slug>")
def best_category_budget(category, budget_slug):
    """Route: /best-mobiles/under-8k"""
    category_map = {"mobiles": "mobile", "bikes": "bike"}
    cat = category_map.get(category, None)
    
    if not cat:
        abort(404)
    
    budget = BUDGET_REVERSE.get(budget_slug.lower(), None)
    if budget is None:
        abort(404)
    
    return render_results(cat, budget, "overall")

@app.route("/best-<category>/under-<budget_slug>/for-<use>")
def best_category_full(category, budget_slug, use):
    """Route: /best-mobiles/under-8k/for-gaming"""
    category_map = {"mobiles": "mobile", "bikes": "bike"}
    cat = category_map.get(category, None)
    
    if not cat:
        abort(404)
    
    budget = BUDGET_REVERSE.get(budget_slug.lower(), None)
    if budget is None:
        abort(404)
    
    if use not in ["overall", "gaming", "camera", "battery", "mileage", "performance", "comfort"]:
        abort(404)
    
    return render_results(cat, budget, use)

# =========================
# LEGACY SEO-FRIENDLY URLS (numeric format)
# =========================
@app.route("/<category>/<int:budget>/<use>", methods=["GET"])
def seo_page(category, budget, use):
    if category not in ["mobile", "bike"]:
        abort(404)
    if use not in ["overall", "gaming", "camera", "battery"]:
        abort(404)
    
    return render_results(category, budget, use)

# =========================
# QUERY PARAMETER SUPPORT (shareable URLs)
# =========================
@app.route("/compare/<category>")
def compare(category):
    """Support /compare/mobile?budget=10000&use=overall format"""
    budget = request.args.get("budget", "10000", type=int)
    use = request.args.get("use", "overall", type=str)
    
    if category not in ["mobile", "bike"]:
        abort(404)
    if use not in ["overall", "gaming", "camera", "battery"]:
        abort(404)
    
    return render_results(category, budget, use)

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
    
    # Home page
    urls.add(f"{BASE_URL}/")
    
    # Category pages
    urls.add(f"{BASE_URL}/best-mobiles")
    urls.add(f"{BASE_URL}/best-bikes")
    
    # Budget slug pages
    for slug, budget in BUDGET_REVERSE.items():
        urls.add(f"{BASE_URL}/best-mobiles/under-{slug}")
        urls.add(f"{BASE_URL}/best-mobiles/under-{slug}/for-overall")
        urls.add(f"{BASE_URL}/best-mobiles/under-{slug}/for-gaming")
        urls.add(f"{BASE_URL}/best-mobiles/under-{slug}/for-camera")
        urls.add(f"{BASE_URL}/best-mobiles/under-{slug}/for-battery")
    
    # Numeric format routes (legacy support)
    uses = ["overall", "gaming", "camera", "battery"]
    for m in db.get("mobiles", []):
        for use in uses:
            urls.add(f"{BASE_URL}/mobile/{m['price']}/{use}")
    
    # Query parameter format
    budgets = [8000, 10000, 15000, 20000]
    for budget in budgets:
        for use in uses:
            urls.add(f"{BASE_URL}/compare/mobile?budget={budget}&use={use}")

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
