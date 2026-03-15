#include <iostream>
#include <vector>
#include <fstream>
#include <sstream>
#include <cmath>
#include <ctime> // used only for clock() to measure Time Taken as required by output format
#include <random>
using namespace std;

mt19937 rng(42);

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

vector<int> selectParent(vector<vector<int>>& population, vector<int>& fitnesses) {
    int total = 0;
    for (int f : fitnesses) total += f;

    uniform_int_distribution<int> dist(0, total - 1);
    int pick = dist(rng);

    int running = 0;
    for (int i = 0; i < (int)population.size(); i++) {
        running += fitnesses[i];
        if (running > pick) return population[i];
    }
    return population.back();
}

pair<vector<int>, vector<int>> crossover(vector<int>& a, vector<int>& b) {
    uniform_int_distribution<int> dist(1, 6);
    int point = dist(rng);

    vector<int> child1, child2;
    for (int i = 0; i < 8; i++) {
        if (i < point) {
            child1.push_back(a[i]);
            child2.push_back(b[i]);
        } else {
            child1.push_back(b[i]);
            child2.push_back(a[i]);
        }
    }
    return make_pair(child1, child2);
}

void mutate(vector<int>& state, double mutationRate) {
    uniform_real_distribution<double> prob(0.0, 1.0);
    uniform_int_distribution<int> row(0, 7);

    for (int i = 0; i < 8; i++) {
        if (prob(rng) < mutationRate) {
            state[i] = row(rng);
        }
    }
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        cout << "Usage: genetic input_filename" << endl;
        return 1;
    }

    ifstream file(argv[1]);
    if (!file.is_open()) {
        cout << "Could not open file" << endl;
        return 1;
    }

    vector<vector<int>> population;
    string line;

    while (getline(file, line)) {
        if (line.empty()) continue;
        vector<int> state;
        istringstream iss(line);
        int val;
        while (iss >> val) state.push_back(val);
        population.push_back(state);
    }
    file.close();

    clock_t start = clock();

    int nodesExplored = 0;
    int maxNodes = 400000;
    double mutationRate = 0.05;

    vector<int> bestState = population[0];
    int bestFitness = fitness(bestState);
    bool found = false;

    while (nodesExplored < maxNodes && !found) {
        vector<int> fitnesses;
        for (int i = 0; i < (int)population.size(); i++) {
            int f = fitness(population[i]);
            fitnesses.push_back(f);
            nodesExplored++;

            if (f > bestFitness) {
                bestFitness = f;
                bestState = population[i];
            }
            if (f == 28) {
                found = true;
                break;
            }
        }

        if (found) break;

        vector<vector<int>> newPop;
        while ((int)newPop.size() < (int)population.size()) {
            vector<int> parent1 = selectParent(population, fitnesses);
            vector<int> parent2 = selectParent(population, fitnesses);

            pair<vector<int>, vector<int>> result = crossover(parent1, parent2);
            vector<int> child1 = result.first;
            vector<int> child2 = result.second;

            mutate(child1, mutationRate);
            mutate(child2, mutationRate);

            newPop.push_back(child1);
            if ((int)newPop.size() < (int)population.size()) newPop.push_back(child2);
        }

        population = newPop;
    }

    clock_t end = clock();
    double timeTaken = double(end - start) / CLOCKS_PER_SEC;

    cout << "Nodes Explored: " << nodesExplored << endl;
    cout << "Goal State: ";
    printState(bestState);
    cout << endl;
    cout << "Final Fitness: " << bestFitness << endl;
    cout << "Time Taken: " << timeTaken << endl;

    return 0;
}