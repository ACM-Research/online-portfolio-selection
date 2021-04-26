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
        #writer = ani.writers['ffmpeg'](fps=60, bitrate=1800)
        fig = plt.figure()
        crs = np.array([strat.cumulative_wealth for strat in strategies])
        def animate(i: int):
            cols = crs[..., :i]
            #print([len(col) for col in cols])
            for col in cols:
                plt.plot([j for j in range(len(col))], col)
            #p = plt.plot([[j for j in range(i)]] * len(cols), cols)
            #print(len(p))

        animator = ani.FuncAnimation(fig, animate, frames=60)
        animator.save(outputfile)

        # TODO add graph limits so it doesn't jump around
        #for strategy in strategies:
        #    plt.plot(strategy.cumulative_wealth, label=f'{strategy.__class__}')
        ##plt.legend()
        #plt.ylabel('Cumulative return')
        #plt.xlabel('Ticks')
        #plt.title('Cumulative return of different algorithms')
        #plt.savefig(outputfile)
