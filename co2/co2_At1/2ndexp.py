print("MORPHOLOGICAL PARSING MODULE")
print("-" * 80)
words = input("Enter words separated by space: ").lower().split()
results = []
for word in words:
    if word == "unhappy":
        prefix = "un"
        base = "happy"
        suffix = "-"
        transformation = "Derivational"
        normalized = "happy"
    elif word == "happiness":
        prefix = "-"
        base = "happy"
        suffix = "ness"
        transformation = "Derivational"
        normalized = "happy"
    elif word == "happily":
        prefix = "-"
        base = "happy"
        suffix = "ly"
        transformation = "Derivational"
        normalized = "happy"
    else:
        prefix = "-"
        base = word
        suffix = "-"
        transformation = "None"
        normalized = word
    breakdown = prefix + " + " + base + " + " + suffix
    results.append([
        word, prefix, base, suffix,
        transformation, breakdown, normalized
    ])
print("\n{:<12} {:<10} {:<10} {:<10} {:<15} {:<25} {:<12}".format(
    "Word", "Prefix", "Base", "Suffix",
    "Type", "Breakdown", "Normalized"
))
print("-" * 100)
for row in results:
    print("{:<12} {:<10} {:<10} {:<10} {:<15} {:<25} {:<12}".format(*row))
