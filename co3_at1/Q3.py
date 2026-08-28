import re
import math
from collections import Counter
training_text = """
The cat sits on the mat.
The cat eats food.
The dog sits on the mat.
The dog eats food.
The student reads a book.
The student learns language.
Machine learning is useful.
Machine learning learns from data.
Artificial intelligence is useful.
Natural language processing analyzes text.
The computer processes data.
Language models predict words.
"""
testing_text = """
The cat sits on the mat.
The dog eats food.
The quantum processor redesigned the system.
Machine learning predicts words.
"""
def preprocess(text):

    sentences = re.split(
        r'[.!?]+',
        text.lower()
    )

    result = []

    for sentence in sentences:

        words = re.findall(
            r'\b[a-z]+\b',
            sentence
        )

        if words:

            result.append(
                ["<s>"] +
                words +
                ["</s>"]
            )

    return result


train = preprocess(
    training_text
)

test = preprocess(
    testing_text
)


# =========================================================
# BUILD MODELS
# =========================================================

unigram = Counter()
bigram = Counter()
trigram = Counter()

for sentence in train:

    for word in sentence:
        unigram[word] += 1

    for i in range(len(sentence) - 1):

        bigram[
            (
                sentence[i],
                sentence[i + 1]
            )
        ] += 1

    for i in range(len(sentence) - 2):

        trigram[
            (
                sentence[i],
                sentence[i + 1],
                sentence[i + 2]
            )
        ] += 1
def p_unigram(word):

    total = sum(unigram.values())

    return unigram[word] / total


def p_bigram(w1, w2):

    if unigram[w1] == 0:
        return 0

    return (
        bigram[(w1, w2)]
        /
        unigram[w1]
    )


def p_trigram(w1, w2, w3):

    if bigram[(w1, w2)] == 0:
        return 0

    return (
        trigram[(w1, w2, w3)]
        /
        bigram[(w1, w2)]
    )

vocabulary = set(unigram.keys())

V = len(vocabulary)


def smoothed_bigram(w1, w2):

    return (
        bigram[(w1, w2)] + 1
    ) / (
        unigram[w1] + V
    )

def entropy_unigram(sentence):

    probabilities = []

    for word in sentence:

        if word in ["<s>", "</s>"]:
            continue

        probability = p_unigram(word)

        if probability > 0:
            probabilities.append(
                probability
            )

    if not probabilities:
        return float("inf")

    entropy = 0

    for p in probabilities:

        entropy += -math.log2(p)

    return entropy / len(
        probabilities
    )


def entropy_bigram(sentence):

    probabilities = []

    for i in range(1, len(sentence)):

        word = sentence[i]
        previous = sentence[i - 1]

        probability = p_bigram(
            previous,
            word
        )

        if probability > 0:

            probabilities.append(
                probability
            )

        else:

            return float("inf")

    if not probabilities:
        return float("inf")

    entropy = 0

    for p in probabilities:

        entropy += -math.log2(p)

    return entropy / len(
        probabilities
    )


def entropy_trigram(sentence):

    probabilities = []

    for i in range(2, len(sentence)):

        w1 = sentence[i - 2]
        w2 = sentence[i - 1]
        w3 = sentence[i]

        probability = p_trigram(
            w1,
            w2,
            w3
        )

        if probability > 0:

            probabilities.append(
                probability
            )

        else:

            return float("inf")

    if not probabilities:
        return float("inf")

    entropy = 0

    for p in probabilities:

        entropy += -math.log2(p)

    return entropy / len(
        probabilities
    )


def entropy_smoothed(sentence):

    probabilities = []

    for i in range(1, len(sentence)):

        previous = sentence[i - 1]
        word = sentence[i]

        probability = smoothed_bigram(
            previous,
            word
        )

        probabilities.append(
            probability
        )

    entropy = 0

    for p in probabilities:

        entropy += -math.log2(p)

    return entropy / len(
        probabilities
    )

def classify(entropy):

    if entropy == float("inf"):
        return "HIGH UNCERTAINTY"

    if entropy > 4:
        return "HIGH UNCERTAINTY"

    return "LOW UNCERTAINTY"

def show_result(sentence):

    print("\n====================================")
    print(
        "Sentence:",
        " ".join(sentence)
    )
    print("====================================")

    e1 = entropy_unigram(sentence)
    e2 = entropy_bigram(sentence)
    e3 = entropy_trigram(sentence)
    es = entropy_smoothed(sentence)

    print(
        "Unigram Entropy :",
        e1
    )

    print(
        "Bigram Entropy  :",
        e2
    )

    print(
        "Trigram Entropy :",
        e3
    )

    print(
        "Smoothed Entropy:",
        es
    )

    print("\nClassification:")

    print(
        "Unigram :",
        classify(e1)
    )

    print(
        "Bigram  :",
        classify(e2)
    )

    print(
        "Trigram :",
        classify(e3)
    )

    print(
        "Smoothed:",
        classify(es)
    )
while True:

    print("\n======================================")
    print(" ENTROPY BASED LANGUAGE MODEL")
    print("======================================")

    print("1. Evaluate test corpus")
    print("2. Enter your own sentence")
    print("3. Exit")

    choice = input(
        "\nEnter your choice: "
    )

    if choice == "1":

        for sentence in test:

            show_result(sentence)

    elif choice == "2":

        sentence = input(
            "\nEnter sentence: "
        )

        processed = preprocess(
            sentence
        )

        if processed:

            show_result(
                processed[0]
            )

    elif choice == "3":

        print("Program terminated.")
        break

    else:

        print("Invalid choice.")
