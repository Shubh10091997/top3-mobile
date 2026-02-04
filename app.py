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
    
    category_map = {
        "mobile": "mobiles",
        "bike": "bikes",
        "laptop": "laptops",
        "tv": "tvs",
        "audio": "audio"
    }
    items = db.get(category_map.get(category, "mobiles"), [])
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
            BASE_URL=BASE_URL,
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
        BASE_URL=BASE_URL,
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

    db = load_data()
    mobiles_preview = db.get("mobiles", [])[:4]

    return render_template(
        "index.html",
        mobiles_preview=mobiles_preview,
        mobiles_count=len(db.get("mobiles", [])),
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
    requested_category = request.args.get("category", "", type=str).lower()
    if requested_category:
        category = requested_category
    budget = request.args.get("budget", "10000", type=int)
    use = request.args.get("use", "overall", type=str)
    
    if category not in ["mobile", "bike", "laptop", "tv", "audio"]:
        abort(404)
    if use not in ["overall", "gaming", "camera", "battery", "performance", "display", "sound", "comfort"]:
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
# ADMIN STATS DASHBOARD
# =========================
@app.route("/admin/stats")
def admin_stats():
    clicks = load_clicks()
    total_clicks = sum(clicks.values()) if clicks else 0
    return render_template(
        "admin_stats.html",
        clicks=clicks,
        total_clicks=total_clicks
    )

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
# API ENDPOINTS
# =========================
@app.route("/api/phones", methods=["GET"])
def api_phones():
    """API endpoint to fetch all phones for frontend knowledge base"""
    from flask import jsonify
    db = load_data()
    return jsonify(db)

@app.route("/api/search", methods=["GET"])
def api_search():
    """
    Advanced phone search API
    Query parameters:
    - q: search query (name, price, specs)
    - category: 'mobile' or 'bike'
    - min_price: minimum price
    - max_price: maximum price
    - sort_by: 'price', 'rating', 'gaming', 'camera', 'battery', 'performance'
    - limit: number of results (default: 50)
    """
    from flask import jsonify
    
    db = load_data()
    query = request.args.get("q", "").lower()
    category = request.args.get("category", "mobile").lower()
    min_price = request.args.get("min_price", 0, type=int)
    max_price = request.args.get("max_price", 500000, type=int)
    sort_by = request.args.get("sort_by", "price")
    limit = request.args.get("limit", 50, type=int)
    
    # Get the right category
    items = db.get("mobiles" if category == "mobile" else "bikes", [])
    
    # Filter by price range
    items = [item for item in items if min_price <= item.get("price", 0) <= max_price]
    
    # Filter by search query
    if query:
        filtered = []
        for item in items:
            item_text = f"{item.get('name', '')} {item.get('reason', '')}".lower()
            if query in item_text or str(item.get('price', '')).startswith(query):
                filtered.append(item)
        items = filtered
    
    # Sort by criteria
    if sort_by == "price":
        items.sort(key=lambda x: x.get("price", 0))
    elif sort_by == "rating":
        items.sort(key=lambda x: overall_score(x), reverse=True)
    elif sort_by in ["gaming", "camera", "battery", "performance", "mileage"]:
        items.sort(key=lambda x: x.get(sort_by, 0), reverse=True)
    
    # Limit results
    items = items[:limit]
    
    return jsonify({
        "success": True,
        "query": query,
        "category": category,
        "count": len(items),
        "results": items
    })

@app.route("/api/phone/<name>", methods=["GET"])
def api_phone_detail(name):
    """Get detailed information about a specific phone"""
    from flask import jsonify
    
    db = load_data()
    
    # Search in mobiles first, then bikes
    for item in db.get("mobiles", []) + db.get("bikes", []):
        if item.get("name", "").lower().replace(" ", "-") == name.lower().replace(" ", "-"):
            return jsonify({"success": True, "phone": item})
    
    return jsonify({"success": False, "error": "Phone not found"}), 404

@app.route("/api/add-phone", methods=["POST"])
def api_add_phone():
    """Add a new phone to the database via API"""
    from flask import jsonify
    
    try:
        phone = request.get_json()
        
        # Validate required fields
        required_fields = ["name", "price", "reason"]
        for field in required_fields:
            if not phone.get(field):
                return jsonify({"success": False, "error": f"Missing required field: {field}"}), 400
        
        # Set defaults for optional fields
        if "gaming" not in phone:
            phone["gaming"] = 5
        if "camera" not in phone:
            phone["camera"] = 5
        if "battery" not in phone:
            phone["battery"] = 5
        if "performance" not in phone:
            phone["performance"] = 5
        if "display" not in phone:
            phone["display"] = 5
        if "image" not in phone or not phone["image"]:
            phone["image"] = "/static/no-image.png"
        if "amazon" not in phone:
            phone["amazon"] = f"https://www.amazon.in/s?k={phone['name'].replace(' ', '+')}"
        if "flipkart" not in phone:
            phone["flipkart"] = f"https://www.flipkart.com/search?q={phone['name']}"
        
        # Load existing data
        db = load_data()
        
        # Check if phone already exists
        for item in db.get("mobiles", []):
            if item.get("name", "").lower() == phone["name"].lower():
                return jsonify({"success": False, "error": "Phone already exists in database"}), 400
        
        # Add phone to database
        db["mobiles"].append(phone)
        save_clicks(db)  # Save updated data
        
        # Re-read from file to ensure consistency
        save_data = lambda data: open(os.path.join(BASE_DIR, "data", "data.json"), "w", encoding="utf-8").write(
            json.dumps(data, indent=2, ensure_ascii=False)
        )
        save_data(db)
        
        return jsonify({"success": True, "message": f"Phone '{phone['name']}' added successfully!"})
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/admin/add-phone")
def admin_add_phone():
    """Admin page to add phones via web interface"""
    return render_template("admin_add_phone.html")

# =========================
# ALL BRANDS PAGE
# =========================
@app.route("/all-brands")
def all_brands():
    """Show all mobile brands category-wise"""
    return render_template("all_brands.html")

# =========================
# SEARCH RESULTS PAGE
# =========================
@app.route("/search")
def search_results():
    """Display formatted search results for a brand/query"""
    return render_template("search_results.html")

# =========================
# STATIC PAGES
# =========================
@app.route("/about")
def about():
    """About page"""
    return render_template("about.html")

@app.route("/contact")
def contact():
    """Contact page"""
    return render_template("contact.html")

@app.route("/privacy-policy")
def privacy_policy():
    """Privacy policy page"""
    return render_template("privacy_policy.html")

# =========================
# RUN APP
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
