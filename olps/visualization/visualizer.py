import matplotlib.pyplot as plt
from olps.strategies.strategy import Strategy
from abc import ABC, abstractmethod

class Visualizer(ABC):
    """
    Abstract class for visualizing portfolios over time
    """
    @staticmethod
    @abstractmethod
    def visualize(outputfile: str, strategies: list[Strategy]):
        """
        Plots the strategies to the output file in a single graph
        """
        pass
