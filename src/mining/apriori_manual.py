def apriori_manual(transactions, min_support):
    """
    Pure-Python Apriori algorithm.
    Returns a list of dicts [{frozenset -> support}, ...] for each level k.
    """
    n = len(transactions)
    sets = [set(t) for t in transactions]  # pre-convert once for speed

    # Level 1
    all_items = set(i for t in transactions for i in t)
    cur_l = {}
    for item in all_items:
        cnt = sum(1 for s in sets if item in s)
        sup = cnt / n
        if sup >= min_support:
            cur_l[frozenset([item])] = sup

    levels = [cur_l]
    k = 2

    while cur_l:
        prev_keys = list(cur_l.keys())
        candidates = set()
        for i in range(len(prev_keys)):
            for j in range(i + 1, len(prev_keys)):
                union = prev_keys[i] | prev_keys[j]
                if len(union) == k:
                    # Apriori pruning
                    if all(frozenset(union - {x}) in cur_l for x in union):
                        candidates.add(union)

        new_l = {}
        for c in candidates:
            cnt = sum(1 for s in sets if c.issubset(s))
            sup = cnt / n
            if sup >= min_support:
                new_l[c] = sup

        if new_l:
            levels.append(new_l)
        cur_l = new_l
        k += 1

    return levels
