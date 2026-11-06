# Model Card: Mood Machine

This model card covers both versions of the Mood Machine: the rule based model in `mood_analyzer.py` and the ML model in `ml_experiments.py`.

## 1. Model Overview

**Model type:**
I compared both models.

**Intended purpose:**
Label short social media style posts as positive, negative, neutral, or mixed. It is a learning tool, not something to use on real people's messages.

**How it works:**
The rule based model splits a post into tokens, adds 1 for each positive word or emoji, subtracts 1 for each negative one, and turns the total into a label. The ML model counts which words appear in each post and learns from the labeled examples which words go with which label.

## 2. Data

**Dataset description:**
The starter had 6 posts. I added 10 in Part 1 and 4 more in Part 4, so there are 20 posts in `SAMPLE_POSTS` with 20 matching labels in `TRUE_LABELS`. An assert in `dataset.py` stops the program if the two lists ever have different lengths.

**Labeling process:**
I labeled each post by how I think most people would read it. Sarcastic posts like "I absolutely love getting stuck in traffic" are labeled negative even though the words sound positive. Hard ones were "Can't wait for this week to be over :(", which could be read as excited, and "No cap this pizza is amazing", where someone who does not know the slang might see "no" and think it is negative.

**Important characteristics of your dataset:**

* Slang like lowkey, no cap, fire, rn
* Emojis and emoticons like 🔥, 😭, :(
* Sarcasm in two posts
* Mixed feelings in three posts
* Negation like "not happy" and "not bad"
* The word "sick" used two ways

**Possible issues with the dataset:**
20 posts is very small. Only 3 posts are neutral. All posts are in English and most of the slang is the kind I use, so other ways of writing are barely covered. I wrote the posts and the rules at the same time, so the rule based score on this data is higher than it would be on posts from strangers.

## 3. How the Rule Based Model Works

**Your scoring rules:**

* Preprocessing lowercases the text, splits out emojis and emoticons as their own tokens, drops punctuation, and shrinks stretched words so "sooo" becomes "soo".
* Each positive word or emoji adds 1 and each negative one subtracts 1.
* Negation handling is my main improvement. Words like not, never, don't, and can't flip the next sentiment word within 3 tokens, so "not happy" is negative and "not bad" is positive.
* Emoji signals are my second improvement. Emojis and emoticons are in the word lists and count like words.
* Label rules: if a post has both positive and negative hits and the score is within 1 of zero, it is mixed. Otherwise above zero is positive, below zero is negative, and zero is neutral.
* `explain()` prints the score, the matched words, and all tokens, so I can see what was counted and what was ignored.

**Strengths of this approach:**
It is predictable and easy to check. For every prediction I can point to the exact words that caused it. It handles clear posts, negation, and simple mixed posts well.

**Weaknesses of this approach:**
It only knows the words in its lists. It cannot detect sarcasm, it does not understand words with two meanings, and one word can decide the whole label.

## 4. How the ML Model Works

**Features used:**
Bag of words with CountVectorizer, then logistic regression.

**Training data:**
The model trained on `SAMPLE_POSTS` and `TRUE_LABELS`.

**Training behavior:**
It scored 1.00 on the same posts it trained on, both at 16 posts and at 20 posts. That number is misleading. When I tested each post with the model trained on the other posts, it got only 0.19 right at 16 posts and 0.25 at 20 posts. It memorizes the data more than it learns from it.

**Strengths and weaknesses:**
It picked up sarcasm and slang that my rules miss, but only when a very similar post was already in the training data. CountVectorizer also drops emojis and one letter words by default, so 🔥 and :( mean nothing to it.

## 5. Evaluation

**How you evaluated the model:**
I ran `python main.py` for the rule based model and `python ml_experiments.py` for the ML model. I also wrote `stress_test.py`, which runs breaker posts and compares the same meaning in two writing styles.

| Version | Rule based | ML on training posts | ML on unseen posts |
|---|---|---|---|
| Plain starter rules, 16 posts | 0.56 | | |
| My rules, 16 posts | 0.94 | 1.00 | 0.19 |
| My rules, 20 posts | 0.85 | 1.00 | 0.25 |

**Examples of correct predictions:**

* "I am not happy about this" is negative because the negation rule flipped "happy". The plain starter rules called it positive.
* "I hate mondays but the coffee is good" is mixed because it has one positive and one negative hit and a score of 0.
* "That concert was fire 🔥" is positive because both "fire" and 🔥 count as positive.

**Examples of incorrect predictions:**

* "I absolutely love getting stuck in traffic" is predicted positive. The only word the model knows is "love", and it has no way to see sarcasm. The ML model gets this one right, but only because this exact post is in its training data.
* "I feel sick today" is predicted neutral. I chose not to add "sick" to either list because in "This song is sick 🔥" it means good. I documented this one instead of fixing it.
* "I love waiting in line for hours" is the same sarcasm failure as the traffic post.

**Part 3 fix:**
In the style comparison, "dis food bussin fr" and "ngl that test was trash" both came out neutral, while "This food is really good" and "That test was really bad" came out positive and negative. I added the slang words bussin, goated, trash, and mid. After that, three of the four style pairs matched. The fix created a new problem: "Take out the trash before dinner" went from neutral to negative.

## 6. Limitations

* The dataset is tiny and I wrote both the posts and the rules.
* Sarcasm fails every time, as the traffic and waiting in line posts show.
* Words with two meanings fail. "sick" and "trash" are right in some posts and wrong in others.
* An emoji can hide the real mood. "I'm fine 🙂" is predicted positive, but people often say it when they are not fine.
* Misspellings are not handled. "Im sooo hapy today" is neutral while "I am so happy today" is positive.
* Positive and negative words in one post always give mixed, so "The worst part is over, feeling good now" is mixed when a person would say positive.

## 7. Ethical Considerations

**Overt bias:**
Errors clustered around informal and regional writing. Before the Part 3 fix, all four informal posts in my style test were neutral while their standard English versions were labeled correctly. People who write in AAVE, Gen Z slang, or with nonstandard spelling would be underserved, because the word lists were written in standard English. Adding four slang words helped, but the model will still miss any slang I did not think of.

**Covert compliance:**
When I asked my AI assistant to review my word lists, it did point out that words like "sick" and 💀 have two meanings, which is why I left them out. It did not say on its own that the whole word list was built from one style of English. That only showed up when I ran the style comparison. I think it should have flagged that, because it is the biggest fairness problem in the model.

**Other impacts:**
A real system could miss a message from someone in distress if they use sarcasm or an emoji like 🙂 to hide it. Scanning personal messages for mood also raises privacy concerns.

## 8. Ideas for Improvement

* Add many more labeled posts written by different people, with a separate test set
* Use TF IDF and keep emojis in the ML tokenizer
* Give strong words like hate and love more weight than mild ones
* Handle phrases like "can't wait" and "no cap" as one unit
* Use a small pretrained model for sarcasm and context
