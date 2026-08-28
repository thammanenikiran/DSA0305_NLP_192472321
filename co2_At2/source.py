
sentences = [
    [("The", "DT"), ("boy", "NN"), ("eats", "VBZ"), ("rice", "NN")],
    [("The", "DT"), ("girl", "NN"), ("drinks", "VBZ"), ("milk", "NN")],
    [("A", "DT"), ("cat", "NN"), ("drinks", "VBZ"), ("milk", "NN")],
    [("The", "DT"), ("dog", "NN"), ("chases", "VBZ"), ("cat", "NN")],
    [("A", "DT"), ("teacher", "NN"), ("teaches", "VBZ"), ("students", "NNS")],
    [("Students", "NNS"), ("study", "VBP"), ("English", "NN")],
    [("Birds", "NNS"), ("fly", "VBP"), ("high", "RB")],
    [("Children", "NNS"), ("play", "VBP"), ("games", "NNS")]
]
print("==============================================")
print("WORDS AND POS TAGS")
print("==============================================")

for sentence in sentences:

    words = []
    tags = []

    for word, tag in sentence:
        words.append(word)
        tags.append(tag)

    print("Words :", words)
    print("Tags  :", tags)
    print()

tags = []

for sentence in sentences:
    for word, tag in sentence:

        if tag not in tags:
            tags.append(tag)

print("POS Tags:")
print(tags)
print()
tag_count = {}

for tag in tags:
    tag_count[tag] = 0

for sentence in sentences:

    for word, tag in sentence:
        tag_count[tag] = tag_count[tag] + 1
print("==============================================")
print("TAG COUNTS")
print("==============================================")

for tag in tag_count:
    print(tag, ":", tag_count[tag])

print()
emission_count = {}
for tag in tags:
    emission_count[tag] = {}
for sentence in sentences:
    for word, tag in sentence:
        if word not in emission_count[tag]:
            emission_count[tag][word] = 1
        else:
            emission_count[tag][word] = emission_count[tag][word] + 1
emission_probability = {}

for tag in tags:

    emission_probability[tag] = {}

    for word in emission_count[tag]:

        count = emission_count[tag][word]

        probability = count / tag_count[tag]

        emission_probability[tag][word] = probability


print("==============================================")
print("EMISSION PROBABILITIES")
print("==============================================")

for tag in emission_probability:

    print("\nTag:", tag)

    for word in emission_probability[tag]:

        print(
            "P(" + word + "|" + tag + ") =",
            emission_probability[tag][word]
        )

print()
transition_count = {}

for tag in tags:
    transition_count[tag] = {}

for sentence in sentences:

    for i in range(len(sentence) - 1):

        current_tag = sentence[i][1]
        next_tag = sentence[i + 1][1]

        if next_tag not in transition_count[current_tag]:

            transition_count[current_tag][next_tag] = 1

        else:

            transition_count[current_tag][next_tag] = \
                transition_count[current_tag][next_tag] + 1
transition_probability = {}

for tag in tags:

    transition_probability[tag] = {}

    for next_tag in transition_count[tag]:

        count = transition_count[tag][next_tag]

        probability = count / tag_count[tag]

        transition_probability[tag][next_tag] = probability


print("==============================================")
print("TRANSITION PROBABILITIES")
print("==============================================")

for tag in transition_probability:

    print("\nFrom Tag:", tag)

    for next_tag in transition_probability[tag]:

        print(
            "P(" + next_tag + "|" + tag + ") =",
            transition_probability[tag][next_tag]
        )

print()
print("==============================================")
print("HMM")
print("==============================================")

print("Emission Model:")
print(emission_probability)

print("\nTransition Model:")
print(transition_probability)

print()
def viterbi(words):

    # Viterbi probability table
    viterbi_table = []

    # Backpointer table
    backpointer = []
    first_word = words[0]
    first_probabilities = {}
    first_backpointer = {}

    for tag in tags:

        if first_word in emission_probability[tag]:

            # Since there is no previous tag,
            # we use the emission probability.

            first_probabilities[tag] = \
                emission_probability[tag][first_word]

        else:

            first_probabilities[tag] = 0

        first_backpointer[tag] = None

    viterbi_table.append(first_probabilities)
    backpointer.append(first_backpointer)
    for i in range(1, len(words)):

        word = words[i]

        current_probabilities = {}
        current_backpointer = {}

        for current_tag in tags:

            # Get emission probability

            if word in emission_probability[current_tag]:

                emission = emission_probability[current_tag][word]

            else:
                emission = 0

            best_probability = 0
            best_previous_tag = None


            # Find best previous tag

            for previous_tag in tags:

                previous_probability = \
                    viterbi_table[i - 1][previous_tag]
                if current_tag in transition_probability[previous_tag]:

                    transition = \
                        transition_probability[previous_tag][current_tag]

                else:

                    transition = 0
                probability = \
                    previous_probability * transition * emission
                if probability > best_probability:

                    best_probability = probability
                    best_previous_tag = previous_tag
            current_probabilities[current_tag] = best_probability

            current_backpointer[current_tag] = best_previous_tag


        viterbi_table.append(current_probabilities)
        backpointer.append(current_backpointer)
    last_column = viterbi_table[-1]

    best_final_tag = None
    best_final_probability = 0

    for tag in tags:

        if last_column[tag] > best_final_probability:

            best_final_probability = last_column[tag]
            best_final_tag = tag
    best_tags = []

    current_tag = best_final_tag

    for i in range(len(words) - 1, -1, -1):

        best_tags.append(current_tag)

        current_tag = backpointer[i][current_tag]
    best_tags.reverse()


    return best_tags, viterbi_table

new_sentence = ["The", "cat", "drinks", "milk"]
result, table = viterbi(new_sentence)
print("==============================================")
print("VITERBI TABLE")
print("==============================================")

for i in range(len(new_sentence)):

    print("\nWord:", new_sentence[i])

    for tag in tags:

        print(tag, ":", table[i][tag])

print()
print("==============================================")
print("FINAL POS TAGGING")
print("==============================================")

for i in range(len(new_sentence)):

    print(new_sentence[i], "->", result[i])


print()
print("Predicted POS Tag Sequence:")
print(result)
