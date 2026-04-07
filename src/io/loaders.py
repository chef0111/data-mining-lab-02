import pandas as pd


def load_groceries_transactions(path):
    transactions = []
    with open(path, "r") as f:
        for line in f:
            items = [item.strip() for item in line.strip().split(",") if item.strip()]
            transactions.append(items)
    return transactions


def load_online_retail(path):
    return pd.read_excel(path, sheet_name="Online Retail")


def clean_online_retail(retail_df):
    return (
        retail_df.dropna(subset=["CustomerID"])
        .query("Quantity > 0 and UnitPrice > 0")
        .copy()
    )


def build_invoice_transactions(retail_clean_df):
    basket = retail_clean_df.groupby("InvoiceNo")["Description"].apply(list)
    return basket.tolist()
