#include <bits/stdc++.h>
using namespace std;
using ull = unsigned long long;

const int N = 10000000;
pair<ull,ull> g[N+1];
bool is_prime[N+1];

int main(){
    // --- 1) initialize ---
    for(int i = 1; i <= N; i++){
        g[i] = {1, 1};
        is_prime[i] = true;
    }
    is_prime[0] = is_prime[1] = false;

    // --- 2) sieve + build g multiplicatively ---
    for(int p = 2; p <= N; p++){
        if(!is_prime[p]) continue;
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
            //   num = p^(α+1) - 1
            //   den = p^(α+1)
            ull num = p_pow * p - 1;
            ull den = p_pow * p;

            // multiply into g[j] and immediately reduce
            g[j].first  *= num;
            g[j].second *= den;
            ull d = gcd(g[j].first, g[j].second);
            g[j].first  /= d;
            g[j].second /= d;
        }
    }

    // --- 3) output ---
    namespace fs = std::filesystem;
    fs::create_directory("precomputed"); // Creates dir if it doesn't exist
    
    ofstream f;
    f.open("precomputed/g.csv");

    for(int i = 1; i <= N; i++){
        f << i
             << ' ' << g[i].first
             << ' ' << g[i].second
             << "\n";
    }
    f.close();
    return 0;
}
