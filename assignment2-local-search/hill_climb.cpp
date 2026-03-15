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
        cout << "Usage: hill_climb input_filename" << endl;
        return 1;
    }

    ifstream file(argv[1]);
    if (!file.is_open()) {
        cout << "Could not open file" << endl;
        return 1;
    }

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

        while (true) {
            int currentFitness = fitness(current);
            if (currentFitness == 28) break;

            vector<vector<int>> neighbors = getNeighbors(current);
            nodesExplored += neighbors.size();

            int bestFitness = currentFitness;
            vector<int> bestNeighbor = current;

            for (auto& neighbor : neighbors) {
                int f = fitness(neighbor);
                if (f > bestFitness) {
                    bestFitness = f;
                    bestNeighbor = neighbor;
                }
            }

            if (bestFitness <= currentFitness) break;
            current = bestNeighbor;
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