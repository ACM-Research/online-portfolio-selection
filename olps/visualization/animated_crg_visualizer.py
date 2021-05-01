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
        strategy_names = [
                f'{strategy.__class__}'[:-2].split('.')[-1]
                for strategy in strategies]

        plt.xlim((0, len(crs[0])))

        def animate(i: int):
            cols = [row[:i] for row in crs]
            if len(cols) != len(strategy_names):
                return
            # manually defining colors keeps them consistent
            for name, col, color in zip(strategy_names, cols, colors):
                plt.plot([j for j in range(len(col))], col, color=color, label=name)
            plt.legend(strategy_names)

        animator = ani.FuncAnimation(fig, animate, save_count=len(crs[0]))
        animator.save(outputfile)
