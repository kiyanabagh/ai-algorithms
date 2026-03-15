def terminal_test(self):
        return self.utility() is not None

def utility(self):
    wins = [(0,1,2),(3,4,5),(6,7,8),
            (0,3,6),(1,4,7),(2,5,8),
            (0,4,8),(2,4,6)]
    for (i,j,k) in wins:
        if self.board[i] == self.board[j] == self.board[k] != ' ':
            return 1 if self.board[i] == 'X' else -1
    if ' ' not in self.board:
        return 0
    return None