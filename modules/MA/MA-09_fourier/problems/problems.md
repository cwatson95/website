# MA-09 — Problems

Work by hand, then check with `code/fourier.py`. Citations in `../refs.md`.

### P1.  Fourier series of a square wave  *(Boas 3e §7.5, p.350)*
Compute the coefficients of the odd square wave (period 1) and show bₙ = 4/(nπ)
for odd n, 0 otherwise (and all aₙ = 0). *Check:* `fourier_series_coeffs(sq, 1, 5)`.

**Solution.** The odd square wave has $f(x)=+1$ on $(0,\tfrac12)$ and $-1$ on $(\tfrac12,1)$. Being odd, every $a_n=0$ (and $a_0=0$). With $P=1$ the sine coefficient is
$$b_n=2\!\int_0^1 f\sin(2\pi n x)\,dx=2\Big[\int_0^{1/2}\!\sin(2\pi n x)\,dx-\int_{1/2}^{1}\!\sin(2\pi n x)\,dx\Big].$$
Each integral gives $\tfrac{1-\cos\pi n}{2\pi n}$ and $\tfrac{\cos\pi n-1}{2\pi n}$, so
$$b_n=2\cdot\frac{1-\cos\pi n}{\pi n}=\frac{2\big(1-(-1)^n\big)}{\pi n}=\begin{cases}\dfrac{4}{\pi n}&n\text{ odd}\\[2pt]0&n\text{ even.}\end{cases}$$
Numerically `fourier_series_coeffs(sq, 1, 5)` returns $a_0=0$, all $a_n=0$, and $b=[1.2732,0,0.4244,0,0.2546]$, exactly $4/(\pi n)=\{1.2732,0.4244,0.2546\}$ for $n=1,3,5$.

### P2.  Orthogonality / Fourier's trick  *(Boas 3e §7.5, p.350)*
Verify ∫₀^P sin(2πmx/P)sin(2πnx/P)dx = (P/2)δₘₙ — the orthogonality that isolates
each coefficient. Then reconstruct a two-mode signal exactly. *Check:*
`series_value` of the coefficients of `0.5 + cos(2πx) + 0.3 sin(4πx)`.

**Solution.** Use the product-to-sum identity $\sin A\sin B=\tfrac12[\cos(A-B)-\cos(A+B)]$ with $A=\tfrac{2\pi m x}{P},\,B=\tfrac{2\pi n x}{P}$:
$$\int_0^P\!\sin\tfrac{2\pi m x}{P}\sin\tfrac{2\pi n x}{P}\,dx=\tfrac12\!\int_0^P\!\big[\cos\tfrac{2\pi(m-n)x}{P}-\cos\tfrac{2\pi(m+n)x}{P}\big]dx.$$
For $m\ne n$ both cosines complete whole cycles and integrate to $0$; for $m=n$ the first term is $\cos 0=1$ giving $\tfrac12P$, the second still vanishes — hence $\tfrac{P}{2}\delta_{mn}$. This orthogonality is what makes "Fourier's trick" pick out one coefficient. The signal $0.5+\cos(2\pi x)+0.3\sin(4\pi x)$ ($P=1$) is *already* a finite series: $a_0/2=0.5,\ a_1=1,\ b_2=0.3$, all others zero — and indeed `fourier_series_coeffs` returns $a_0=1,\,a_1=1,\,b_2=0.3$, so `series_value` reconstructs it with zero error.

### P3.  DFT of a pure tone  *(Boas 3e §7.7, p.358)*
Sample cos(2π·k₀·n/N) and show the DFT has nonzero bins only at k₀ and N−k₀,
each of magnitude N/2. *Check:* `dft([cos(2*pi*k0*n/N) for n in range(N)])`.

**Solution.** Write the sample with Euler's formula, $x_n=\cos\tfrac{2\pi k_0 n}{N}=\tfrac12\big(e^{2\pi i k_0 n/N}+e^{-2\pi i k_0 n/N}\big)$, and feed it to the DFT kernel:
$$X_k=\sum_{n=0}^{N-1}x_n\,e^{-2\pi i k n/N}=\tfrac12\sum_{n=0}^{N-1}\Big[e^{2\pi i(k_0-k)n/N}+e^{-2\pi i(k_0+k)n/N}\Big].$$
The geometric sum $\sum_{n=0}^{N-1}e^{2\pi i j n/N}=N$ when $j\equiv 0\ (\mathrm{mod}\ N)$ and $0$ otherwise. So only $k=k_0$ and $k=N-k_0$ (since $-k_0\equiv N-k_0$) survive, each with $X_k=N/2$. For $N=16,\,k_0=2$, `dft` gives $|X_2|=|X_{14}|=8.0=N/2$ and all other bins $0$.

### P4.  Parseval's theorem  *(Boas 3e §7.11, p.375)*
For any signal show Σₙ|xₙ|² = (1/N)Σₖ|Xₖ|² (energy is conserved between time and
frequency). *Check:* compare the two sums for a random complex `x` and its `dft`.

**Solution.** Insert the inverse DFT $x_n=\tfrac1N\sum_k X_k e^{2\pi i k n/N}$ into $\sum_n|x_n|^2=\sum_n x_n^{*}x_n$ and swap the order of summation:
$$\sum_n |x_n|^2=\sum_n x_n^{*}\,\frac1N\sum_k X_k e^{2\pi i k n/N}=\frac1N\sum_k X_k\Big(\underbrace{\sum_n x_n e^{-2\pi i k n/N}}_{=\,X_k}\Big)^{*}=\frac1N\sum_k |X_k|^2.$$
The inner sum is exactly the DFT $X_k$, so its conjugate times $X_k$ gives $|X_k|^2$. Energy is conserved up to the $1/N$ convention of this transform. Numerically, for a random complex length-8 `x`, both $\sum_n|x_n|^2$ and $\tfrac1N\sum_k|X_k|^2$ equal $12.404901$.

### P5.  FFT vs DFT  *(numerical)*
Confirm the radix-2 FFT returns the same array as the direct DFT for N = 2,4,8,16,
and note it is O(N log N) vs O(N²). *Check:* `fft(x)` ≈ `dft(x)`.

**Solution.** Split the DFT sum by parity of $n$ (Cooley–Tukey). With $x_n^{\text{ev}}=x_{2m}$ and $x_n^{\text{od}}=x_{2m+1}$,
$$X_k=\sum_{m}x_{2m}e^{-2\pi i k(2m)/N}+\sum_{m}x_{2m+1}e^{-2\pi i k(2m+1)/N}=E_k+e^{-2\pi i k/N}\,O_k,$$
where $E_k,O_k$ are length-$N/2$ DFTs. Recursing halves the problem each level, giving $\log_2 N$ levels of $O(N)$ work — $O(N\log N)$ total versus $O(N^2)$ for the direct double sum. The two produce the *same* array up to floating-point roundoff: `fft` vs `dft` differ by at most $\sim2.6\times10^{-14}$ for $N=2,4,8,16$, confirming `fft(x)` ≈ `dft(x)`.
