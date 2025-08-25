Probability theory is the mathematically rigorous study of chance, fundamental to all fields of science.

![[Pasted image 20250823132711.png]]

Setting exact definitions aside for now, let’s ponder a bit about what _probability_ represents. Let’s say I toss a coin, with a 50% chance (or _0.5 probability_) of it being heads. After repeating the experiment 10 times, how many heads did I get?

If you have answered 5, you are wrong. Heads being 0.5 probability doesn’t guarantee that every second throw is heads. Instead, what it means that if you repeat the experiment _n_ times where _n_ is a _really large number_, the number of heads will be very close to _n/2_.

Besides the basics, there are some advanced things you need to understand, first and foremost, _expected value_ and _entropy_. But let’s not get ahead of ourselves! First, we have to understand what probability is!

## The concept of probability

First of all, probability is a function that renders a numeric value between 0 and 1 to _events_. Events are represented by _sets_, which are subsets in the _event space,_ denoted by Ω.

![[Pasted image 20250823132725.png]]

There are two defining properties of probability:

1. the probability of the entire event space is 1,
    
2. and the probabilities of disjoint events can be summed up.
    

In terms of mathematical formulas:

![[Pasted image 20250823132734.png]]

Set operations can also be translated to the language of events: _A ∪ B_ means that either _A_ or _B_ occurs, while _A ∩ B_ means that both occur.

![[Pasted image 20250823132744.png]]

One of the most important concepts in probability theory is _conditional probability_, which studies probabilities in the context of observations. By definition, it is given by the ratio of the probability of both events occurring and the probability of the observed event.

![[Pasted image 20250823132753.png]]

One simple example: what is the probability of a given email being spam, if it contains the word _“deal”_? Observing keywords like the mentioned _“deal”_ increases the probability of the email being spam.

In certain practical scenarios, we only know _P(A | B)_, but we want to estimate _P(B | A)_. This is what _Bayes’ theorem_ is for, expressing one in terms of the other.

![[Pasted image 20250823132803.png]]

In English, Bayes’ theorem shows us how to update our _priors_ in terms of the _likelihood_.

## Expected value

Suppose that you play a game with your friend. You toss a classical six-sided dice, and if the outcome is 1 or 2, you win 300 bucks. Otherwise, you lose 200. What are your average earnings per round if you play this game long enough? Should you even be playing this game?

Well, you win 100 bucks with probability 1/3, and you lose 200 with probability 2/3. That is, if X is the random variable encoding the result of the dice throw, then

![[Pasted image 20250823132813.png]]

This is the expected value, that is, the average amount of money you will receive per round in the long run. Since this is negative, you will lose money, so you should never play this game.

Generally speaking, the expected value is defined by

![[Pasted image 20250823132824.png]]

for discrete random variables and

![[Pasted image 20250823132833.png]]

for real-valued continuous random variables.

In machine learning, _loss functions for training neural networks are expected values_ in one way or another_._

## **Law of large numbers**

People often falsely attribute certain phenomena to the law of large numbers. For instance, gamblers who are on a losing streak believe that they should soon win because of the _law of large numbers_. This is totally wrong. Let’s see what this is really!

Suppose that _X, X₁, X₂, ..._ are random variables representing the independent repetitions of the same experiment. (Say, rolling a dice or tossing a coin.)

The (strong) _law of large numbers_ states that

![[Pasted image 20250823132842.png]]

holds with probability one; that is, the average of the outcomes in the long run equals the expected value.

An interpretation is that if a random event is repeated enough times, individual results might not matter. So, if you are playing in a casino with a game that has negative expected value (as they all do), it doesn’t matter that you win occasionally. The law of large numbers implies that you _will lose money_.

To get a little bit ahead, LLN is going to be essential for _stochastic gradient descent_.

## **Information theory**

Let’s play a game. I have thought of a number between 1 and 1024, and you have to guess it. You can ask questions, but your goal is to use as few questions as possible. How much do you need?

If you play it smart, you will perform a binary search with your questions. First, you may ask: _is the number between 1 and 512?_ With this, you have cut the search space in half. Using this strategy, you can figure out the answer in _log₂(1024) = 10_ questions.

But what if I didn’t use the uniform distribution when picking the number? For instance, I could have used a Poisson distribution.

Here, you would probably need fewer questions because you know that the distribution tends to concentrate around specific points. (Which depends on the parameter.)

In the extreme case, when the distribution is concentrated on a single number, you need _zero_ questions to guess it correctly. Generally, the number of questions depends on the information carried by the distribution. The uniform distribution contains the least amount of information, while singular ones are pure information.

_Entropy_ is a measure that quantifies this. It is defined by

![[Pasted image 20250823132856.png]]

for discrete random variables and

![[Pasted image 20250823132905.png]]

for continuous, real-valued ones. (The base of the logarithm is usually 2, _e_, or 10, but it doesn’t really matter.)

If you have ever worked with classification models before, you probably encountered the _cross-entropy_ loss, defined by

![[Pasted image 20250823132913.png]]

Another frequently used quantity is the _Kullback-Leibler divergence_, defined by

![[Pasted image 20250823132927.png]]

where _P_ and _Q_ are two probability distributions. This is essentially cross-entropy minus the entropy, which can be thought of as quantifying the difference between the two distributions. This is useful, for instance, when training generative adversarial networks. Minimizing the Kullback-Leibler divergence guarantees that the two distributions are similar.

## Further study

Here, I would again recommend an online course from MIT, which covers all the fundamentals and some advanced concepts. Check out [Introduction to Probability by John Tsitsiklis](https://youtube.com/playlist?list=PLUl4u3cNGP60hI9ATjSFgLZpbNJ7myAg6&si=hqqCNfvRt8wlRpFy)!

Some of articles about probability:

- [The Law of Large Numbers](https://thepalindrome.substack.com/p/the-law-of-large-numbers)
    
- [Is probability frequentist or Bayesian?](https://thepalindrome.substack.com/p/is-probability-frequentist-or-bayesian)
    
- [Probabilities, densities, and distributions](https://thepalindrome.substack.com/p/probabilities-densities-and-distributions)
    
- [What's the meaning of the expected value?](https://thepalindrome.substack.com/p/whats-the-meaning-of-the-expected)


and:

-  [[Binomal Distributions]]
- [[Normal Distribution]]
- [[Statistical visualisations]]
- [[Summary Statistics DataCamp]]

