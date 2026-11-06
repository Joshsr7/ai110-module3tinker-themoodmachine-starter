# mood_analyzer.py
"""
Rule based mood analyzer for short text snippets.

This class starts with very simple logic:
  - Preprocess the text
  - Look for positive and negative words
  - Compute a numeric score
  - Convert that score into a mood label
"""

import re
from typing import List, Optional, Tuple

from dataset import POSITIVE_WORDS, NEGATIVE_WORDS, POSITIVE_EMOJIS, NEGATIVE_EMOJIS

# Words that flip the next sentiment word, as in "not happy" or "never fun".
NEGATIONS = {"not", "no", "never", "don't", "dont", "can't", "cant", "isn't",
             "wasn't", "ain't", "won't", "didn't", "nothing"}
NEGATION_WINDOW = 3  # a negation reaches at most this many tokens ahead

# One token is a text emoticon, a single emoji, or a word.
TOKEN_PATTERN = re.compile(
    r"[:;]-?[()dp]"                               # :) :( :-) :d ;p
    r"|[\U0001F300-\U0001FAFF\u2600-\u27BF]"      # emoji
    r"|[a-z0-9']+"                                # words and contractions
)


class MoodAnalyzer:
    """
    A very simple, rule based mood classifier.
    """

    def __init__(
        self,
        positive_words: Optional[List[str]] = None,
        negative_words: Optional[List[str]] = None,
    ) -> None:
        # Use the default lists from dataset.py if none are provided.
        positive_words = positive_words if positive_words is not None else POSITIVE_WORDS
        negative_words = negative_words if negative_words is not None else NEGATIVE_WORDS

        # Store as sets for faster lookup. Emojis are treated like words.
        self.positive_words = set(w.lower() for w in positive_words) | set(POSITIVE_EMOJIS)
        self.negative_words = set(w.lower() for w in negative_words) | set(NEGATIVE_EMOJIS)

    # ---------------------------------------------------------------------
    # Preprocessing
    # ---------------------------------------------------------------------

    def preprocess(self, text: str) -> List[str]:
        """
        Convert raw text into a list of tokens the model can work with.

        Steps:
          - Lowercase and strip whitespace
          - Pull out emoticons like ":)" and emojis as their own tokens
          - Keep words and contractions, drop other punctuation
          - Shrink stretched words like "sooo" so they can still match
        """
        cleaned = text.strip().lower().replace("\u2019", "'")
        tokens = TOKEN_PATTERN.findall(cleaned)
        return [self._normalize_repeats(token) for token in tokens]

    def _normalize_repeats(self, token: str) -> str:
        """Shrink stretched words like "sooo" or "happyyy" to a known spelling."""
        if not re.search(r"(.)\1\1", token):
            return token
        two = re.sub(r"(.)\1{2,}", r"\1\1", token)   # goood -> good
        one = re.sub(r"(.)\1{2,}", r"\1", token)      # happyyy -> happy
        known = self.positive_words | self.negative_words
        return one if one in known and two not in known else two

    # ---------------------------------------------------------------------
    # Scoring logic
    # ---------------------------------------------------------------------

    def score_text(self, text: str) -> int:
        """
        Compute a numeric "mood score" for the given text.

        Positive words increase the score.
        Negative words decrease the score.

        Improvements over the starter:
          - Negation handling: "not happy" counts as negative, "not bad" as positive
          - Emoji signals: emojis and emoticons count like sentiment words
        """
        score, _, _ = self._analyze(text)
        return score

    def _analyze(self, text: str) -> Tuple[int, List[str], List[str]]:
        """Return (score, positive hits, negative hits) for a piece of text.

        Each positive word or emoji adds 1 and each negative one subtracts 1.
        A negation word flips the next sentiment token within NEGATION_WINDOW,
        so "not bad" counts as positive and "not happy" counts as negative.
        """
        score = 0
        positive_hits: List[str] = []
        negative_hits: List[str] = []
        negation_left = 0

        for token in self.preprocess(text):
            if token in NEGATIONS:
                negation_left = NEGATION_WINDOW
                continue

            value = 0
            if token in self.positive_words:
                value = 1
            elif token in self.negative_words:
                value = -1

            if value and negation_left:
                value = -value
                token = "not " + token
                negation_left = 0
            elif negation_left:
                negation_left -= 1

            if value > 0:
                positive_hits.append(token)
            elif value < 0:
                negative_hits.append(token)
            score += value

        return score, positive_hits, negative_hits

    # ---------------------------------------------------------------------
    # Label prediction
    # ---------------------------------------------------------------------

    def predict_label(self, text: str) -> str:
        """
        Turn the numeric score for a piece of text into a mood label.

        The default mapping is:
          - score > 0  -> "positive"
          - score < 0  -> "negative"
          - score == 0 -> "neutral"

        Change from the starter: if the post has both positive and negative
        hits and the score is within 1 of zero, it is labeled "mixed".
        """
        score, positive_hits, negative_hits = self._analyze(text)
        # Both kinds of signal and no clear winner means the post is mixed.
        if positive_hits and negative_hits and abs(score) <= 1:
            return "mixed"
        if score > 0:
            return "positive"
        if score < 0:
            return "negative"
        return "neutral"

    # ---------------------------------------------------------------------
    # Explanations (optional but recommended)
    # ---------------------------------------------------------------------

    def explain(self, text: str) -> str:
        """
        Return a short string explaining WHY the model chose its label.

        Shows the score, which tokens counted as positive or negative, and the
        full token list so ignored words are easy to spot.
        """
        score, positive_hits, negative_hits = self._analyze(text)
        return (
            f"score={score}, positive={positive_hits}, negative={negative_hits}, "
            f"tokens={self.preprocess(text)}"
        )
