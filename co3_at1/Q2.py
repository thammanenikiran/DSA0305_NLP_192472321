import re
from collections import Counter
corpus = """
Machine learning is a part of artificial intelligence.
Machine learning can analyze data.
Machine learning models learn patterns.
Artificial intelligence is changing the world.
Artificial intelligence helps people.
Natural language processing is a branch of artificial intelligence.
Natural language processing helps computers understand language.
Deep learning is a part of machine learning.
Deep learning models learn from data.
The computer learns patterns from data.
The model predicts the next word.
Language models predict words.
Students learn machine learning.
Students study artificial intelligence.
"""

def preprocess(text):

    sentences = re.split(r'[.!?]+', text.lower())
    result = []
    for sentence in sentences:
        words = re.findall(
            r'\b[a-z]+\b',
            sentence
        )

        if words:

            words = [
                "<s>"
            ] + words + [
                "</s>"
            ]

            result.append(words)

    return result


sentences = preprocess(corpus)
unigram = Counter()
bigram = Counter()
trigram = Counter()
for sentence in sentences:

    for word in sentence:
        unigram[word] += 1

    for i in range(len(sentence) - 1):

        bigram[
            (sentence[i], sentence[i + 1])
        ] += 1

    for i in range(len(sentence) - 2):

        trigram[
            (
                sentence[i],
                sentence[i + 1],
                sentence[i + 2]
            )
        ] += 1

def P1(word):

    total = sum(unigram.values())

    return unigram[word] / total
def P2(w1, w2):

    if unigram[w1] == 0:
        return 0
    return bigram[
        (w1, w2)
    ] / unigram[w1]


def P3(w1, w2, w3):

    if bigram[(w1, w2)] == 0:
        return 0

    return trigram[
        (w1, w2, w3)
    ] / bigram[(w1, w2)]

def unsmoothed(sentence):

    words = re.findall(
        r'\b[a-z]+\b',
        sentence.lower()
    )

    if len(words) < 2:
        return []

    w1 = words[-2]
    w2 = words[-1]

    result = []

    for word in unigram:

        if word in ["<s>", "</s>"]:
            continue

        probability = P3(
            w1,
            w2,
            word
        )

        if probability > 0:

            result.append(
                (word, probability)
            )

    result.sort(
        key=lambda x: x[1],
        reverse=True
    )

    return result[:5]

def backoff(sentence):

    words = re.findall(
        r'\b[a-z]+\b',
        sentence.lower()
    )

    if not words:
        return []

    w2 = words[-1]

    if len(words) >= 2:
        w1 = words[-2]
    else:
        w1 = None

    result = []

    for word in unigram:

        if word in ["<s>", "</s>"]:
            continue

        probability = 0

        # TRIGRAM
        if w1 is not None:

            probability = P3(
                w1,
                w2,
                word
            )

        # BIGRAM
        if probability == 0:

            probability = P2(
                w2,
                word
            )

        # UNIGRAM
        if probability == 0:

            probability = P1(word)

        result.append(
            (word, probability)
        )

    result.sort(
        key=lambda x: x[1],
        reverse=True
    )

    return result[:5]
def interpolation(sentence):

    words = re.findall(
        r'\b[a-z]+\b',
        sentence.lower()
    )

    if not words:
        return []

    w2 = words[-1]

    if len(words) >= 2:
        w1 = words[-2]
    else:
        w1 = None
    lambda1 = 0.2
    lambda2 = 0.3
    lambda3 = 0.5

    result = []

    for word in unigram:

        if word in ["<s>", "</s>"]:
            continue

        p1 = P1(word)

        p2 = P2(
            w2,
            word
        )

        p3 = 0

        if w1 is not None:

            p3 = P3(
                w1,
                w2,
                word
            )

        probability = (
            lambda1 * p1
            +
            lambda2 * p2
            +
            lambda3 * p3
        )

        result.append(
            (word, probability)
        )

    result.sort(
        key=lambda x: x[1],
        reverse=True
    )

    return result[:5]
def display(title, predictions):

    print("\n------------------------------")
    print(title)
    print("------------------------------")

    if not predictions:

        print("No prediction available.")

    else:

        for word, probability in predictions:

            print(
                f"{word:15} "
                f"{probability:.4f}"
            )

while True:

    print("\n======================================")
    print(" BACKOFF & INTERPOLATION MODEL")
    print("======================================")

    print("1. Unsmoothed N-gram")
    print("2. Backoff Model")
    print("3. Deleted Interpolation")
    print("4. Compare All")
    print("5. Exit")

    choice = input(
        "\nEnter your choice: "
    )

    if choice == "1":

        sentence = input(
            "Enter incomplete sentence: "
        )

        display(
            "UNSMOOTHED MODEL",
            unsmoothed(sentence)
        )

    elif choice == "2":

        sentence = input(
            "Enter incomplete sentence: "
        )

        display(
            "BACKOFF MODEL",
            backoff(sentence)
        )

    elif choice == "3":

        sentence = input(
            "Enter incomplete sentence: "
        )

        display(
            "DELETED INTERPOLATION",
            interpolation(sentence)
        )

    elif choice == "4":

        sentence = input(
            "Enter incomplete sentence: "
        )

        display(
            "UNSMOOTHED",
            unsmoothed(sentence)
        )

        display(
            "BACKOFF",
            backoff(sentence)
        )

        display(
            "INTERPOLATION",
            interpolation(sentence)
        )

    elif choice == "5":

        print("Program terminated.")
        break

    else:

        print("Invalid choice.")
