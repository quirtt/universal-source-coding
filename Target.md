<script type="text/javascript"
  src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.0/MathJax.js?config=TeX-AMS_CHTML">
</script>
<script type="text/x-mathjax-config">
  MathJax.Hub.Config({
    tex2jax: {
      inlineMath: [['$','$'], ['\\(','\\)']],
      processEscapes: true},
      jax: ["input/TeX","input/MathML","input/AsciiMath","output/CommonHTML"],
      extensions: ["tex2jax.js","mml2jax.js","asciimath2jax.js","MathMenu.js","MathZoom.js","AssistiveMML.js", "[Contrib]/a11y/accessibility-menu.js"],
      TeX: {
      extensions: ["AMSmath.js","AMSsymbols.js","noErrors.js","noUndefined.js"],
      equationNumbers: {
      autoNumber: "AMS"
      }
    }
  });
</script>

# What is the target of the project

Arnab sir's requirements and benchmarks:

- We cannot just randomly sort out the frequencies of the letters from a text file and just produce a Huffman encoding over that distribution and call it a day, instead we have to keep in account of the `conditional probabilities` e.g., `q` comes before `u` always in the natural language setting so `qu` should have a shorter code word than writing the code for `q` and `u` together.

- We want to find the central p.m.f of all the ditributions of giving the model of english language, inside the probability simplex.

## First Issue

Essentially, if as we’re processing a text file, we’re able to identify recurring phrases, we can substitute those phrases with a code that would be shorter than the original text. Doing this over the entire document gives us the compression we’re after. This is basically a very naive application to Lempel-Ziv algorithm

Lempel-Ziv relies on a dictionary which maps a phrase to a unique code. The first 256 entries in the dictionary are the single ASCII characters mapped to their numeric code. For example, at the start, the dictionary might look something like this:

```python
{
  "A": "65",
  "B": "66",
  ....
  "a": "97",
  "b": "98"
}
```

Now, we’ll iterate through the rest of the text — character by character — building up a phrase / character sequence. If the inclusion of a new character creates a phrase that doesn’t currently exist in our dictionary, we will ignore this breaking character and output the code that matches the previous state of our character sequence. Then, we’ll add this new phrase with this breaking character into our dictionary and assign it a new code.

For example, let’s say our input text is:

```python
... app [cursor] appl ....
```

Our dictionary might look something like this:

```python
{
  ...
  "app": 324,
  ....
}
```

The next portion of text we come across is `appl` which isn’t currently in our dictionary. So, we’ll output the code for the existing phrase match of `app` and then we’ll add `appl` to our dictionary with a new code.The output after this iteration might look something like this:

```python
Dictionary: { … “app”: 324, “appl”: 325 …}
Output: … 324 …
```

This gives us a chance to build up to larger phrases and achieve greater compression. As the program processes the input and the dictionary grows, we’ll eventually be storing larger and larger strings. The longer the string, the more compression we can get by replacing it with a smaller code instead.

> This is just a very trivial implementation of Lempel-ziv. Nothing new in this!

## Second Issue

I worked a bit along the lines of minimax algorithm and came over a pretty interesting result.

Assume that we have a random variable $X$ drawn according to a distribution from the family $\{p_\theta\}$, where the parameter $\theta \in \{1, 2, \ldots, m\}$ is unknown. We wish to find an efficient code for this source. We wish to find a code that does well irrespective of the true distribution $\{p_\theta\}$ , and thus we define the minimax redundancy as
$$D_{*} = \min_{q} \max_{p_\theta} D\left(p_\theta \|q\right)$$
This minimax redundancy is achieved by a distribution $q$ that is at the `center` of the information ball containing the distributions $p_\theta$, that is, the distribution $q$ whose maximum distance from any of the distributions $p_\theta$ is minimized. To find the distribution $q$ that is as close as possible to all the possible $p_\theta$ in relative entropy, consider the following channel:

$$\begin{equation}
\theta \mapsto
\begin{pmatrix}
  \cdots & p_1 & \cdots \\
  \cdots & p_2 & \cdots \\
  \vdots  & \vdots  &  \vdots  \\
  \cdots & p_\theta & \cdots \\
  \vdots  & \vdots  &  \vdots  \\
  \cdots & p_m & \cdots \\
