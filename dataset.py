"""
Shared data for the Mood Machine lab.

This file defines:
  - POSITIVE_WORDS: starter list of positive words
  - NEGATIVE_WORDS: starter list of negative words
  - SAMPLE_POSTS: short example posts for evaluation and training
  - TRUE_LABELS: human labels for each post in SAMPLE_POSTS
"""

# ---------------------------------------------------------------------
# Starter word lists
# ---------------------------------------------------------------------

POSITIVE_WORDS = [
    "happy",
    "great",
    "good",
    "love",
    "excited",
    "awesome",
    "fun",
    "chill",
    "relaxed",
    "amazing",
    "hopeful",
    "proud",
    "glad",
    "fire",
    # slang added in Part 3 after the style comparison
    "bussin",
    "goated",
]

NEGATIVE_WORDS = [
    "sad",
    "bad",
    "terrible",
    "awful",
    "angry",
    "upset",
    "tired",
    "stressed",
    "hate",
    "boring",
    "ugh",
    "annoyed",
    "exhausted",
    "worst",
    # slang added in Part 3 after the style comparison
    "trash",
    "mid",
]

# Emojis and text emoticons count as mood signals too.
POSITIVE_EMOJIS = [":)", ":d", "🙂", "😊", "😂", "🔥", "❤", "🥳"]
NEGATIVE_EMOJIS = [":(", "😭", "😢", "😡", "😞"]

# ---------------------------------------------------------------------
# Starter labeled dataset
# ---------------------------------------------------------------------

# Short example posts written as if they were social media updates or messages.
SAMPLE_POSTS = [
    "I love this class so much",
    "Today was a terrible day",
    "Feeling tired but kind of hopeful",
    "This is fine",
    "So excited for the weekend",
    "I am not happy about this",
]

# Human labels for each post above.
# Allowed labels in the starter:
#   - "positive"
#   - "negative"
#   - "neutral"
#   - "mixed"
TRUE_LABELS = [
    "positive",  # "I love this class so much"
    "negative",  # "Today was a terrible day"
    "mixed",     # "Feeling tired but kind of hopeful"
    "neutral",   # "This is fine"
    "positive",  # "So excited for the weekend"
    "negative",  # "I am not happy about this"
]

# Added posts. Each one gets exactly one label below.
NEW_POSTS = [
    ("Lowkey stressed but kind of proud of myself", "mixed"),
    ("I absolutely love getting stuck in traffic", "negative"),  # sarcasm
    ("That concert was fire 🔥", "positive"),                     # slang and emoji
    ("This movie was not bad at all", "positive"),               # negation
    ("Ugh my phone died again 😭", "negative"),
    ("Got the job!!! sooo happy rn", "positive"),                # repeated letters
    ("No cap this pizza is amazing", "positive"),                # slang
    ("I hate mondays but the coffee is good", "mixed"),
    ("Can't wait for this week to be over :(", "negative"),
    ("Just finished my homework, going to bed", "neutral"),
    # Added in Part 4 to see how each model reacts to more data
    ("I love waiting in line for hours", "negative"),             # sarcasm
    ("This song is sick 🔥", "positive"),                         # slang
    ("I feel sick today", "negative"),                            # same word, other meaning
    ("Not gonna lie, today was pretty good", "positive"),
]

for post, label in NEW_POSTS:
    SAMPLE_POSTS.append(post)
    TRUE_LABELS.append(label)

assert len(SAMPLE_POSTS) == len(TRUE_LABELS), "every post needs exactly one label"
