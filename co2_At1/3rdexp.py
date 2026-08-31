print("STEMMING-BASED PREPROCESSING MODULE")
print("-" * 85)
words = input("Enter words separated by space: ").lower().split()
results = []
for word in words:
    if word == "played":
        stem = "play"
        affix = "ed"
        transformation = "Inflectional"
        normalized = "play"
    elif word == "playing":
        stem = "play"
        affix = "ing"
        transformation = "Inflectional"
        normalized = "play"
    elif word == "player":
        stem = "play"
        affix = "er"
        transformation = "Derivational"
        normalized = "play"
    else:
        stem = word
        affix = "-"
        transformation = "None"
        normalized = word
    results.append([
        word, stem, affix, transformation, normalized
    ])
print("\n{:<15} {:<15} {:<15} {:<18} {:<15}".format(
    "Original", "Stem", "Removed Affix",
    "Transformation", "Normalized"
))

print("-" * 85)
for row in results:
    print("{:<15} {:<15} {:<15} {:<18} {:<15}".format(*row))
