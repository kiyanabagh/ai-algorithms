#include <iostream>
#include <vector>
#include <cmath>
using namespace std;

int fitness(vector<int>& state) {
    int count = 0;
    for (int i = 0; i < 8; i++) {
        for (int j = i + 1; j < 8; j++) {
            if (state[i] != state[j] && abs(state[i] - state[j]) != abs(i - j)) {
                count++;
            }
        }
    }
    return count;
}

int main() {
    vector<int> test1 = {0, 4, 7, 5, 2, 6, 1, 3};
    vector<int> test2 = {0, 1, 2, 3, 4, 5, 6, 7};

    cout << "Fitness of [0,4,7,5,2,6,1,3]: " << fitness(test1) << endl;
    cout << "Fitness of [0,1,2,3,4,5,6,7]: " << fitness(test2) << endl;

    return 0;
}