\end{pmatrix}
\mapsto X
\end{equation}
$$

This is a channel $\{\theta, p_\theta \left(x\right), X\}$ with the rows of the transition matrix equal to the different $p_\theta$’s, the possible distributions of the source. The capacity of this channel is given by:

$$
C = \max_{\pi\left(\theta\right)} I\left(\theta \;; X\right) = \max_{\pi\left(\theta\right)} \sum_{\theta\,,\; x} \pi\left(\theta\right)p_\theta\left(x\right)\log\frac{p_\theta\left(x\right)}{q_{\pi}\left(x\right)}
$$

where $${q_{\pi}\left(x\right)} = \sum_{\theta} \pi\left(\theta\right)p_\theta\left(x\right)$$
The distribution $q$ that achieves the minimum in the minimax is the output distribution $q^*(x)$ induced be the capacity-achieving input distribution $\pi_*(\theta)$ is $$q^{*}(x) = q_{\pi^{*}}(x) = \sum_{\theta} \pi^*(\theta) p_\theta(x)$$
Consider the following:
$$
\begin{equation}
\begin{aligned}
I(\theta; X) &= \sum_{i,j} \pi_i p_{ij} \log \frac{P_{ij}}{(q _\pi)_j}  \\
&= \sum_{i} \pi_i D(p_i\| q_\pi) \\
&= \sum_{i,j} \pi_i p_{ij} \log \frac{p_{ij} q_j}{q_j (q_\pi)_j} \\
&= \sum_{i,j} \pi_i p_{ij} \log \frac{p_{ij}}{q_j} + \sum_{i, j} \pi_i p_{ij} \log \frac{q_j}{(q_\pi)_j} \\
&= \sum_{i,j} \pi_i p_{ij} \log \frac{p_{ij}}{q_j} + \sum_j (q_\pi)_j \log \frac{q_j}{(q _\pi)_j} \\
&= \sum_{i,j} \pi_i p_{ij} \log \frac{p_{ij}}{q_j} - D(q_\pi \| q) \\
&= \sum_i \pi_i D(p_i \| q) - D(q_\pi \| q)\\
&\leq \sum_i \pi_i D(p_i \| q)
\end{aligned}
\end{equation}
$$
where $p_{ij} = p_\theta(x)$ for $\theta = i\; , x = j$. Then for any distribution $q$ on output, we have,
$$\sum_i \pi_i D(p_i \| q) \geq \sum_{i} \pi_i D(p_i\| q_\pi)$$
and therefore, $$I_\pi(\theta\,; X) = \min_q\sum_{i} \pi_i D(p_i\| q)$$
Hence, the channel capacity by definition is,
$$
\begin{equation}
\begin{aligned}
C &=\max_{\pi} I_{\pi}(\theta\,;X)\\
&=\max_{\pi}\min_{q}\sum_{i}\pi_{i}D(p_{i}\|q)\\
&= \min_{q}\max_{\pi} \sum_{i}\pi_{i}D(p_{i}\|q)
\end{aligned}
\end{equation}
$$
The last equality follows from the fact that, $\sum_{i}\pi_{i}D(p_{i}\|q)$  is convex in $q$ and concave in $\pi$ and the maximum is achieved by putting all the weight on the index $i$ maximizing $D(p_i\|q)$. So if we just calculate the channel capacity, we're done and we can even explicitly formulate the resulting p.m.f.

The only issue is that this algorithm is offline, we must have a finite set of alphabet. Now there are two problems:

- A cutoff must be generated so that less occuring code blocks are reduced as much as possible otherwise it would have a huge complexity issue.

- Needs a large class of ditribution of distributions, facing two problems:
  - We are restricting our universe to only those distributions. It would perform really well within that distribution but would perform really bad once we come out of the universe.

  - How to get all those possible class of p.m.fs required to generate the universe. My proposition is to use `corpus nltk` which contains some pretty famous literature in `.txt` format. Though I need some more suggestions.

>Try to put your suggestions in form of issues.
