#include <bits/stdc++.h>
using namespace std;
#define int unsigned long long

const int N = 1000000;
multiset<int> pfactorize[N+1];
int phi[N+1], sigma[N+1];

void init_pfactorize() {
    for (int i = 1; i <= N; i++) {
        phi[i] = i;
        sigma[i] = 1;
    }
    
    for (int i = 2; i <= N; i++) {
        if (!pfactorize[i].empty()) continue;
        
        for (int pow = i; pow <= N; pow *= i) {
            for (int j = pow; j <= N; j += pow) {
                pfactorize[j].insert(i);
            }
        }
        
        for (int j = i; j <= N; j += i) {
            phi[j] = phi[j] / i * (i - 1);
            
            int p_power = i, sum_p_power = 1 + i;
            while (j % (p_power * i) == 0) {
                p_power *= i;
                sum_p_power += p_power;
            }
            sigma[j] *= sum_p_power;
        }
    }
}


signed main() {
    init_pfactorize();

    for (int i = 1; i <= N; i++) {
        cout << i << " " << phi[i] << " " << sigma[i] << "\n";
    }
    
    return 0;
}