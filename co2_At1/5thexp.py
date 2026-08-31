print("PORTER STEMMER BASED PREPROCESSING")
print("=" * 80)
words = input("Enter words separated by space: ").lower().split()
def porter_stem(word):
    steps = []
    original = word
    # Step 1: Remove -al
    if word.endswith("al"):
        word = word[:-2]
        steps.append("Remove 'al' -> " + word)

    # Step 2: Remove -ion
    if word.endswith("ion"):
        word = word[:-3]
        steps.append("Remove 'ion' -> " + word)

    # Step 3: Remove final e
    if word.endswith("e") and len(word) > 3:
        word = word[:-1]
        steps.append("Remove final 'e' -> " + word)

    return original, steps, word
results = []
for word in words:
    original, steps, final_stem = porter_stem(word)

    if len(steps) == 0:
        rule = "No rule applied"
        intermediate = word
    else:
        rule = "; ".join(steps)
        intermediate = " -> ".join(
            [x.split("->")[1].strip() for x in steps]
        )

    results.append([
        original,
        rule,
        intermediate,
        final_stem
    ])

print("\n{:<15} {:<45} {:<25} {:<15}".format(
    "Original",
    "Applied Rule(s)",
    "Intermediate Forms",
    "Final Stem"
))

print("-" * 105)
for row in results:
    print("{:<15} {:<45} {:<25} {:<15}".format(*row))
