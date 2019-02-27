import time
import random
import numpy as np
import math

class Board(object):
    """An N-queens candidate solution ."""

    def __init__(self,N):
        """A random N-queens instance"""
        self.queens = dict()
        for col in range(N):
            row = random.choice(range(N))
            self.queens[col] = row
        
    def display(self):
        """Print the board."""
        for r in range(len(self.queens)):
            for c in range(len(self.queens)):
                if self.queens[c] == r:
                    print 'Q',
                else:
                    print '-',
            print
        print "cost: ", self.cost()
        print

    def copy(self,board):
        """Copy a board (prevent aliasing)"""
        self.queens = board.queens.copy()
        
    def moves(self):
        """Return a list of possible moves given the current placements."""
        # YOU FILL THIS IN
        moveList = []
        x = self
        for queen in range(8):
            #move
            for move in range(1,8):
                x.queens[queen] = (x.queens[queen] + move) % 8
                moveList.append(x)
        return moveList

    def neighbor(self, move):
        """Return a Board instance like this one but with one move made."""
        # YOU FILL THIS IN
        #Random select queen
        x = self
        queen = random.choice(range(8))
        #Random col move
        col = random.choice(range(8))
        x.queens[queen] = (x.queens[queen] + col ) % 8
        return x

    def crossover(self, board):
        """Return a Board instance that is a recombination with its argument."""
        # random crossover point
        x = Board(8)
        crossval = random.choice(range(8))
        for col in range(0, crossval):
            x.queens[col] = self.queens[col]
        for col in range(crossval, 8):
            x.queens[col] = board.queens[col]
        return x

    def cost(self):
        """Compute the cost of this solution."""
        # YOU FILL THIS IN
        result = 0;
        #check queens cost
        for queen in range(7):
            for queenN in range(queen+1, 8):
                #in the diagnose                                                           in the vertical 
                if (abs(queenN - queen) == abs(self.queens[queenN] - self.queens[queen])) or self.queens[queen] == self.queens[queenN]:
                   result += 1
        return result

class EvolutionaryAlgorithm(object):
    """Evolve solutions to the n-queens problem"""

    def evolve(self, popsize, pc):
        """popsize: population size, pc: crossover probability"""
        
        ## Initial population
        population = []
        for i in range(popsize):
            population.append(Board(8));

        steps = 0
        ## While problem is not solved    
        while(population[0].cost() > 0):

            ## Uniform random parent selection
            x = population[random.choice(range(popsize))]

            ## Crossover with probability pc
            if random.random() < pc:
                y = population[random.choice(range(popsize))]
                x = x.crossover(y)

            ## Mutation (take a short random walk)
            for i in range(np.random.poisson()+1):                
                mlist = x.moves()
                x = x.neighbor(random.choice(mlist));            

            ## Truncation selection
            population.append(x)
          
            ## sort population by fitness, remove least fit
            population = [x for _, x in sorted(zip(map(Board.cost,population),population))]
            population.pop()

            #population[0].display()
            ## Display best every 1000 generations
            ##
            if (steps % 1000 == 0):
                population[0].display()

                time.sleep(0.1)

            steps = steps+1
        population[0].display()
        return steps

class SimulatedAnnealing(object):
    def anneal(self,startTemp,decayRate):
        ## Initial random board
        x = Board(8);
        t = startTemp
        steps = 0
        while x.cost() > 0:
            E_before = x.cost()
            mlist = x.moves()
            x_after = x.neighbor(random.choice(mlist))
            E_after = x_after.cost()
            Delta = E_before - E_after

            if(Delta > 0):
                #good move
                x = x_after
            elif math.exp(Delta/startTemp)>random.random():
                x = x_after
            ##
            ## YOU FILL IN HERE            
            ##
            
            ## Display best every 1000 steps
            startTemp -= decayRate
            if (steps % 1000 == 0):
                x.display()
                time.sleep(0.1)
            steps = steps+1
            
        x.display()
        return steps
        

def main():
    """Create a problem, solve it with simulated anealing, and console-animate."""

    ea = EvolutionaryAlgorithm();
    ea_steps = ea.evolve(100,0.5);
    sa = SimulatedAnnealing()
    sa_steps = sa.anneal(1000,0.999)

    print "The evolutionary algorithm solved the problem in ", ea_steps, " steps"
    print "Simulated annealing solved the problem in ", sa_steps, " steps"

if __name__ == '__main__':
    main()
