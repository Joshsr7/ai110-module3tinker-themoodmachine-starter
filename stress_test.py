"""
Stress tests for the Mood Machine. Run with: python stress_test.py

Part 1 runs "breaker" posts that are built to confuse the rule based model.
Part 2 compares the same meaning written in two language styles, to look for
errors that cluster around one way of writing.
Part 3 runs the same breakers through the ML model for comparison.
"""

from mood_analyzer import MoodAnalyzer
from ml_experiments import train_ml_model, predict_single_text
from dataset import SAMPLE_POSTS, TRUE_LABELS

# (post, what a person would most likely say)
BREAKERS = [
    ("I love getting stuck in traffic", "negative"),         # sarcasm
    ("This new song is sick", "positive"),                    # slang with two meanings
    ("I'm fine 🙂", "neutral"),                               # emoji that can hide a bad mood
    ("I'm exhausted but proud of myself", "mixed"),          # mixed emotions
    ("The worst part is over, feeling good now", "positive"),
    ("I don't hate it", "neutral"),
    ("Take out the trash before dinner", "neutral"),
]

# Same meaning, two styles: (informal or regional, standard)
STYLE_PAIRS = [
    ("dis food bussin fr", "This food is really good"),
    ("ngl that test was trash", "That test was really bad"),
    ("Im sooo hapy today", "I am so happy today"),
    ("this movie mid tbh", "This movie was boring"),
]


def main() -> None:
    analyzer = MoodAnalyzer()
    vectorizer, model = train_ml_model(SAMPLE_POSTS, TRUE_LABELS)

    print("=== Breakers, rule based ===")
    for text, expected in BREAKERS:
        label = analyzer.predict_label(text)
        mark = "ok  " if label == expected else "MISS"
        print(f'{mark} "{text}" -> {label}, a person would say {expected}')
        print(f"       {analyzer.explain(text)}")

    print("\n=== Same meaning, different style, rule based ===")
    for informal, standard in STYLE_PAIRS:
        a, b = analyzer.predict_label(informal), analyzer.predict_label(standard)
        mark = "same" if a == b else "DIFF"
        print(f'{mark} "{informal}" -> {a}   |   "{standard}" -> {b}')

    print("\n=== Breakers, ML model trained on SAMPLE_POSTS ===")
    for text, expected in BREAKERS:
        label = predict_single_text(text, vectorizer, model)
        mark = "ok  " if label == expected else "MISS"
        print(f'{mark} "{text}" -> {label}, a person would say {expected}')


if __name__ == "__main__":
    main()
