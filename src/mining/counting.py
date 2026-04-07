from collections import Counter
from itertools import combinations


def frequent_1_itemsets(transaction_sets, min_support):
    n_transactions = len(transaction_sets)
    item_counter = Counter()
    for t_set in transaction_sets:
        item_counter.update(t_set)

    frequent_1 = {
        item: count / n_transactions
        for item, count in item_counter.items()
        if (count / n_transactions) >= min_support
    }
    return frequent_1


def frequent_2_itemsets(transaction_sets, frequent_1, min_support):
    n_transactions = len(transaction_sets)
    pair_counter = Counter()
    frequent_1_items = set(frequent_1)

    for t_set in transaction_sets:
        items_in_t = sorted(t_set & frequent_1_items)
        if len(items_in_t) >= 2:
            pair_counter.update(combinations(items_in_t, 2))

    frequent_2 = {}
    for pair, count in pair_counter.items():
        sup = count / n_transactions
        if sup >= min_support:
            frequent_2[pair] = sup

    return frequent_2
