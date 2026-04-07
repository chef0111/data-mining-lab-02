from collections import Counter
from itertools import combinations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from mlxtend.frequent_patterns import apriori as mlxtend_apriori
from mlxtend.frequent_patterns import association_rules, fpgrowth
from mlxtend.preprocessing import TransactionEncoder

from src.config import (
    EX1_OUTPUT_PATH,
    EX1_PLOT_PATH,
    GROCERIES_PATH,
    PROJECT_ROOT,
    ensure_output_dirs,
)
from src.io.loaders import load_groceries_transactions
from src.io.output_capture import setup_output_capture
from src.mining.apriori_manual import apriori_manual


def run():
    ensure_output_dirs()
    setup_output_capture(EX1_OUTPUT_PATH)

    # ================================================================
    # EXERCISE 1 - groceries.csv
    # ================================================================
    print("=" * 65)
    print("EXERCISE 1: groceries.csv")
    print("=" * 65)

    # Question 1: Read groceries.csv into transactions
    print("\n--- Q1: Read groceries.csv into transactions ---")

    transactions = load_groceries_transactions(GROCERIES_PATH)

    num_transactions = len(transactions)
    all_items_flat = [item for t in transactions for item in t]
    num_items = len(all_items_flat)

    print(f"Number of transactions : {num_transactions}")
    print(f"Total number of items  : {num_items}")
    print(f"Sample transaction[0]  : {transactions[0]}")

    # Question 2: Unique items & top-10 most frequent items
    print("\n--- Q2: Unique items & top-10 most frequent ---")

    unique_items = set(all_items_flat)
    counter = Counter(all_items_flat)
    top10 = counter.most_common(10)

    print(f"Number of unique items : {len(unique_items)}")
    print("\nTop 10 most frequent items:")
    for rank, (item, cnt) in enumerate(top10, 1):
        print(f"  {rank:2d}. {item:<35s} count={cnt}")

    # Question 3: Support of 1-itemsets
    print("\n--- Q3: Support of 1-itemsets (top-10 shown) ---")

    support_1 = {}
    for item in unique_items:
        count = sum(1 for t in transactions if item in t)
        support_1[item] = count / num_transactions

    top10_sup = sorted(support_1.items(), key=lambda x: -x[1])[:10]
    for item, sup in top10_sup:
        print(f"  {item:<35s} support={sup:.4f}")

    # Question 4: Frequent 1-itemsets with min_support=0.01
    print("\n--- Q4: Frequent 1-itemsets (min_support=0.01) ---")

    min_support = 0.01
    l1 = {item: sup for item, sup in support_1.items() if sup >= min_support}
    print(f"Number of frequent 1-itemsets: {len(l1)}")
    for item, sup in sorted(l1.items(), key=lambda x: -x[1])[:5]:
        print(f"  {item:<35s} support={sup:.4f}")

    # Question 5: Candidate & frequent 2-itemsets
    print("\n--- Q5: Candidate & frequent 2-itemsets ---")

    items_l1 = list(l1.keys())
    c2 = list(combinations(items_l1, 2))
    support_2 = {}
    for pair in c2:
        count = sum(1 for t in transactions if set(pair).issubset(t))
        support_2[pair] = count / num_transactions

    l2 = {pair: sup for pair, sup in support_2.items() if sup >= min_support}
    print(f"Candidate 2-itemsets : {len(c2)}")
    print(f"Frequent 2-itemsets  : {len(l2)}")
    for pair, sup in sorted(l2.items(), key=lambda x: -x[1])[:5]:
        print(f"  {set(pair)}  support={sup:.4f}")

    # Question 7: Print intermidiate steps of Apriori
    print("\n--- Q6 & Q7: Apriori algorithm (min_support=0.01) ---")

    frequent_levels = apriori_manual(transactions, min_support=0.01)

    for i, level in enumerate(frequent_levels):
        print(f"\n  L{i+1}  ({len(level)} itemsets)")
        for itemset, sup in sorted(level.items(), key=lambda x: -x[1])[:3]:
            print(f"    {set(itemset)}  support={sup:.4f}")
        if len(level) > 3:
            print(f"    ... ({len(level) - 3} more)")

    # Question 8: One-hot encoding using TransactionEncoder
    print("\n--- Q8: One-hot encoding ---")

    te = TransactionEncoder()
    te_array = te.fit(transactions).transform(transactions)
    df = pd.DataFrame(te_array, columns=te.columns_)
    print(f"Shape: {df.shape}")
    print(df.iloc[:3, :6])

    # Question 9: mlxtend Apriori
    print("\n--- Q9: mlxtend Apriori (min_support=0.01) ---")

    fi_apriori = mlxtend_apriori(df, min_support=0.01, use_colnames=True)
    print(f"Frequent itemsets: {len(fi_apriori)}")
    print(fi_apriori.sort_values("support", ascending=False).head(5).to_string())

    # Question 10: mlxtend FP-Growth
    print("\n--- Q10: mlxtend FP-Growth (min_support=0.01) ---")

    fi_fp = fpgrowth(df, min_support=0.01, use_colnames=True)
    print(f"Frequent itemsets: {len(fi_fp)}")
    print(fi_fp.sort_values("support", ascending=False).head(5).to_string())

    # Question 11: Association rules
    print("\n--- Q11: Association rules (min_confidence=0.2) ---")

    rules = association_rules(fi_fp, metric="confidence", min_threshold=0.2)
    print(f"Total rules: {len(rules)}")
    print(
        rules[
            ["antecedents", "consequents", "support", "confidence", "lift"]
        ].head(5).to_string()
    )

    # Question 12: Filter top-10 rules by confidence
    print("\n--- Q12: Top 10 rules by confidence ---")

    rules_sorted = rules.sort_values("confidence", ascending=False)
    print(
        rules_sorted[
            ["antecedents", "consequents", "support", "confidence", "lift"]
        ]
        .head(10)
        .to_string()
    )

    # Question 13: Rules whose consequent is "whole milk"
    print("\n--- Q13: Rules with consequent = 'whole milk' ---")

    rules_milk = rules[rules["consequents"].apply(lambda x: "whole milk" in x)]
    rules_milk = rules_milk.sort_values("confidence", ascending=False)
    print(f"Rules → whole milk: {len(rules_milk)}")
    print(
        rules_milk[
            ["antecedents", "consequents", "support", "confidence", "lift"]
        ]
        .head(10)
        .to_string()
    )

    # Question 14: Effect of min_support and min_confidence on item/rule counts
    print("\n--- Q14: Effect of thresholds ---")

    supports_ex1 = [0.01, 0.02, 0.03, 0.05]
    itemset_counts = []
    for s in supports_ex1:
        its = mlxtend_apriori(df, min_support=s, use_colnames=True)
        itemset_counts.append(len(its))
        print(f"  min_support={s:.2f}  ->  {len(its)} frequent itemsets")

    confidences = [0.2, 0.4, 0.6, 0.8]
    rule_counts = []
    for c in confidences:
        r = association_rules(fi_apriori, metric="confidence", min_threshold=c)
        rule_counts.append(len(r))
        print(f"  min_conf={c:.1f}      ->  {len(r)} rules")

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle(
        "Exercise 1 - Q14: Threshold Effects (Groceries)",
        fontsize=13,
        fontweight="bold",
    )

    axes[0].plot(
        supports_ex1,
        itemset_counts,
        marker="o",
        color="steelblue",
        linewidth=2,
    )
    axes[0].set_title("min_support vs # Frequent Itemsets")
    axes[0].set_xlabel("min_support")
    axes[0].set_ylabel("# Frequent Itemsets")
    axes[0].grid(True, alpha=0.4)
    for x, y in zip(supports_ex1, itemset_counts):
        axes[0].annotate(str(y), (x, y), textcoords="offset points", xytext=(0, 8), ha="center")

    axes[1].plot(
        confidences,
        rule_counts,
        marker="s",
        color="darkorange",
        linewidth=2,
    )
    axes[1].set_title("min_confidence vs # Rules")
    axes[1].set_xlabel("min_confidence")
    axes[1].set_ylabel("# Rules")
    axes[1].grid(True, alpha=0.4)
    for x, y in zip(confidences, rule_counts):
        axes[1].annotate(str(y), (x, y), textcoords="offset points", xytext=(0, 8), ha="center")

    plt.tight_layout()
    plt.savefig(EX1_PLOT_PATH, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  -> Plot saved: {EX1_PLOT_PATH.relative_to(PROJECT_ROOT).as_posix()}")


if __name__ == "__main__":
    run()
