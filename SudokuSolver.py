import numpy as np
from rich.progress import track
from rich.console import Console
import time

def get_test_cases(numTestcases):
    quizzes = np.zeros((1_000_000, 81), np.int32)
    solutions = np.zeros((1_000_000, 81), np.int32)
    for i, line in enumerate(open('sudoku.csv', 'r').read().splitlines()[1:numTestcases]):
        quiz, solution = line.split(",")
        for j, q_s in enumerate(zip(quiz, solution)):
            q, s = q_s
            quizzes[i, j] = q
            solutions[i, j] = s
    quizzes = quizzes.reshape((-1, 9, 9))
    solutions = solutions.reshape((-1, 9, 9))
    return quizzes, solutions

class Sudoku():
    def __init__(self, sudoku_numpy_list):
        self._sudoku_list = sudoku_numpy_list
    
    def verify(self):
        """
        return True if sudoku is solved
        False otherwise
        """

        #Checks if all x axis are correct
        for y in range(9):
            numbers = {1, 2, 3, 4, 5, 6, 7, 8, 9}
            for x in range(9):
                value = self._sudoku_list[x, y]
                if value in numbers:
                    numbers.remove(value)
                else:
                    return False
        #Checks if all y axis are correct
        for x in range(9):
            numbers = {1, 2, 3, 4, 5, 6, 7, 8, 9}
            for y in range(9):
                value = self._sudoku_list[x, y]
                if value in numbers:
                    numbers.remove(value)
                else:
                    return False
        #Checks if all squares are correct
        for i in range(3):
            for j in range(3):
                numbers = {1, 2, 3, 4, 5, 6, 7, 8, 9}
                for x in range(3):
                    for y in range(3):
                        value = self._sudoku_list[(3*i+x), (3*j+y)]
                        if value in numbers:
                            numbers.remove(value)
                        else:
                            return False                        

        return True

    def generateSets(self):
        setsColumns = [None for _ in range(9)]
        setsRows = [None for _ in range(9)]
        setsQuadrants = [[None for _ in range(3)] for _ in range(3)]

        candidates = {i for i in range(1, 10)}

        for i in range (9):
            setsColumns[i] = candidates - {x for x in self._sudoku_list[:,i]}
            setsRows[i] = candidates - {x for x in self._sudoku_list[i,:]}

        for i in range (3):
            for j in range (3):
                start_column = 3*j
                start_row = 3*i
                end_column = start_column+3
                end_row = start_row+3
                #print(self._sudoku_list[start_row:end_row, start_column:end_column].flatten())
                setsQuadrants[i][j] = candidates - {x for x in self._sudoku_list[start_row:end_row, start_column:end_column].flatten()}

        self.candidates = [[None for _ in range(9)] for _ in range(9)]
        for y in range (9):
            for x in range (9):
                self.candidates[x][y] = setsColumns[y] & setsRows[x] & setsQuadrants[x//3][y//3]



    

        #print(setsQuadrants)
        #print(self._sudoku_list)

    def solve(self):
        self.generateSets()

        changed = True
        while changed:
            changed = False
            for y in range (9):
                for x in range (9):
                    if len(self.candidates[x][y]) == 1:
                        if self._sudoku_list[x,y] == 0:
                            changed = True
                            self._sudoku_list[x,y] = list(self.candidates[x][y])[0]
                            
            self.generateSets()


        if self.verify() == True:

            return True

        else:
            #check if sudoku is unsolvable (leere felder keine kandidaten)
            for y in range (9):
                for x in range (9):
                    if len(self.candidates[x][y]) == 0 and self._sudoku_list[x,y] == 0:
                        return False
                 
            #state speichern
            current_state = self._sudoku_list.copy()
            
            #speichern wo man am raten ist feld und menge aller möglichkeiten für diesen fall updaten
            
            #for loop durch möglichkeiten raaten
            for y in range (9):
                for x in range (9):
                    if self._sudoku_list[x,y] == 0:
                        candidates = self.candidates[x][y].copy()
                        for i in candidates:
                            self._sudoku_list[x,y] = i
                            solved = self.solve()
                            if solved:                        
                                return True 
                            else:
                                self._sudoku_list = current_state.copy()
                        
            return False

if __name__ == "__main__":
    numTestcases = 10000
    console = Console()
    with console.status("[bold green]Reading File...") as status:
        quizzes, solutions = get_test_cases(numTestcases+1)
    num_unsolvable = 0
    start = time.time()
    for i in track(range(numTestcases), description='[green]Processing data'):
        test = Sudoku(quizzes[i])
        solved = test.solve()
        if not solved:
            num_unsolvable += 1
            print(test._sudoku_list)
    print(f"Time: {time.time()-start}")
    print("Finished, Unsolvable: ", num_unsolvable)
    
