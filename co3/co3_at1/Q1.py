import re
from collections import Counter, defaultdict
corpus = """
Artificial intelligence is changing the world.
Artificial intelligence helps people solve complex problems.
Machine learning is a part of artificial intelligence.
Machine learning can analyze large amounts of data.
Natural language processing helps computers understand language.
Natural language processing is used in many applications.
Deep learning is a powerful technique in artificial intelligence.
Deep learning can solve difficult problems.
Students learn artificial intelligence and machine learning.
Students use natural language processing for text analysis.
Language models predict the next word in a sentence.
Language models are useful for speech and text prediction.
The computer learns patterns from the training data.
The model predicts words using previous words.
Machine learning models learn from data.
Artificial intelligence and machine learning are important technologies.
"""

def preprocess(text):
    sentences = re.split(r'[.!?]+', text.lower())

    processed_sentences = []

    for sentence in sentences:
        words = re.findall(r'\b[a-z]+\b', sentence)

        if words:
            words = ["<s>"] + words + ["</s>"]
            processed_sentences.append(words)

    return processed_sentences


sentences = preprocess(corpus)

unigram = Counter()
bigram = Counter()
trigram = Counter()

for sentence in sentences:

    # Unigram
    for word in sentence:
        unigram[word] += 1

    # Bigram
    for i in range(len(sentence) - 1):
        pair = (sentence[i], sentence[i + 1])
        bigram[pair] += 1

    # Trigram
    for i in range(len(sentence) - 2):
        triple = (
            sentence[i],
            sentence[i + 1],
            sentence[i + 2]
        )
        trigram[triple] += 1

def unigram_probability(word):
    total = sum(unigram.values())

    if unigram[word] == 0:
        return 0

    return unigram[word] / total


def bigram_probability(w1, w2):
    denominator = unigram[w1]

    if denominator == 0:
        return 0

    return bigram[(w1, w2)] / denominator


def trigram_probability(w1, w2, w3):
    denominator = bigram[(w1, w2)]

    if denominator == 0:
        return 0

    return trigram[(w1, w2, w3)] / denominator

def display_counts(n):

    print("\n------------------------------")
    print(f"{n}-GRAM FREQUENCY COUNTS")
    print("------------------------------")

    if n == 1:

        for word, count in unigram.items():
            print(word, ":", count)

    elif n == 2:

        for words, count in bigram.items():
            print(words, ":", count)

    elif n == 3:

        for words, count in trigram.items():
            print(words, ":", count)
def display_probabilities(n):

    print("\n------------------------------")
    print(f"{n}-GRAM PROBABILITIES")
    print("------------------------------")

    if n == 1:

        for word in unigram:
            print(
                word,
                "=>",
                round(unigram_probability(word), 4)
            )

    elif n == 2:

        for (w1, w2) in bigram:
            print(
                (w1, w2),
                "=>",
                round(bigram_probability(w1, w2), 4)
            )

    elif n == 3:

        for (w1, w2, w3) in trigram:
            print(
                (w1, w2, w3),
                "=>",
                round(
                    trigram_probability(w1, w2, w3),
                    4
                )
            )
def predict_next_word(sentence, n=3):

    words = re.findall(r'\b[a-z]+\b', sentence.lower())

    if not words:
        return []

    predictions = []
    if n == 1:

        for word, count in unigram.most_common():

            if word not in ["<s>", "</s>"]:
                predictions.append(
                    (word, unigram_probability(word))
                )

    elif n == 2:

        last_word = words[-1]

        for (w1, w2), count in bigram.items():

            if w1 == last_word and w2 not in ["<s>", "</s>"]:

                probability = bigram_probability(w1, w2)

                predictions.append(
                    (w2, probability)
                )

    elif n == 3:

        if len(words) < 2:
            return []

        w1 = words[-2]
        w2 = words[-1]

        for (a, b, c), count in trigram.items():

            if a == w1 and b == w2:

                if c not in ["<s>", "</s>"]:

                    probability = trigram_probability(
                        a, b, c
                    )

                    predictions.append(
                        (c, probability)
                    )

    predictions.sort(
        key=lambda x: x[1],
        reverse=True
    )

    return predictions[:5]

def calculate_accuracy(test_cases, n):

    correct = 0

    for sentence, actual_word in test_cases:

        predictions = predict_next_word(sentence, n)

        predicted_words = [
            word for word, probability in predictions
        ]

        if actual_word.lower() in predicted_words:
            correct += 1

    if len(test_cases) == 0:
        return 0

    return (correct / len(test_cases)) * 100
while True:

    print("\n======================================")
    print("       N-GRAM LANGUAGE MODEL")
    print("======================================")

    print("1. Display Unigram")
    print("2. Display Bigram")
    print("3. Display Trigram")
    print("4. Predict Next Word")
    print("5. Test Prediction Accuracy")
    print("6. Exit")

    choice = input("\nEnter your choice: ")
    if choice == "1":

        display_counts(1)
        display_probabilities(1)

    elif choice == "2":

        display_counts(2)
        display_probabilities(2)
    elif choice == "3":

        display_counts(3)
        display_probabilities(3)
    elif choice == "4":

        sentence = input(
            "\nEnter incomplete sentence: "
        )

        print("\nSelect N-gram:")
        print("1. Unigram")
        print("2. Bigram")
        print("3. Trigram")

        n = int(input("Enter N: "))

        predictions = predict_next_word(
            sentence,
            n
        )

        print("\nTop-5 Predictions:")

        if not predictions:

            print(
                "No prediction available "
                "for this sentence."
            )

        else:

            for word, probability in predictions:

                print(
                    word,
                    "=> Probability:",
                    round(probability, 4)
                )
    elif choice == "5":

        print("\nEnter number of test cases:")

        number = int(input())

        test_cases = []

        for i in range(number):

            print(
                f"\nTest case {i + 1}"
            )

            sentence = input(
                "Incomplete sentence: "
            )

            actual_word = input(
                "Actual next word: "
            )

            test_cases.append(
                (sentence, actual_word)
            )

        n = int(
            input(
                "\nEnter N (1/2/3): "
            )
        )

        accuracy = calculate_accuracy(
            test_cases,
            n
        )

        print(
            "\nPrediction Accuracy:",
            round(accuracy, 2),
            "%"
        )
    elif choice == "6":

        print("Program terminated.")
        break

    else:

        print("Invalid choice.")
