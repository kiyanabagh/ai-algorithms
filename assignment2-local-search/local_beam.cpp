#include <iostream>
#include <vector>
#include <fstream>
#include <sstream>
#include <cmath>
#include <ctime> // used only for clock() to measure Time Taken as required by output format
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

vector<vector<int>> getNeighbors(vector<int>& state) {
    vector<vector<int>> neighbors;
    for (int col = 0; col < 8; col++) {
        for (int row = 0; row < 8; row++) {
            if (row != state[col]) {
                vector<int> neighbor = state;
                neighbor[col] = row;
                neighbors.push_back(neighbor);
            }
        }
    }
    return neighbors;
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
        cout << "Usage: local_beam input_filename" << endl;
        return 1;
    }

    ifstream file(argv[1]);
    if (!file.is_open()) {
        cout << "Could not open file" << endl;
        return 1;
    }

    vector<vector<int>> beam;
    string line;

    while (getline(file, line)) {
        if (line.empty()) continue;
        vector<int> state;
        istringstream iss(line);
        int val;
        while (iss >> val) state.push_back(val);
        beam.push_back(state);
    }
    file.close();

    int k = beam.size();
    clock_t start = clock();

    int nodesExplored = 0;
    vector<int> goalState;
    int finalFitness = 0;
    bool found = false;

    cout << "Starting Local Beam Search with " << k << " initial states..." << endl;

    while (!found) {
        // generate all neighbors of all k states
        vector<vector<int>> allNeighbors;
        for (int i = 0; i < k; i++) {
            vector<vector<int>> neighbors = getNeighbors(beam[i]);
            for (auto& n : neighbors) {
                allNeighbors.push_back(n);
            }
        }

        nodesExplored += allNeighbors.size();

        // check for goal in neighbors
        for (auto& n : allNeighbors) {
            if (fitness(const_cast<vector<int>&>(n)) == 28) {
                goalState = n;
                finalFitness = 28;
                found = true;
                break;
            }
        }

        if (found) break;

        // sort all neighbors by fitness descending, keep top k
        // simple selection sort for top k
        for (int i = 0; i < k && i < (int)allNeighbors.size(); i++) {
            int bestIdx = i;
            int bestF = fitness(allNeighbors[i]);
            for (int j = i + 1; j < (int)allNeighbors.size(); j++) {
                int f = fitness(allNeighbors[j]);
                if (f > bestF) {
                    bestF = f;
                    bestIdx = j;
                }
            }
            swap(allNeighbors[i], allNeighbors[bestIdx]);
        }

        beam.clear();
        for (int i = 0; i < k; i++) {
            beam.push_back(allNeighbors[i]);
        }
    }

    clock_t end = clock();
    double timeTaken = double(end - start) / CLOCKS_PER_SEC;

    cout << "Final Fitness: " << finalFitness << "/28" << endl;
    cout << "Nodes Explored: " << nodesExplored << endl;
    cout << "Goal State:     ";
    printState(goalState);
    cout << endl;
    cout << "Time Taken:     " << timeTaken << "s" << endl;

    return 0;
}