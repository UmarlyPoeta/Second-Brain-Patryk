

# Calculus

Calculus is the study of _differentiation_ and _integration_ of functions. Essentially, a neural network is a differentiable function, so calculus will be a fundamental tool to train neural networks, as we will see.

![[Pasted image 20250823131954.png]]

To familiarize yourself with the concepts, you should make things simple and study functions of a single variable for the first time. By definition, the derivative of a function is defined by the limit

![[Pasted image 20250823132041.png]]

where the ratio for a given _h_ is the slope of the line between the points _(x, f(x))_ and _(x+h, f(x+h))_.

In the limit, this is essentially the slope of the tangent line at the point _x_. The figure below illustrates the concept.

![[Pasted image 20250823132050.png]]

Differentiation can be used to optimize functions: the derivative is zero at local maxima or minima. (However, this is not true in the other direction; see _f(x) = x³_ at _0_.)

Points where the derivative is zero are called _critical points_. Whether a critical point is a minimum or a maximum can be decided by looking at the _second derivative_:

![[Pasted image 20250823132102.png]]

There are several essential rules regarding differentiation, but probably the most important is the so-called _chain rule_:

![[Pasted image 20250823132114.png]]

which tells us how to calculate the derivative of composed functions.

Integration is often called the inverse of differentiation. This is true because if _f_ is the derivative of _F_, that is, _F′(x) = f(x)_, then

![[Pasted image 20250823132123.png]]

holds. (If _f_ is an integrable function.)

The integral of a function can also be thought of as the signed area under the curve:

![[Pasted image 20250823132137.png]]

Integration itself plays a role in understanding the concept of expected value. For instance, quantities like entropy and Kullback-Leibler divergence are defined in terms of integrals.

## Further study

I would recommend the [Single Variable Calculus course from MIT](https://www.youtube.com/playlist?list=PL590CCC2BC5AF3BC1). (In general, online courses from MIT are always excellent learning resources.) If you are more of a book person, there are many textbooks available. The [Calculus book by Gilbert Strang](https://ocw.mit.edu/courses/res-18-001-calculus-fall-2023/pages/textbook/), which accompanies the previously mentioned course, is again a great resource, available completely free of charge.

Here are some of my articles on the topic:

- [Why does gradient descent work?](https://thepalindrome.substack.com/p/why-does-gradient-descent-work)
    
- [The history of trigonometric functions](https://thepalindrome.substack.com/p/the-history-of-trigonometric-functions)
    
- [The fascinating story of the exponential function](https://thepalindrome.substack.com/p/the-story-of-the-exponential-function)

