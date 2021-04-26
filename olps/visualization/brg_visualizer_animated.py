import matplotlib.pyplot as plt
import matplotlib.animation as ani
import numpy as np
import ffmpeg
from olps.strategies.strategy import Strategy
from .visualizer import Visualizer

class BarCRGVisualizer(Visualizer):
    """
    Class for visualizing cumulative return of multiple strategies as a graph (Cumulative Return Graph)
    """
    @staticmethod
    def visualize(outputfile: str, strategies: list[Strategy]):
        """
        Plots the strategies' cumulative return to the output file in a single graph
        """
        fig = plt.figure()
        bar = 'vertical'
        crs = np.array([strat.weights for strat in strategies])
        def animate(i: int):
            iv = min(i, len(crs)-1) 
            performance = crs[iv]
            plt.bar(x= i ,height= performance, align='center', color=['red', 'green', 'blue', 'orange'])

        animator = ani.FuncAnimation(fig, animate, frames=60)
        animator.save(outputfile)