import matplotlib.pyplot as plt
from olps.strategies.strategy import Strategy
from .visualizer import Visualizer

class CRGVisualizer(Visualizer):
    """
    Class for visualizing cumulative return of multiple strategies as a graph (Cumulative Return Graph)
    """
    @staticmethod
    def visualize(outputfile: str, strategies: list[Strategy]):
        """
        Plots the strategies' cumulative return to the output file in a single graph
        """
        for strategy in strategies:
            plt.plot(strategy.cumulative_wealth, label=f'{strategy.__class__}')
        #plt.legend()
        plt.ylabel('Cumulative return')
        plt.xlabel('Ticks')
        plt.title('Cumulative return of different algorithms')
        plt.savefig(outputfile)
