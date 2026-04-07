from itertools import combinations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from mlxtend.frequent_patterns import apriori as mlxtend_apriori
from mlxtend.frequent_patterns import association_rules, fpgrowth
from mlxtend.preprocessing import TransactionEncoder

from src.config import (
    EX2_OUTPUT_PATH,
    EX2_PLOT_PATH,
    PROJECT_ROOT,
    RETAIL_PATH,
    ensure_output_dirs,
)
from src.io.loaders import (
    build_invoice_transactions,
    clean_online_retail,
    load_online_retail,
)
from src.io.output_capture import setup_output_capture
from src.mining.counting import frequent_1_itemsets, frequent_2_itemsets
from src.mining.metrics import compute_confidence, compute_support


def run():
    ensure_output_dirs()
    setup_output_capture(EX2_OUTPUT_PATH)

    # ================================================================
    # EXERCISE 2 - Online_Retail.xlsx
    # ================================================================
    print("\n" + "=" * 65)
    print("EXERCISE 2: Online_Retail.xlsx")
    print("=" * 65)

    # Question 1: Read, inspect, clean
    print("\n--- Q1: Read and clean Online_Retail.xlsx ---")

    retail = load_online_retail(RETAIL_PATH)
    print("Raw shape:", retail.shape)
    print("\nColumns:", list(retail.columns))
    print("\nMissing values:")
    print(retail.isnull().sum())

    retail_clean = clean_online_retail(retail)
    print(
        f"\nClean shape: {retail_clean.shape}  (removed {len(retail)-len(retail_clean)} rows)"
    )
    print(retail_clean.head(3))

    # Question 2: Build transaction list (InvoiceNo = one basket)
    print("\n--- Q2: Transaction list ---")

    rx = build_invoice_transactions(retail_clean)
    rx_sets = [set(t) for t in rx]
    print(f"Number of transactions: {len(rx)}")
    print(f"Sample [0]: {rx[0][:4]}")

    # Question 3: Support function
    print("\n--- Q3: Support function ---")
    print("  compute_support(itemset, transactions) defined.")

    # Question 4: Compute support for specific itemsets
    print("\n--- Q4: Support of specific itemsets ---")

    checks = [
        ["WHITE HANGING HEART T-LIGHT HOLDER"],
        ["JUMBO BAG RED RETROSPOT"],
        ["WHITE HANGING HEART T-LIGHT HOLDER", "JUMBO BAG RED RETROSPOT"],
        ["REGENCY CAKESTAND 3 TIER", "JUMBO BAG RED RETROSPOT"],
    ]
    for its in checks:
        print(f"  support({its}) = {compute_support(its, rx_sets):.6f}")

    # Question 5: Frequent 1-itemsets (min_support=0.02, computed directly)
    print("\n--- Q5: Frequent 1-itemsets (min_support=0.02) ---")

    min_sup_r = 0.02
    freq1_retail = frequent_1_itemsets(rx_sets, min_sup_r)

    print(f"Frequent 1-itemsets: {len(freq1_retail)}")
    for item, sup in sorted(freq1_retail.items(), key=lambda x: -x[1])[:5]:
        print(f"  {item:<45s} {sup:.4f}")

    # Question 6: Candidate 2-itemsets
    print("\n--- Q6: Candidate 2-itemsets ---")

    c2_retail = list(combinations(freq1_retail.keys(), 2))
    print(f"Candidate 2-itemsets: {len(c2_retail)}")

    # Question 7: Frequent 2-itemsets
    print("\n--- Q7: Frequent 2-itemsets ---")

    freq2_retail = frequent_2_itemsets(rx_sets, freq1_retail, min_sup_r)

    print(f"Frequent 2-itemsets: {len(freq2_retail)}")
    for pair, sup in sorted(freq2_retail.items(), key=lambda x: -x[1])[:5]:
        print(f"  {set(pair)}  {sup:.4f}")

    # Question 8: Confidence function
    print("\n--- Q8: Confidence function ---")

    x_d = ["REGENCY CAKESTAND 3 TIER"]
    y_d = ["JUMBO BAG RED RETROSPOT"]
    print(f"  confidence({x_d} -> {y_d}) = {compute_confidence(x_d, y_d, rx_sets):.4f}")

    # Question 9: Apriori (mlxtend) on Online Retail
    print("\n--- Q9: Apriori on Online Retail (min_support=0.02) ---")

    te_r = TransactionEncoder()
    arr_r = te_r.fit(rx).transform(rx)
    df_r = pd.DataFrame(arr_r, columns=te_r.columns_)

    fi_retail_a = mlxtend_apriori(df_r, min_support=0.02, use_colnames=True)
    print(f"Frequent itemsets (Apriori): {len(fi_retail_a)}")
    sz = fi_retail_a["itemsets"].apply(len).value_counts().sort_index()
    for s, c in sz.items():
        print(f"  {s}-itemsets: {c}")

    # Question 10: One-hot encoding
    print("\n--- Q10: One-hot encoding ---")
    print(f"Shape: {df_r.shape}")
    print(df_r.iloc[:3, :5])

    # Question 11: mlxtend Apriori (already done above)
    print("\n--- Q11: mlxtend Apriori results ---")
    print(fi_retail_a.sort_values("support", ascending=False).head(5).to_string())

    # Question 12: FP-Growth on Online Retail
    print("\n--- Q12: FP-Growth (min_support=0.02) ---")

    fi_retail_fp = fpgrowth(df_r, min_support=0.02, use_colnames=True)
    print(f"Frequent itemsets (FP-Growth): {len(fi_retail_fp)}")
    print(fi_retail_fp.sort_values("support", ascending=False).head(5).to_string())

    # Question 13: Association rules
    print("\n--- Q13: Association rules (Online Retail, min_conf=0.3) ---")

    rules_r = association_rules(fi_retail_fp, metric="confidence", min_threshold=0.3)
    print(f"Total rules: {len(rules_r)}")
    print(
        rules_r[
            ["antecedents", "consequents", "support", "confidence", "lift"]
        ].head(5).to_string()
    )

    # Question 14: Strong rules: confidence >= 0.7 and lift >= 1.2
    print("\n--- Q14: Strong rules (confidence >= 0.7, lift >= 1.2) ---")

    strong_rules_r = rules_r[
        (rules_r["confidence"] >= 0.7) & (rules_r["lift"] >= 1.2)
    ].sort_values("confidence", ascending=False)

    print(f"Number of strong rules: {len(strong_rules_r)}")
    print(
        strong_rules_r[
            ["antecedents", "consequents", "support", "confidence", "lift"]
        ].to_string()
    )

    # Question 15: Plot: min_support vs # itemsets
    print("\n--- Q15: Plot min_support vs # Itemsets (Online Retail) ---")

    supports_r = [0.01, 0.02, 0.03, 0.04, 0.05, 0.07, 0.10]
    counts_r = []
    for s in supports_r:
        its = fpgrowth(df_r, min_support=s, use_colnames=True)
        counts_r.append(len(its))
        print(f"  min_support={s:.2f}  ->  {len(its)} frequent itemsets")

    fig2, ax2 = plt.subplots(figsize=(9, 5))
    ax2.plot(supports_r, counts_r, marker="o", color="teal", linewidth=2)
    ax2.fill_between(supports_r, counts_r, alpha=0.15, color="teal")
    ax2.set_title(
        "Exercise 2 - Q15: min_support vs # Frequent Itemsets\n(Online Retail)",
        fontsize=13,
    )
    ax2.set_xlabel("min_support")
    ax2.set_ylabel("# Frequent Itemsets")
    ax2.grid(True, alpha=0.4)
    for x, y in zip(supports_r, counts_r):
        ax2.annotate(str(y), (x, y), textcoords="offset points", xytext=(0, 8), ha="center")
    plt.tight_layout()
    plt.savefig(EX2_PLOT_PATH, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  -> Plot saved: {EX2_PLOT_PATH.relative_to(PROJECT_ROOT).as_posix()}")


if __name__ == "__main__":
    run()
