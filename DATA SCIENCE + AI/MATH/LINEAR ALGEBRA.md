Predictive models such as neural networks are essentially functions that are trained using the tools of calculus. However, they are _described_ using linear algebraic concepts, such as matrix multiplication.
![[Pasted image 20250823130940.png]]
If you are a machine learning engineer working on real-life problems, linear algebra is the most important topic for you, and mastering it will put you above the playing field.

Let’s dive deep!

## Vectors and vector spaces

To have a good understanding of linear algebra, I suggest starting with vector spaces.

The textbook definition is intimidating and abstract, so let’s talk about a special case first. You can think of each point in the plane as a tuple **x** = _(x₁, x₂)_, represented by an arrow pointing from the origin to _(x₁, x₂)_.
![[Pasted image 20250823130952.png]]
You can add these vectors together and multiply them with scalars. Algebraically, it simply goes as
![[Pasted image 20250823131003.png]]
but it’s easier to visualize:

![[Pasted image 20250823131018.png]]
The Euclidean plane is the prototypical model of a vector space. Tuples of _n_ elements form _n_-dimensional vectors, making up the Euclidean space
![[Pasted image 20250823131029.png]]
In general, a set of vectors _V_ is a vector space over the real numbers if you can add and scale vectors in a straightforward way.

When thinking about vector spaces, it helps to model them as tuples in Euclidean space mentally.

## Normed spaces

When you have a good understanding of vector spaces, the next step is to understand how to measure _distance_ in vector spaces.

By default, a vector space in itself gives no tools for this. How would you do this on the plane? You have probably learned that there, we have the famous Euclidean norm defined by

![[Pasted image 20250823131041.png]]
Although the vector notation and the square root symbol make this feel intimidating, the magnitude is just the Pythagorean theorem in disguise.

![[Pasted image 20250823131053.png]]

This can be generalized further: in three dimensions, the Euclidean norm is the repeated application of the Pythagorean theorem.

![[Pasted image 20250823131104.png]]

This is a special case of a _norm_. In general, a vector space _V_ is normed if there is a function _‖ ⋅ ‖: V → [0, ∞)_ such that

![[Pasted image 20250823131116.png]]

where **x** and **y** are any two vectors.

Again, this might be scary, but this is a simple and essential concept. There are a bunch of norms out there, and the most important is the _p-norm_ family, defined for any _p ∈ [0, ∞)_ by

![[Pasted image 20250823131139.png]]

(with _p = 2_ giving the Euclidean norm) and the _supremum norm_

![[Pasted image 20250823131150.png]]

Norms can be used to define a _distance_ by taking the norm of the difference:

![[Pasted image 20250823131203.png]]

The _1-norm_ is called _the Manhattan norm_ (or _taxicab norm_), because the distance between two points depends on how many “grid jumps” you have to perform to get from **x** to **y**.

![[Pasted image 20250823131213.png]]

Sometimes, like for _p = 2_, the norm comes from a so-called _inner product_, which is a bilinear function _〈 ⋅, ⋅ 〉: V × V → [0, ∞)_ such that

![[Pasted image 20250823131224.png]]

A vector space with an inner product is called an _inner product space_. An example is the classical Euclidean product

![[Pasted image 20250823131235.png]]

On the other hand, every inner product can be turned into a norm by

![[Pasted image 20250823131246.png]]

When the inner product for two vectors is zero, we say that the vectors are _orthogonal_ to each other. (Try to come up with some concrete examples on the plane to understand the concept more deeply.)

## **Basis and orthogonal/orthonormal basis**

Although vector spaces are infinite (in our case), you can find a finite set of vectors that can be used to express _all_ vectors in the space. For example, on the plane, we have

![[Pasted image 20250823131258.png]]

where

![[Pasted image 20250823131305.png]]

This is a special case of a basis and an orthonormal basis.

In general, a _basis_ is a minimal set of vectors _**v**₁, **v**₂, ..., **v**ₙ ∈ V_ such that their linear combinations span the vector space:

![[Pasted image 20250823131314.png]]

A basis always exists for any vector space. (It may not be a finite set, but that shouldn’t concern us now.) Without a doubt, a basis simplifies things greatly when talking about linear spaces.

When the vectors in a basis are orthogonal to each other, we call it an _orthogonal basis_. If each basis vector’s norm is 1 for an orthogonal basis, we say it is _orthonormal_.

