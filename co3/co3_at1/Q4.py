import re
from collections import Counter, defaultdict
training_data = [
    ("I", "PRP"),
    ("read", "VBP"),
    ("a", "DT"),
    ("book", "NN"),

    ("I", "PRP"),
    ("book", "VB"),
    ("a", "DT"),
    ("ticket", "NN"),

    ("The", "DT"),
    ("cat", "NN"),
    ("sits", "VBZ"),
    ("on", "IN"),
    ("the", "DT"),
    ("mat", "NN"),

    ("The", "DT"),
    ("dog", "NN"),
    ("eats", "VBZ"),
    ("food", "NN"),

    ("She", "PRP"),
    ("reads", "VBZ"),
    ("a", "DT"),
    ("book", "NN"),

    ("He", "PRP"),
    ("plays", "VBZ"),
    ("football", "NN"),

    ("Machine", "NN"),
    ("learning", "NN"),
    ("is", "VBZ"),
    ("useful", "JJ"),

    ("Artificial", "JJ"),
    ("intelligence", "NN"),
    ("is", "VBZ"),
    ("powerful", "JJ"),
]


# =========================================================
# STOCHASTIC MODEL
# =========================================================

word_tag_count = defaultdict(Counter)
tag_transition = defaultdict(Counter)
tag_count = Counter()

previous_tag = "<START>"

for word, tag in training_data:

    word_tag_count[
        word.lower()
    ][tag] += 1

    tag_transition[
        previous_tag
    ][tag] += 1

    tag_count[tag] += 1

    previous_tag = tag
def rule_based_tag(word):

    w = word.lower()

    # Dictionary
    dictionary = {

        "i": "PRP",
        "you": "PRP",
        "he": "PRP",
        "she": "PRP",
        "we": "PRP",
        "they": "PRP",

        "a": "DT",
        "an": "DT",
        "the": "DT",

        "on": "IN",
        "in": "IN",
        "at": "IN",
        "with": "IN",

        "is": "VBZ",
        "am": "VBP",
        "are": "VBP",

        "read": "VBP",
        "reads": "VBZ",

        "book": "NN",
        "ticket": "NN",
        "cat": "NN",
        "dog": "NN",
        "food": "NN",
        "mat": "NN",

        "useful": "JJ",
        "powerful": "JJ"
    }

    if w in dictionary:

        return dictionary[w]

    # Pattern rules

    if w.endswith("ing"):
        return "VBG"

    if w.endswith("ed"):
        return "VBD"

    if w.endswith("ly"):
        return "RB"

    if w.endswith("ous"):
        return "JJ"

    if w.endswith("ful"):
        return "JJ"

    if w.endswith("s"):
        return "NNS"

    return "NN"
def stochastic_tag(sentence):

    words = sentence.split()

    result = []

    previous_tag = "<START>"

    for word in words:

        candidates = word_tag_count[
            word.lower()
        ]

        if candidates:

            best_tag = None
            best_score = -1

            for tag in candidates:

                word_probability = (
                    candidates[tag]
                    /
                    sum(candidates.values())
                )

                transition_probability = (
                    tag_transition[
                        previous_tag
                    ][tag]
                    /
                    max(
                        1,
                        sum(
                            tag_transition[
                                previous_tag
                            ].values()
                        )
                    )
                )

                score = (
                    word_probability
                    *
                    transition_probability
                )

                if score > best_score:

                    best_score = score
                    best_tag = tag

            tag = best_tag

        else:

            # Unknown word
            tag = rule_based_tag(word)

        result.append(
            (word, tag)
        )

        previous_tag = tag

    return result
def initial_tag(word):

    return rule_based_tag(word)


def transformation_rules(tagged_sentence):

    result = []

    words = [
        word
        for word, tag in tagged_sentence
    ]

    for i, (word, tag) in enumerate(
        tagged_sentence
    ):

        w = word.lower()

        if i > 0:

            previous_word = words[i - 1].lower()

            if previous_word in [
                "a",
                "an",
                "the"
            ]:

                if w == "book":

                    tag = "NN"
        if i > 0:

            previous_word = words[
                i - 1
            ].lower()

            if previous_word == "i":

                if w == "book":

                    tag = "VB"

                elif w == "read":

                    tag = "VBP"

        if w.endswith("ing"):

            tag = "VBG"

        result.append(
            (word, tag)
        )

    return result


def transformation_based_tagging(
    sentence
):

    words = sentence.split()

    initial = []

    for word in words:

        initial.append(
            (
                word,
                initial_tag(word)
            )
        )

    final = transformation_rules(
        initial
    )

    return final

def display(title, result):

    print("\n------------------------------")
    print(title)
    print("------------------------------")

    for word, tag in result:

        print(
            f"{word:15} -> {tag}"
        )
while True:

    print("\n======================================")
    print("      COMPARATIVE POS TAGGING")
    print("======================================")

    print("1. Rule-Based POS")
    print("2. Stochastic POS")
    print("3. Transformation-Based POS")
    print("4. Compare All")
    print("5. Exit")

    choice = input(
        "\nEnter your choice: "
    )

    if choice == "1":

        sentence = input(
            "\nEnter sentence: "
        )

        result = []

        for word in sentence.split():

            result.append(
                (
                    word,
                    rule_based_tag(word)
                )
            )

        display(
            "RULE-BASED POS TAGGING",
            result
        )

    elif choice == "2":

        sentence = input(
            "\nEnter sentence: "
        )

        result = stochastic_tag(
            sentence
        )

        display(
            "STOCHASTIC POS TAGGING",
            result
        )

    elif choice == "3":

        sentence = input(
            "\nEnter sentence: "
        )

        result = transformation_based_tagging(
            sentence
        )

        display(
            "TRANSFORMATION-BASED POS TAGGING",
            result
        )

    elif choice == "4":

        sentence = input(
            "\nEnter sentence: "
        )

        # Rule-based

        rule_result = []

        for word in sentence.split():

            rule_result.append(
                (
                    word,
                    rule_based_tag(word)
                )
            )

        # Stochastic

        stochastic_result = stochastic_tag(
            sentence
        )

        # Transformation

        transformation_result = (
            transformation_based_tagging(
                sentence
            )
        )

        display(
            "RULE-BASED",
            rule_result
        )

        display(
            "STOCHASTIC",
            stochastic_result
        )

        display(
            "TRANSFORMATION-BASED",
            transformation_result
        )

    elif choice == "5":

        print("Program terminated.")
        break

    else:

        print("Invalid choice.")
