import math
from itertools import combinations

DEBUG = True

# DO NOT CHANGE THE FOLLOWING LINE
def apriori(itemsets, threshold):
    # DO NOT CHANGE THE PRECEDING LINE

    # given number of items per set (n), traverse through a series of sets and create new sets of size n
    # condition to join sets: must have n-2 elements in common
    # return the newly created sets
    def find_itemsets(itemsets, n):
        itemset_list = list(itemsets)
        new_itemsets = set()
        for i in range(len(itemset_list)):
            for j in range(i + 1, len(itemset_list)):
                if len(set(itemset_list[i]).intersection(set(itemset_list[j]))) == (n - 2):
                    new_itemsets.add(set((itemset_list[i])).union(set(itemset_list[j])))

        return new_itemsets


    # given a series of itemsets and a series of non frequent itemsets, remove all sets which contain a subset of non frequent itemsets
    def prune(itemsets, non_frequent_itemsets):
        if len(non_frequent_itemsets) == 0:
            return itemsets
        
        pruned_itemsets = set()
        
        for itemset in itemsets:
            flag = False
            for non_frequent_itemset in non_frequent_itemsets:
                if itemset.intersection(non_frequent_itemset) == non_frequent_itemset:
                    flag = True
                    break
            if not flag:
                pruned_itemsets.add(itemset)
        
        return pruned_itemsets


    # Total number of itemsets
    n = len(itemsets)

    # Set containing frequent item sets which have reached the minimum support threshold
    selected_itemsets = set()

    # Traverse through the itemsets and create a set containing each individual item
    # Output frequent_items 
    initial_items = set()
    for itemset in itemsets:
        for item in itemset:
            initial_items
    # while at least one frequent item reaches the min support
    frequent_items = set()
    for i in range(2, len(itemsets)):
        for item in initial_items:
            support = 0
            for itemset in itemsets:
                if item in itemset:
                    support += 1
            if (support / n) >= threshold:
                frequent_items.add(item)
                initial_items.remove(item)
    
        # Create new itemsets of size +1
        frequent_items_temp = find_itemsets(frequent_items, i)

        # if frequent_items_temp is empty, break out of the loop 
        if len(frequent_items_temp) == 0:
            break

        # prune the itemsets
        frequent_items_temp = prune(frequent_items_temp, initial_items)

        # if frequent_items_temp is empty, break out of the loop 
        if len(frequent_items_temp) == 0:
            break
        
        # set up for the next iteration
        initial_items = frequent_items_temp
        frequent_items = frequent_items_temp
    


    final_frequent_items = []
    for i in range(2, len(itemsets)):
        for item in initial_items:
            support = 0
            for itemset in itemsets:
                if item in itemset:
                    support += 1
            final_frequent_items.append(item, (support/n))

    
    # Should return a list of pairs, where each pair consists of the frequent itemset and its support 
    # e.g. [(set(items), 0.7), (set(otheritems), 0.74), ...]
    return final_frequent_items

    
# DO NOT CHANGE THE FOLLOWING LINE
def association_rules(itemsets, frequent_itemsets, metric, metric_threshold):
    # DO NOT CHANGE THE PRECEDING LINE
    
    # Should return a list of triples: condition, effect, metric value 
    # Each entry (c,e,m) represents a rule c => e, with the matric value m
    # Rules should only be included if m is greater than the given threshold.    
    # e.g. [(set(condition),set(effect),0.45), ...]
    
        rules = []

        # Note: Association rule formulas are based on the textbook.
        # Helper function to calculate the support of a set of items
        # Subset is a set of items
        # Itemsets is a list of sets, each representing a transaction
        def calculate_support(subset, itemsets):
            count = 0
            for itemset in itemsets:
                if subset.issubset(itemset):
                    count += 1
            return count / len(itemsets)

        # Helper function to calculate the confidence of a rule
        # X and Y are itemsets
        def calculate_confidence(X, Y):
            return calculate_support(X | Y, itemsets) / calculate_support(X, itemsets)

        # Helper function to calculate the lift of a rule
        def calculate_lift(X, Y):
            return calculate_support(X | Y, itemsets) / (calculate_support(X, itemsets) * calculate_support(Y, itemsets))

        # Helper function to calculate the conviction of a rule
        def calculate_all_confidence(X, Y):
            return calculate_support(X | Y, itemsets) / max(calculate_support(X, itemsets), calculate_support(Y, itemsets))

        # Helper function to calculate the max confidence of a rule
        def calculate_max_confidence(X, Y):
            return max(calculate_all_confidence(X, Y), calculate_all_confidence(Y, X))

        # Helper function to calculate kulczynski of a rule (average of lift and confidence)
        def calculate_kulczynski(X, Y):
            return (calculate_confidence(X, Y) + calculate_confidence(Y, X)) / 2

        # Helper function to calculate the cosine of a rule
        def calculate_cosine(X, Y):
            return calculate_support(X | Y, itemsets) / math.sqrt(calculate_support(X, itemsets) * calculate_support(Y, itemsets))

        # Iterate over frequent itemsets
        for freq_set, support in frequent_itemsets:
            if len(freq_set) < 2:
                continue  # No rule possible with single item
            
            # Generate all possible antecedents and consequents
            for size in range(1, len(freq_set)):
                for antecedent in combinations(freq_set, size):
                    antecedent = set(antecedent)
                    consequent = freq_set - antecedent

                    if not consequent:
                        continue

                    # Compute the metric
                    if metric == "lift":
                        m_value = calculate_lift(antecedent, consequent)
                    elif metric == "all_conf":
                        m_value = calculate_all_confidence(antecedent, consequent)
                    elif metric == "max_conf":
                        m_value = calculate_max_confidence(antecedent, consequent)
                    elif metric == "kulczynski":
                        m_value = calculate_kulczynski(antecedent, consequent)
                    elif metric == "cosine":
                        m_value = calculate_cosine(antecedent, consequent)
                    else:
                        raise ValueError("Unknown metric: " + metric)

                    # Append rule if metric exceeds threshold
                    if m_value >= metric_threshold:
                        rules.append((antecedent, consequent, m_value))

        return rules

# TEST CASES (def association_rules)
if DEBUG:
    itemsets = [
        {"A", "B", "C"},
        {"A", "B"},
        {"A", "C"},
        {"B", "C"},
        {"A", "B", "C", "D"}
    ]

    frequent_itemsets = [
        ({"A", "B"}, 0.6),
        ({"A", "C"}, 0.6),
        ({"B", "C"}, 0.8),
        ({"A", "B", "C"}, 0.4)
    ]

    # Rules with Lift metric
    rules_lift = association_rules(itemsets, frequent_itemsets, metric="lift", metric_threshold=1.0)
    print("Rules with Lift Metric:", rules_lift)
    # Rules with All Confidence metric
    rules_all_conf = association_rules(itemsets, frequent_itemsets, metric="all_conf", metric_threshold=0.5)
    print("Rules with All Confidence Metric:", rules_all_conf)
    # Rules with Max Confidence metric
    rules_max_conf = association_rules(itemsets, frequent_itemsets, metric="max_conf", metric_threshold=0.7)
    print("Rules with Max Confidence Metric:", rules_max_conf)
    # Rules with Kulczynski metric
    rules_kulczynski = association_rules(itemsets, frequent_itemsets, metric="kulczynski", metric_threshold=0.6)
    print("Rules with Kulczynski Metric:", rules_kulczynski)
    # Rules with Cosine metric
    rules_cosine = association_rules(itemsets, frequent_itemsets, metric="cosine", metric_threshold=0.5)
    print("Rules with Cosine Metric:", rules_cosine)