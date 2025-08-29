from collections import Counter
from fractions import Fraction
from time import perf_counter

# Internal data
totient = []
sigma = []
g = []
pfactorize = []

def load_phigma(max_n, filepath):
    """Load precomputed totient and sigma values from a file."""

    start = perf_counter()
    print("Loading totient and sigma...\t\t", end=' ', flush=True)

    global totient, sigma
    totient = [0] * (max_n + 1)
    sigma = [0] * (max_n + 1)
    with open(f"{filepath}/phigma.csv") as h:
        for line in h.read().split("\n"):
            if not line.strip():
                continue
            a, b, c = map(int, line.split(" "))
            if a > max_n:
                break
            totient[a] = b
            sigma[a] = c
            
    print(f"finished ({int((perf_counter() - start) * 1000)} ms)")

def load_g(max_n, filepath):
    """Load precomputed totient and sigma values from a file."""
    
    start = perf_counter()
    print("Loading g...\t\t\t\t", end=' ', flush=True)

    global g
    g = [None] * (max_n + 1)
    with open(f"{filepath}/g.csv") as h:
        for line in h.read().split("\n"):
            if not line.strip():
                continue
            a, b, c = map(int, line.split(" "))
            if a > max_n:
                break
            g[a] = (b, c)
    
    print(f"finished ({int((perf_counter() - start) * 1000)} ms)")

def init_pfactorize(max_n):
    """Precompute prime factorizations up to max_n."""
    start = perf_counter()
    print("Computing prime factorizations...\t", end=' ', flush=True)

    global pfactorize
    pfactorize = [Counter() for _ in range(max_n + 1)]
    for i in range(2, max_n + 1):
        if pfactorize[i]:
            continue
        pow_i = i
        while pow_i <= max_n:
            for j in range(pow_i, max_n + 1, pow_i):
                pfactorize[j][i] += 1
            if pow_i > max_n // i:
                break
            pow_i *= i

    print(f"finished ({int((perf_counter() - start) * 1000)} ms)")

def init(max_n=1000, filepath="precomputed"):
    """Initialize totient, sigma, g, and prime factorization arrays with detailed ms timing."""

    global_start = perf_counter()
    print(f"Initializing precomputed data up to n={max_n}...\n")
    
    load_phigma(max_n, filepath)
    #load_g(max_n, filepath)
    init_pfactorize(max_n)
    
    print(f"\nInitialization completed in {int((perf_counter() - global_start) * 1000)} ms")
