import matplotlib.pyplot as plt
import matplotlib.animation as ani
import numpy as np
from olps.strategies.strategy import Strategy
from .visualizer import Visualizer

class AnimatedCRGVisualizer(Visualizer):
    """
    Class for animating cumulative return of multiple strategies as a graph (Cumulative Return Graph)
    """
    @staticmethod
    def visualize(outputfile: str, strategies: list[Strategy]):
        """
        Plots the strategies' cumulative return to the output file in a single graph by animating them
        """
        # https://matplotlib.org/stable/tutorials/colors/colors.html
        # single character notation for the colors
        colors = 'bgrcmyk'
        fig = plt.figure()
        crs = np.array([strat.cumulative_wealth for strat in strategies])
        def animate(i: int):
            cols = crs[..., :i]
            # manually defining colors keeps them consistent
            for col, color in zip(cols, colors):
                plt.plot([j for j in range(len(col))], col, color=color)

        animator = ani.FuncAnimation(fig, animate, frames=60)
        animator.save(outputfile)
