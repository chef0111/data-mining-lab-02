def compute_support(itemset, transactions):
    """Support(X) = |{t : X subseteq t}| / |T|"""
    n = len(transactions)
    itemset_set = set(itemset)
    cnt = sum(1 for t in transactions if itemset_set.issubset(t))
    return cnt / n


def compute_confidence(x, y, transactions):
    """confidence(X -> Y) = support(X union Y) / support(X)"""
    sup_x = compute_support(list(x), transactions)
    sup_xy = compute_support(list(x) + list(y), transactions)
    return sup_xy / sup_x if sup_x > 0 else 0.0
