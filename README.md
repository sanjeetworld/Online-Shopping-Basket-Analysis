# Online Shopping Basket Analysis

A Python project that analyzes grocery purchases to find products that are often bought together. It uses the Apriori algorithm to create frequent itemsets and association rules, then provides a small Flask web app for exploring product recommendations.

## Features

- Cleans and explores the grocery transaction data.
- Builds customer and date based baskets from the transaction records.
- Finds frequent itemsets with Apriori and generates association rules.
- Evaluates recommendations against held out baskets in the notebook.
- Provides a Flask interface that reads the notebook's saved rules. It does not retrain the model for each web request.
- Shows support, confidence, and lift for each recommendation.

## Project layout

```text
Online-Shopping-Basket-Analysis/
├── app.py
├── dataset/
│   └── Dataset14-Grocery-MarketBasket-Analysis.csv
├── notebooks/
│   ├── market_basket_analysis.ipynb
│   ├── final_association_rules.csv
│   ├── frequent_itemsets.csv
│   └── customer_validation_results.csv
├── static/
│   └── style.css
├── templates/
│   └── index.html
└── requirements.txt
```

## Requirements

- Python 3.12
- pip

## Setup

Open a terminal in the project folder and create a virtual environment:

```powershell
python -m venv .venv
```

Activate it in PowerShell and install the dependencies:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If PowerShell prevents environment activation, run this once in the current terminal and activate again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

## Run the analysis notebook

Start Jupyter from the project folder:

```powershell
jupyter notebook
```

Open `notebooks/market_basket_analysis.ipynb` and run its cells. The web app expects the notebook to have created these files:

- `notebooks/final_association_rules.csv`
- `notebooks/frequent_itemsets.csv`

The provided CSV exports are ready to use. Rerun the notebook if you change the dataset or want to regenerate the analysis results.

## Run the web app

From the project folder, with the virtual environment activated:

```powershell
python app.py
```

Open <http://127.0.0.1:5000> in a browser. Search for a product or choose one from the suggestions, then select **Show recommendations**. The app shows up to ten direct recommendations based on rules whose antecedent is that single product. If no direct rule exists for a product, try another product.

Stop the local server with `Ctrl+C` in the terminal.

## Understanding the metrics

- **Support**: the fraction of all baskets containing both the selected product and recommended item(s).
- **Confidence**: among baskets containing the selected product, the fraction that also contain the recommendation.
- **Lift**: how much more often the products occur together than would be expected if they were independent. A value above 1 indicates a positive association.

## Dataset

The included grocery dataset contains transaction records with member number, date, and item description. Baskets are formed using the member and date fields. Keep the dataset's original license and attribution with the project when redistributing it.

## Notes

- Run `app.py` from the project root so it can find the `notebooks` exports.
- The app uses the saved CSV rules and itemsets; it does not run Apriori when a page is opened.
- Do not commit your `.venv` folder to GitHub. It can be recreated using the setup steps above.
