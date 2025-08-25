
This is the part where linear algebra and calculus come together, laying the foundations for the primary tool to train neural networks: gradient descent. Mathematically speaking, a neural network is simply a function of multiple variables. (Although the number of variables can be in the millions.)

![[Pasted image 20250823132309.png]]

Similar to univariate calculus, the two main topics here are differentiation and integration. Let’s suppose that we have a function _f: ℝⁿ → ℝ_, mapping vectors to real numbers.

In two dimensions (that is, for _n = 2_), you can imagine its plot as a surface. (Since humans don’t see higher than three dimensions, it is hard to visualize functions with more than two real variables.)

![[Pasted image 20250823132322.png]]

## **Differentiation in multiple variables**

In a single variable, the derivative was the slope of the tangent line. How would you define tangents here? A point on the surface has several tangents, not just one. However, there are two special tangents: one is parallel to the _x-z_ plane, while the other is parallel to the _y-z_ plane. Their slope is determined by the _partial derivatives_, defined by

![[Pasted image 20250823132333.png]]

That is, you take the derivative of the functions obtained by fixing all but one variable. (The formal definition is identical for ≥ 3 variables, just more complicated notation.)

Tangents in these special directions span the _tangent plane_.

![[Pasted image 20250823132344.png]]
The tangent plane

## The gradient

There is another special direction: the _gradient_, which is the vector defined by

![[Pasted image 20250823132402.png]]

The gradient always points to the direction of the largest increase! So, if you would take a tiny step in this direction, your elevation would be the maximal among all the other directions you could have chosen. This is the basic idea of _gradient descent_, an algorithm used to maximize functions. Its steps are the following.

1. Calculate the gradient at the point _**x₀**_, where you currently are.
    
2. Take a small step in the direction opposite to the gradient to arrive at the point _**x₁**_. (The step size is called the _learning rate_.)
    
3. Go back to Step 1 and repeat the process until convergence.
    

Of course, there are several flaws in this basic algorithm, which has been improved several times over the years. Modern gradient descent-based optimizers employ various techniques, such as adaptive step size, momentum, and other methods, which we will not detail here.

Calculating the gradient in practice is difficult. Functions are often described by the composition of other functions, for instance, the familiar linear layer

![[Pasted image 20250823132415.png]]

where _A_ is a matrix, _b_ and _x_ are vectors, and _σ_ is the sigmoid function. (Of course, there can be other activations, but we shall stick to this for simplicity.) How would you calculate this gradient? At this point, it is not even clear how to define the gradient for vector-vector functions such as this, so let’s discuss!

The function _g(**x**): ℝⁿ → ℝᵐ_ can always be written in terms of vector-scalar functions like

![[Pasted image 20250823132425.png]]

The gradient of _g_ is defined by the matrix whose _k_-th row is the _k_-th component’s gradient. That is,

![[Pasted image 20250823132436.png]]

This matrix is called the _total derivative of g_.

In our example _f(**x**) = σ(A**x** + **b**)_, things become a bit more complicated because it is the composition of two functions:

1. _l(**x**) = A**x** + **b**_,
    
2. and _σ(**x**),_
    

defined by applying the univariate sigmoid componentwise. The function _l_ can be decomposed further to _m_ functions mapping from the n-dimensional vector space to the space of real numbers:

![[Pasted image 20250823132447.png]]

where

![[Pasted image 20250823132507.png]]

If you calculate the total derivative, you’ll see that

![[Pasted image 20250823132519.png]]

This is the _chain rule for multivariate functions_ in its full generality. Without it, there would be no easy way to calculate the gradient of a neural network, which is ultimately a composition of many functions.

## **Higher-order derivatives**

Similarly to the univariate case, the gradient and derivatives play a role in determining whether a given point in space is a local minimum or maximum. (Or neither.) To provide a concrete example, training a neural network is equivalent to minimizing the loss function on the parameters’ training data. It is all about finding the optimal parameter configuration _w_ for which the minimum is attained:

![[Pasted image 20250823132547.png]]

where N: ℝⁿ → ℝᵐ and l: ℝᵐ → ℝ are the neural network and the loss function, respectively.

For a general differentiable vector-scalar function of _n_ variables, there are _n²_ second derivatives, forming the _Hessian matrix_

![[Pasted image 20250823132603.png]]

In multiple variables, the determinant of the Hessian takes the role of the second derivative. Similarly, it can be used to determine whether a critical point (i.e., where all the derivatives are zero) is a minimum, maximum, or just a saddle point.

## **Further study**

There are lots of fantastic online courses on multivariable calculus. I have two specific recommendations:

- [MIT multivariable calculus](https://www.youtube.com/playlist?list=PL4C4C8A7D06566F38)
    
- [Khan Academy on multivariable calculus](https://www.youtube.com/playlist?list=PLSQl0a2vh4HC5feHa6Rc5c0wbRTx56nF7)
    



