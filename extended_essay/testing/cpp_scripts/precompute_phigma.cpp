#include <bits/stdc++.h>
using namespace std;
using ull = unsigned long long;

const int N = 10000000;
ull phi[N + 1], sigma[N + 1];
bool is_prime[N + 1];

int main(){
    // --- 1) initialize ---
    for(int i = 1; i <= N; i++){
        phi[i] = sigma[i] = 1;
        is_prime[i] = true;
    }

    // --- 2) sieve + build phi and sigma multiplicatively ---
    for (int p = 2; p <= N; p++) {
        if (!is_prime[p]) continue;
        // mark multiples as composite
        for(int k = 2*p; k <= N; k += p)
            is_prime[k] = false;

        // for each multiple j of p, pull off exponent α
        for(int j = p; j <= N; j += p){
            // find highest p^α dividing j
            ull p_pow = p;
            while(j % (p_pow * p) == 0)
                p_pow *= p;
            // now p_pow = p^α, so contribution is
            //   phi = p^α - p^(α-1)
            //   sigma = (p^(α+1) - 1) / (p - 1)
            ull dphi = p_pow - p_pow / p;
            ull dsig = (p_pow * p - 1) / (p - 1);
            phi[j] *= dphi;
            sigma[j] *= dsig;
        }
    }

    // --- 3) output ---
    namespace fs = std::filesystem;
    fs::create_directory("precomputed"); // Creates dir if it doesn't exist

    ofstream f;
    f.open("precomputed/phigma.csv");
    
    
    for(int i = 1; i <= N; i++){
        f << i
             << ' ' << phi[i]
             << ' ' << sigma[i]
             << "\n";
    }
    f.close();
    return 0;
}
