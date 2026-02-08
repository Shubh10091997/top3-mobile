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
# AFFILIATE IDS
# =========================
AMAZON_ASSOCIATE_ID = "bestofthree-21"

# =========================
# HELPER FUNCTION FOR IMAGES
# =========================
def get_phone_image_url(model, brand):
    """Generate a placeholder image for each phone"""
    safe_name = f"{brand} {model}".replace(" ", "+")
    return f"https://via.placeholder.com/300x400?text={safe_name}"

# =========================
# DATA LOAD FUNCTIONS
# =========================
def load_data():
    """Load phone data from all brand-specific JSON files and merge them"""
    brands = ["samsung", "realme", "redmi", "poco", "apple", "vivo", "oppo", "motorola"]
    all_phones = []
    
    # Load each brand's phone data
    for brand in brands:
        brand_file = os.path.join(BASE_DIR, "data", f"{brand}.json")
        try:
            with open(brand_file, "r", encoding="utf-8") as f:
                brand_data = json.load(f)
                if isinstance(brand_data, dict) and "phones" in brand_data:
                    phones = brand_data.get("phones", [])
                    # Add brand name and ensure required fields
                    for phone in phones:
                        if "brand" not in phone:
                            phone["brand"] = brand_data.get("brand", brand.capitalize())
                        
                        # Set phone name if not present
                        if "name" not in phone:
                            phone["name"] = phone.get("model", "Unknown")
                        
                        # Add reason/why buy if not present
                        if "reason" not in phone:
                            best_for = phone.get("best_for", [])
                            if best_for:
                                phone["reason"] = f"Best for {', '.join(best_for)}"
                            else:
                                phone["reason"] = "Great choice"
                        
                        # Add numeric ratings (1-10) for display
                        if "rating" not in phone:
                            phone["rating"] = 4.0
                        
                        # Ensure numeric specs for template (default to rating value)
                        rating = phone.get("rating", 4.0)
                        specs = ["gaming", "camera", "battery", "performance", "display"]
                        for spec in specs:
                            if spec not in phone or not isinstance(phone[spec], (int, float)):
                                phone[spec] = rating
                        
                        # Add image URL
                        if "image" not in phone or not phone.get("image"):
                            brand_name = phone.get("brand", brand)
                            model_name = phone.get("model", "")
                            phone["image"] = get_phone_image_url(model_name, brand_name)
                    
                    all_phones.extend(phones)
        except (FileNotFoundError, json.JSONDecodeError):
            pass  # Skip if file doesn't exist or is invalid

    # Return data structure that maintains compatibility with existing code
    data = {
        "mobiles": all_phones,
        "bikes": [],
        "laptops": [],
        "tvs": [],
        "audio": []
    }
    
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
    20000: "20k",
    25000: "25k",
    30000: "30k",
    40000: "40k",
    50000: "50k",
    75000: "75k",
    100000: "1 lakh"
}

USE_NAMES = {
    "overall": "Overall",
    "gaming": "Gaming",
    "camera": "Camera",
    "battery": "Battery",
    "performance": "Performance",
    "display": "Display"
}

# =========================
# HELPER FUNCTIONS
# =========================
def _coerce_price(p):
    try:
        return int(p) if isinstance(p, (int, float, str)) else 0
    except:
        return 0

def overall_score(item):
    """Calculate overall score based on specs"""
    try:
        specs = [
            item.get("gaming", 0),
            item.get("camera", 0),
            item.get("battery", 0),
            item.get("performance", 0),
            item.get("display", 0)
        ]
        return sum(s for s in specs if isinstance(s, (int, float))) / 5
    except:
        return 0

def add_badges(top3):
    badges = ["Top Choice", "Best Alternative", "Good Option"]
    for i, item in enumerate(top3):
        if i < len(badges):
            item["badge"] = badges[i]

# =========================
# RESULTS PAGE
# =========================
@app.route("/compare/<category>", methods=["GET"])
def get_results(category):
    budget = int(request.args.get("budget", 10000))
    use = request.args.get("use", "overall").lower()
    
    return render_results(category, budget, use)

def render_results(category, budget, use):
    """Render results for comparison"""
    db = load_data()
    
    # Category mapping
    category_map = {
        "mobile": "mobiles",
        "bike": "bikes",
        "tv": "tvs",
        "laptop": "laptops",
        "audio": "audio"
    }
    items = db.get(category_map.get(category, "mobiles"), [])
    items = [i for i in items if _coerce_price(i.get("price", 0)) <= budget]

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
            breadcrumb_use=USE_NAMES.get(use, use.capitalize()),
            request=request
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
        seo_desc=f"Compare the best {category}s under ₹{budget} in India for {use}. Expert recommendations.",
        request=request
    )

# =========================
# HEALTH CHECK
# =========================
@app.route("/health")
def health_check():
    return {"status": "healthy"}, 200

# =========================
# HOME PAGE
# =========================
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        category = request.form.get("category")
        budget = int(request.form.get("budget"))
        use = request.form.get("use")
        return redirect(f"/{category}/{budget}/{use}")

    db = load_data()
    mobiles_preview = db.get("mobiles", [])[:4]
    new_launch_phones = [p for p in db.get("mobiles", []) if p.get("is_new_launch", False)][:4]

    return render_template(
        "index.html",
        mobiles_preview=mobiles_preview,
        mobiles_count=len(db.get("mobiles", [])),
        new_launch_phones=new_launch_phones,
        seo_title="Top 3 Best Options in India",
        seo_desc="Compare top 3 mobiles and bikes in India before buying"
    )

# =========================
# ABOUT PAGE
# =========================
@app.route("/about")
def about():
    return render_template("about.html")

# =========================
# CONTACT PAGE
# =========================
@app.route("/contact")
def contact():
    return render_template("contact.html")

# =========================
# PRIVACY POLICY
# =========================
@app.route("/privacy-policy")
def privacy_policy():
    return render_template("privacy_policy.html")

# =========================
# ERROR HANDLERS
# =========================
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def server_error(e):
    return render_template("500.html"), 500

# =========================
# RUN APP
# =========================
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
