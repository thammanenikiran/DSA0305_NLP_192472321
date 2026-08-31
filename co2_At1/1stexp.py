print("MORPHOLOGICAL ANALYSIS")
print("-" * 70)
words = input("Enter words separated by space: ").lower().split()
results = []
for word in words:
    if word == "connected":
        root = "connect"
        suffix = "ed"
        suffix_type = "Inflectional"
        normalized = "connect"

    elif word == "connecting":
        root = "connect"
        suffix = "ing"
        suffix_type = "Inflectional"
        normalized = "connect"

    elif word == "connection":
        root = "connect"
        suffix = "ion"
        suffix_type = "Derivational"
        normalized = "connect"

    else:
        root = word
        suffix = "-"
        suffix_type = "None"
        normalized = word

    results.append([word, root, suffix, suffix_type, normalized])

print("\n{:<15} {:<15} {:<10} {:<15} {:<15}".format(
    "Word", "Root", "Suffix", "Type", "Normalized"
))

print("-" * 70)
for row in results:
    print("{:<15} {:<15} {:<10} {:<15} {:<15}".format(*row))
