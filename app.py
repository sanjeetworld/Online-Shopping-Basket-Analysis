"""Small Flask interface for the notebook's saved association rules."""

from __future__ import annotations

import csv
from pathlib import Path

from flask import Flask, render_template, request


PROJECT_DIR = Path(__file__).resolve().parent
RULES_FILE = PROJECT_DIR / "notebooks" / "final_association_rules.csv"
ITEMSETS_FILE = PROJECT_DIR / "notebooks" / "frequent_itemsets.csv"
app = Flask(__name__)


def parse_items(value: str) -> tuple[str, ...]:
    """Read the notebook's comma-separated itemset representation."""
    return tuple(part.strip() for part in (value or "").split(",") if part.strip())


def load_artifacts() -> tuple[list[dict], list[str]]:
    """Load saved rules once at startup; web requests never retrain the model."""
    if not RULES_FILE.is_file():
        raise FileNotFoundError(
            f"Association rules not found: {RULES_FILE}. Run the notebook and export final_association_rules.csv first."
        )

    rules: list[dict] = []
    products: set[str] = set()
    with RULES_FILE.open("r", encoding="utf-8-sig", newline="") as file:
        for row in csv.DictReader(file):
            antecedents = parse_items(row.get("antecedents", ""))
            consequents = parse_items(row.get("consequents", ""))
            if not antecedents or not consequents:
                continue
            products.update(antecedents)
            products.update(consequents)
            try:
                support = float(row["support"])
                confidence = float(row["confidence"])
                lift = float(row["lift"])
            except (KeyError, TypeError, ValueError):
                continue
            rules.append({
                "antecedents": antecedents,
                "consequents": consequents,
                "support": support,
                "confidence": confidence,
                "lift": lift,
            })

    # Include products from the saved itemsets too, even when a product has no
    # direct single-item recommendation rule.
    if ITEMSETS_FILE.is_file():
        with ITEMSETS_FILE.open("r", encoding="utf-8-sig", newline="") as file:
            for row in csv.DictReader(file):
                products.update(parse_items(row.get("itemsets", "")))
    return rules, sorted(products, key=str.casefold)


RULES, PRODUCTS = load_artifacts()


@app.route("/", methods=["GET", "POST"])
def index():
    selected_product = ""
    recommendations: list[dict] = []
    message = ""

    if request.method == "POST":
        selected_product = request.form.get("product", "").strip()
        if selected_product not in PRODUCTS:
            message = "Choose a product from the list to see its recommendations."
        else:
            recommendations = [
                rule for rule in RULES
                if len(rule["antecedents"]) == 1
                and rule["antecedents"][0].casefold() == selected_product.casefold()
            ]
            recommendations.sort(
                key=lambda rule: (rule["confidence"], rule["lift"], rule["support"]),
                reverse=True,
            )
            recommendations = recommendations[:10]
            if not recommendations:
                message = (
                    f"No direct single-product rules were found for {selected_product}. "
                    "Try another product from the list."
                )

    return render_template(
        "index.html",
        products=PRODUCTS,
        selected_product=selected_product,
        recommendations=recommendations,
        message=message,
        rule_count=len(RULES),
        product_count=len(PRODUCTS),
    )


if __name__ == "__main__":
    app.run(debug=True)
