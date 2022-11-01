from abc import ABC, abstractmethod, abstractproperty
from re import search

class SearchAlgorithm(ABC):
    frontier = []
    results = []
    
    @abstractmethod
    def get_next(self):
        pass
    
    def expand_frontier(self, expansion):
        self.frontier.extend(expansion)

    def add_result(self, result):
        self.results.append(result)

class BFS(SearchAlgorithm): 
    def get_next(self):
        return self.frontier.pop(0)
    
class DFS(SearchAlgorithm): 
    def get_next(self):
        return self.frontier.pop()