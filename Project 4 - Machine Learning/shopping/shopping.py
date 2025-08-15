import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    evidence = []
    labels = []

    # Open the csv file
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        # Get the column names
        fieldnames = reader.fieldnames

        for row in reader:
            # Append only the first 17 columns to evidence
            evidence.append([lookup(name, row[name]) for name in fieldnames[:17]])
            # Labels should be the remaining. In this case we know it is only revenue so we ask for it directly
            labels.append(lookup("Revenue", row["Revenue"]))
    return evidence, labels


def lookup(name, value):
    """
    Auxiliar function for the lookup tables needed to implement correctly the data types.

    Returns an output value after converting the input.

    """
    monthTable = {
        "Jan": 0,
        "Feb": 1,
        "Mar": 2,
        "Apr": 3,
        "May": 4,
        "June": 5,
        "Jul": 6,
        "Aug": 7,
        "Sep": 8,
        "Oct": 9,
        "Nov": 10,
        "Dec": 11,
    }
    typeTable = {
        "Administrative": int,
        "Administrative_Duration": float,
        "Informational": int,
        "Informational_Duration": float,
        "ProductRelated": int,
        "ProductRelated_Duration": float,
        "BounceRates": float,
        "ExitRates": float,
        "PageValues": float,
        "SpecialDay": float,
        "Month": lambda v: int(monthTable[v]),
        "OperatingSystems": int,
        "Browser": int,
        "Region": int,
        "TrafficType": int,
        "VisitorType": lambda v: 1 if v == "Returning_Visitor" else 0,
        "Weekend": lambda v: 1 if v == "TRUE" else 0,
        "Revenue": lambda v: 1 if v == "TRUE" else 0,
    }
    conversionFunction = typeTable[name]
    return conversionFunction(value)


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    # Get the classifier object
    classifier = KNeighborsClassifier(n_neighbors=1)
    # Apply to the data set
    classifier.fit(evidence, labels)
    return classifier


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    truePositives = 0
    trueNegatives = 0

    # Iterate both lists and add count to specificity and sensitivity
    for actual, pred in zip(labels, predictions):
        if actual == 1 and pred == 1:
            truePositives += 1
        elif actual == 0 and pred == 0:
            trueNegatives += 1

    # Normalize sensitivity and specificity. We know we have at least one of each
    positiveCount = 0
    negativeCount = 0
    for label in labels:
        if label == 1:
            positiveCount += 1
        else:
            negativeCount += 1

    sensitivity = float(truePositives / positiveCount)
    specificity = float(trueNegatives / negativeCount)

    return sensitivity, specificity

if __name__ == "__main__":
    main()
