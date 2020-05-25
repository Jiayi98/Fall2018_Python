import random

class Graph(object):
    """A constuctor that can read/Users/user/Desktop/final_project/final.py the input
    and build according probability model
    dict:{state:Neighbors}
    Neighbors:{token:freq}
    """
    
    def __init__(self, state):
        self.dict = {} # key is state, value is its Neighbors
        self.prev = state
        self.dict[self.prev] = Neighbor(state)
    

            
    def addNeighbor(self, state):
        if state not in self.dict:
            self.dict[state] = Neighbor(state)
        
        self.dict[self.prev].add(state)
        self.prev = state
        

    def getNeighbors(self, state):
        return self.dict[state]


    def getSelected(self, current):
        s = self.dict[current].randomSelect()
        return s





import random

class Neighbor(object):
    def __init__(self,state):
        self.prev = state
        self.dict = {} # key is state; value is its frequency
        self.total = 0 #sum of all neighbor's frequencies
    
    def add(self, state):
        self.total += 1
        if state not in self.dict:
            self.dict[state] = 1
        else:
            num = self.dict[state] + 1
            self.dict[state] = num

    def randomSelect(self):
        n = random.randint(1,self.total)
        #print(n)
        for state,freq in self.dict.items():
            n -= freq
            if n <= 0:
                #print("FIND IT !!!!!!", state)
                return state

        #return "DEBUG: no token being selected"








    