## Linear transformations

The key objects related to vector spaces are _linear transformations_. If you have seen a neural network before, you know that the fundamental building blocks are layers of the form _f(**x**) = σ(A**x** + **b**)_, where _A_ is a matrix_, b_ and _x_ are vectors, and _σ_ is the sigmoid function. (Or any activation function, really.) Well, the part _Ax_ is a linear transformation.

In general, the function _L: V → W_ is a linear transformation between vector spaces _V_ and _W_ if

![[Pasted image 20250823131401.png]]

holds for all _x, y_ in _V_, and all real number _a_.

To give a concrete example, rotations around the origin in the plane are linear transformations.

Undoubtedly, the most crucial fact about linear transformations is that they can be represented with matrices, as you’ll see next in your studies.

## Matrices and their operations

If linear transformations are clear, you can turn to the study of matrices. (Linear algebra courses often start with matrices, but I would recommend it this way for reasons to be explained later.)

The most important operation for matrices is matrix multiplication, also known as the matrix product. In general, if _A_ and _B_ are matrices defined by

![[Pasted image 20250823131525.png]]

then their product can be obtained by

![[Pasted image 20250823131535.png]]

This might seem difficult to comprehend, but it is pretty straightforward. Take a look at the figure below, demonstrating how to calculate the element in the 2nd row, 1st column of the product.

![[Pasted image 20250823131545.png]]

The reason why matrix multiplication is defined the way it is because matrices represent linear transformations between vector spaces. Matrix multiplication is the composition of linear transformations.

## Determinants

In my opinion, determinants are hands down one of the most challenging concepts to grasp in linear algebra. Depending on your learning resource, it is usually defined by either a recursive definition or a sum that iterates through all permutations. None of them is tractable without significant experience in mathematics.

To understand this concept, watch this video below. Trust me, it is magic.

https://youtu.be/Ip3X9LOh2dk

To summarize, the determinant of a matrix describes how the volume of an object scales under the corresponding linear transformation. If the transformation changes orientations, the sign of the determinant is negative.

You will eventually need to understand how to calculate the determinant, but I wouldn’t worry about it now.

## **Eigenvalues, eigenvectors, and matrix decompositions**

A standard first linear algebra course usually ends with eigenvalues/eigenvectors and some special matrix decompositions like the Singular Value Decomposition.

Let’s suppose that we have a matrix _A_. The number _λ_ is an eigenvalue of _A_ if there is a vector _**x**_ (called an _eigenvector_) such that _A**x** = λ**x**_ holds. In other words, the linear transformation represented by _A_ is a scaling by _λ_ for the vector _x_. This concept plays an essential role in linear algebra. (And practically in every field that uses linear algebra extensively.)

At this point, you are ready to familiarize yourself with a few matrix decompositions. If you think about it for a second, what type of matrices are the best from a computational perspective? Diagonal matrices! If a linear transformation has a diagonal matrix, it is trivial to compute its value on an arbitrary vector:

![[Pasted image 20250823131726.png]]

Most special forms aim to decompose a matrix _A_ into a product of matrices, where hopefully at least one of the matrices is diagonal. Singular Value Decomposition, or SVD in short, the most famous one, states that there are special matrices _U_, _V,_ and a diagonal matrix _Σ_ such that _A = U Σ V_ holds. (_U_ and _V_ are so-called _unitary matrices_, which I don’t define here; suffice to know that it is a special family of matrices.)

SVD is also used to perform Principal Component Analysis, one of the simplest and most well-known methods for dimensionality reduction.

## Further study

Linear algebra can be taught in many ways. The path I outlined here was inspired by the textbook [Linear Algebra Done Right](http://linear.axler.net/) by Sheldon Axler. For an online lecture, I would recommend the [Linear Algebra course from MIT OpenCourseWare,](https://www.youtube.com/playlist?list=PL49CF3715CB9EF31D) an excellent resource.

Here are all of my articles on the topic:

- [Matrices and graphs](https://thepalindrome.substack.com/p/matrices-and-graphs)
    
- [How to measure the angle between two functions](https://thepalindrome.substack.com/p/how-to-measure-the-angle-between)
    
- [The unreasonable effectiveness of orthogonal systems](https://thepalindrome.substack.com/p/the-unreasonable-effectiveness-of)

