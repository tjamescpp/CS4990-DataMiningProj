import math

# DO NOT CHANGE THE FOLLOWING LINE
def apriori(itemsets, threshold):
    # DO NOT CHANGE THE PRECEDING LINE

    # Total number of itemsets
    n = len(itemsets)

    # Set containing frequent item sets which have reached the minimum support threshold
    selected_itemsets = set()

    # Traverse through the itemsets and create a set containing each individual item
    # Output frequent_items 
    frequent_items = set()
    for itemset in itemsets:
        for item in itemset:
            if item not in frequent_items:
                frequent_items.add(item)

    # while at least one frequent item reaches the min support
    while(True):
        for item in frequent_items:
            support = 0
            for itemset in itemsets:
                if item.issubset(itemset):
                    support += 1
            if (support / n) >= threshold:
                selected_itemsets.add(item)
                frequent_items.remove(item)
    
    # after iterating throught items, selected_itemsets contains the items which meet the support value and frequent_items contains the sets which do not
    


    
    

    
    # Should return a list of pairs, where each pair consists of the frequent itemset and its support 
    # e.g. [(set(items), 0.7), (set(otheritems), 0.74), ...]
    return []

    
# DO NOT CHANGE THE FOLLOWING LINE
def association_rules(itemsets, frequent_itemsets, metric, metric_threshold):
    # DO NOT CHANGE THE PRECEDING LINE
    
    # Should return a list of triples: condition, effect, metric value 
    # Each entry (c,e,m) represents a rule c => e, with the matric value m
    # Rules should only be included if m is greater than the given threshold.    
    # e.g. [(set(condition),set(effect),0.45), ...]
    return []
