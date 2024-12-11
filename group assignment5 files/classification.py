import numpy
import math


# These are suggested helper functions
# You can structure your code differently, but if you have
# trouble getting started, this might be a good starting point

# Create the decision tree recursively
def make_node(previous_ys, xs, ys, columns):
    # WARNING: lists are passed by reference in python
    # If you are planning to remove items, it's better
    # to create a copy first
    columns = columns[:]

    # First, check the three termination criteria:

    # If there are no rows (xs and ys are empty):
    #      Return a node that classifies as the majority class of the parent
    if not xs:
        return {"type": "class", "class": majority(previous_ys)}

    # If all ys are the same:
    #      Return a node that classifies as that class
    if same(ys):
        return {"type": "class", "class": ys[0]}

    # If there are no more columns left:
    #      Return a node that classifies as the majority class of the ys
    if not columns:
        return {"type": "class", "class": majority(ys)}

    # Otherwise:
    # Compute the entropy of the current ys
    # For each column:
    #     Perform a split on the values in that column
    #     Calculate the entropy of each of the pieces
    #     Compute the overall entropy as the weighted sum
    #     The gain of the column is the difference of the entropy before
    #        the split, and this new overall entropy
    # Select the column with the highest gain, then:
    # Split the data along the column values and recursively call
    #    make_node for each piece
    # Create a split-node that splits on this column, and has the result
    #    of the recursive calls as children.

    current_entropy = entropy(ys)

    best_column = None
    best_gain = 0
    best_splits = None

    for column in columns:
        # Perform a split on the values in that column
        splits = {}
        for i, value in enumerate(xs):
            if value[column] not in splits:
                splits[value[column]] = [[], []]
            splits[value[column]][0].append(xs[i])
            splits[value[column]][1].append(ys[i])

        # Calculate the entropy of each of the pieces
        # Compute the overall entropy as the weighted sum
        total_entropy = 0
        for split in splits.values():
            # Slide's formula for gain split
            total_entropy += len(split[1]) / len(ys) * entropy(split[1])

        # The gain of the column is the difference of the entropy before the split, and this new overall entropy
        gain = current_entropy - total_entropy
        if gain > best_gain:
            best_column = column
            best_gain = gain
            best_splits = splits

    # Select the column with the highest gain
    # Note: This is a placeholder return value
    if best_column is None:
        return {"type": "class", "class": majority(ys)}

    # Split the data along the column values and recursively call make_node for each piece
    new_columns = columns[:]
    new_columns.remove(best_column)
    children = {}
    for value, split in best_splits.items():
        children[value] = make_node(ys, split[0], split[1], new_columns)

    # Create a split-node that splits on this column, and has the result of the recursive calls as children
    return {"type": "split", "column": best_column, "children": children}


# Determine if all values in a list are the same
# Useful for the second basecase above
def same(values):
    if not values:
        return True
    # if there are values:
    # pick the first, check if all other are the same

    first = values[0]
    for value in values:
        if value != first:
            return False
    return True


# Determine how often each value shows up
# in a list; this is useful for the entropy
# but also to determine which values is the
# most common
def counts(values):
    count_dict = {}
    for value in values:
        if value not in count_dict:
            count_dict[value] = 0
        count_dict[value] += 1

    # placeholder return value
    return count_dict


# Return the most common value from a list
# Useful for base cases 1 and 3 above.
def majority(values):
    count_dict = counts(values)
    max_count = 0
    max_value = None
    for value, count in count_dict.items():
        if count > max_count:
            max_count = count
            max_value = value

    # placeholder return value
    return max_value


# Calculate the entropy of a set of values
# First count how often each value shows up
# When you divide this value by the total number
# of elements, you get the probability for that element
# The entropy is the negation of the sum of p*log2(p)
# for all these probabilities.
def entropy(values):
    total = len(values)
    if total == 0:
        return 0
    count_dict = counts(values)

    # Formula for entropy based on slides: Entropy = -sum(p*log2(p)) and p = count/total
    # placeholder return value
    return -sum((count/total) * math.log2(count/total) for count in count_dict.values())

# This is the main decision tree class
# DO NOT CHANGE THE FOLLOWING LINE


class DecisionTree:
    # DO NOT CHANGE THE PRECEDING LINE
    def __init__(self, tree={}):
        self.tree = tree

    # DO NOT CHANGE THE FOLLOWING LINE
    def fit(self, x, y):
        # DO NOT CHANGE THE PRECEDING LINE

        self.majority = majority(y)
        self.tree = make_node(y, x, y, list(range(len(x[0]))))

    # DO NOT CHANGE THE FOLLOWING LINE
    def predict(self, x):
        # DO NOT CHANGE THE PRECEDING LINE
        if not self.tree:
            return None

        predicted_labels = []

        # To classify using the tree:
        for instance in x:
            current_node = self.tree
        # Start with the root as the "current" node
        # As long as the current node is an interior node (type == "split"):
            while current_node["type"] == "split":
                #    get the value of the attribute the split is performed on
                attribute = current_node['column']
        #    select the child corresponding to that value as the new current node
                x_attribute = instance[attribute]

                if x_attribute in current_node["children"]:
                    current_node = current_node["children"][x_attribute]

        # NOTE: In some cases, your tree may not have a child for a particular value
        #       In that case, return the majority value (self.majority) from the training set
                else:
                    current_node = {"type": "class", "class": self.majority}

        # IMPORTANT: You have to perform this classification *for each* element in x
            predicted_labels.append(current_node["class"])
        # placeholder return value
        # Note that the result is a list of predictions, one for each x-value
        return predicted_labels

    # DO NOT CHANGE THE FOLLOWING LINE
    def to_dict(self):
        # DO NOT CHANGE THE PRECEDING LINE
        # change this if you store the tree in a different format
        return self.tree
