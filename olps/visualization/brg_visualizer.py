import matplotlib.pyplot as plt
import matplotlib.animation as ani
import numpy as np
from olps.strategies.strategy import Strategy
from .visualizer import Visualizer

class BarCRGVisualizer(Visualizer):
    """
    Class for visualizing cumulative return of multiple strategies as a graph (Cumulative Return Graph)
    """

    @staticmethod
    def visualize(outputfile: str, strategies: list[Strategy], asset_names: list[str]):
        """
        Plots the strategies' cumulative return to the output file in a single graph
        """

        colors = ['r', 'b', 'g', 'y', 'c', 'm', 'k', 'tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan']
        
        N = len(strategies)
        ind = np.arange(N)
        width = 0.2 / len(strategies)

        fig = plt.figure()
        ax = fig.add_subplot(111)
        
        def autolabel(rects):
            for rect in rects:
                h = rect.get_height()
                ax.text(rect.get_x()+rect.get_width()/2., 1.05*h, '%d'%int(h),
                        ha='center', va='bottom')

        asset_weights = strategies[0].weights
        for i in range(1, len(strategies)):
            asset_weights = np.column_stack((asset_weights, strategies[i].weights.T))
        

        rect_list = []
        for weights in range(len(asset_weights)):
            yvals = asset_weights[weights]
            rect = ax.bar((ind + (width * weights)), yvals, width, color = colors[weights % len(colors)])
            autolabel(rect)
            rect_list.append(rect)
        
        strategies_names_list = [type(strat).__name__ for strat in strategies]

        ax.set_ylabel('Portfolio Distributions by Strategy')
        ax.set_xticks(ind + width)
        ax.set_xticklabels( tuple(strategies_names_list) )
        ax.legend( tuple(rect_list), tuple(asset_names))

        plt.savefig(outputfile)