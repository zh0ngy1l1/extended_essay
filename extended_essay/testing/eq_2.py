"""
This program will determine how many values n != 2 exist such that f(n) = f(2),
in other words the line with density 1/n and the line with density 1/2 coincide.
"""

print("Loading data...")

from funcs import N, totient, sigma, pfactorize
from fractions import Fraction

n_max = min(N, 1000000)
def f(x):
    return Fraction(totient[x]*sigma[x], x**2)
print("Defined f(n) = phi(n)sigma(n)/n^2")

t=3
print(f"Finding values {t} < n < {n_max} for which f(n) = f({t})")

found = False
for i in range(t+1, n_max+1):
    if f(i) == f(t):
        print(f"Found solution f({i}) = f({t})")
        found = True

if not found:
    print("No solutions found.")
