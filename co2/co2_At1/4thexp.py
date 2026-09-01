print("FINITE-STATE MORPHOLOGICAL PARSER")
print("=" * 100)
words = input("Enter words separated by space: ").lower().split()
results = []
for word in words:
    if word == "writes":
        path = "q0 -> q1 -> q2 -> q3 -> q4"
        breakdown = "write + s"
        root = "write"
        classification = "Regular Inflection"
        normalized = "write"

    elif word == "writing":
        path = "q0 -> q1 -> q2 -> q3 -> q5"
        breakdown = "write + ing"
        root = "write"
        classification = "Regular Inflection"
        normalized = "write"
    elif word == "written":
        path = "q0 -> q1 -> q6 -> q7"
        breakdown = "write -> written"
        root = "write"
        classification = "Irregular Inflection"
        normalized = "write"
    else:

        path = "q0"
        breakdown = word
        root = word
        classification = "Unknown"
        normalized = word

    results.append([
        word,
        path,
        breakdown,
        root,
        classification,
        normalized
    ])

print("\n{:<12} {:<30} {:<22} {:<12} {:<20} {:<12}".format(
    "Word",
    "State Path",
    "Morphological Breakdown",
    "Root",
    "Classification",
    "Normalized"
))

print("-" * 120)
for row in results:
    print("{:<12} {:<30} {:<22} {:<12} {:<20} {:<12}".format(*row))
