import json
import os
from flask import Flask, render_template, request, redirect, send_file

app = Flask(__name__)

# ================= DATA LOAD =================
def load_data():
    with open(os.path.join("data", "data.json"), "r", encoding="utf-8") as f:
        return json.load(f)

def load_clicks():
    with open(os.path.join("data", "clicks.json"), "r", encoding="utf-8") as f:
        return json.load(f)

def save_clicks(data):
    with open(os.path.join("data", "clicks.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

# ================= HELPER =================
def overall_score(item):
    nums = [v for v in item.values() if isinstance(v, int)]
    return sum(nums) / len(nums) if nums else 0

# ================= HOME =================
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        category = request.form["category"]
        budget = int(request.form["budget"])
        use = request.form["use"]

        db = load_data()
        items = db["mobiles"] if category == "mobile" else db["bikes"]
        items = [i for i in items if i["price"] <= budget]

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

        return render_template(
            "result.html",
            top3=items[:3],
            others=items[3:],
            category=category.capitalize(),
            budget=budget,
            use=use.capitalize(),
            seo_title=f"Top 3 Best {category.capitalize()} Under ₹{budget}",
            seo_desc=f"Compare top 3 best {category}s under ₹{budget}"
        )

    return render_template(
        "index.html",
        seo_title="Top 3 Best Options",
        seo_desc="Compare mobiles and bikes smartly before buying"
    )

# ================= SEO URL =================
@app.route("/<category>/<int:budget>/<use>")
def seo_page(category, budget, use):
    db = load_data()

    if category not in ["mobile", "bike"]:
        return "Invalid category", 404

    items = db["mobiles"] if category == "mobile" else db["bikes"]
    items = [i for i in items if i["price"] <= budget]

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

    return render_template(
        "result.html",
        top3=items[:3],
        others=items[3:],
        category=category.capitalize(),
        budget=budget,
        use=use.capitalize(),
        seo_title=f"Top 3 Best {category.capitalize()} Under ₹{budget} for {use.capitalize()}",
        seo_desc=f"Compare top 3 best {category}s under ₹{budget}"
    )

# ================= CLICK TRACKING =================
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

# ================= SITEMAP =================
@app.route("/sitemap.xml")
def sitemap():
    return send_file(
        os.path.join(app.root_path, "sitemap.xml"),
        mimetype="application/xml"
    )

# ================= ROBOTS =================
@app.route("/robots.txt")
def robots():
    return send_file(
        os.path.join(app.root_path, "robots.txt"),
        mimetype="text/plain"
    )

# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True)
