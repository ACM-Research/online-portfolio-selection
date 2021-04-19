import matplotlib.pyplot as plt
from olps.strategies.strategy import Strategy
from typing import *

class Visualizer:
    """
    Class for visualizing cumulative wealth of multiple strategies
    """
    outputfile: str
    strategies: list[Strategy]

    def __init__(self, outputfile: str, strategies: list[Strategy]):
        """
        Initialize the visualizer with already run strategies and output file
        """
        self.outputfile = outputfile
        self.strategies = strategies

    def visualize(self):
        """
        Plots the strategies to the output file in a single graph
        """
        print(f'Attempting to write to {self.outputfile}')
        for strategy in self.strategies:
            plt.plot(strategy.cumulative_wealth, label=f'{strategy.__class__}')
        #plt.legend()
        plt.ylabel('Cumulative return')
        plt.xlabel('Ticks')
        plt.title('Cumulative return of different algorithms')
        plt.savefig(self.outputfile)
