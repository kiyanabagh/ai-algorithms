#include <iostream>
#include <vector>
#include <fstream>
#include <sstream>
#include <cmath>
#include <ctime> // used only for clock() to measure Time Taken as required by output format
#include <random>
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

void printState(vector<int>& state) {
    cout << "[";
    for (int i = 0; i < 8; i++) {
        cout << state[i];
        if (i < 7) cout << ", ";
    }
    cout << "]";
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        cout << "Usage: sim_anneal input_filename" << endl;
        return 1;
    }

    ifstream file(argv[1]);
    if (!file.is_open()) {
        cout << "Could not open file" << endl;
        return 1;
    }

    mt19937 rng(42);

    string line;
    int caseNum = 1;

    while (getline(file, line)) {
        if (line.empty()) continue;

        vector<int> state;
        istringstream iss(line);
        int val;
        while (iss >> val) state.push_back(val);

        clock_t start = clock();

        vector<int> current = state;
        int nodesExplored = 0;

        double T = 1000.0;
        double coolingRate = 0.999;
        double minTemp = 0.001;

        while (T > minTemp) {
            int currentFitness = fitness(current);
            if (currentFitness == 28) break;

            // pick random neighbor
            int col = rng() % 8;
            int row = rng() % 7;
            if (row >= current[col]) row++;

            vector<int> next = current;
            next[col] = row;
            nodesExplored++;

            int delta = fitness(next) - currentFitness;

            if (delta > 0) {
                current = next;
            } else {
                double prob = exp((double)delta / T);
                uniform_real_distribution<double> dist(0.0, 1.0);
                if (dist(rng) < prob) {
                    current = next;
                }
            }

            T *= coolingRate;
        }

        clock_t end = clock();
        double timeTaken = double(end - start) / CLOCKS_PER_SEC;
        int finalFitness = fitness(current);

        cout << "--- Case " << caseNum << ": Input ";
        printState(state);
        cout << " ---" << endl;
        cout << "Final Fitness: " << finalFitness << "/28" << endl;
        cout << "Nodes Explored: " << nodesExplored << endl;
        cout << "Goal State:     ";
        printState(current);
        cout << endl;
        cout << "Time Taken:     " << timeTaken << "s" << endl;
        cout << "----------------------------------------" << endl;

        caseNum++;
    }

    file.close();
    return 0;
}