from .datasource import DataSource
import numpy as np

class Kernel_Based_DataSource(DataSource):
    window 
    # modifying the constructors to include the window size
    def __init__(self, initial_prices: np.array):
        """
        Initialize the data source with the price of all assets at the beginning of strategy execution.
        """
        self.prices = initial_prices
        self.price_relatives = None
        window = 2
     def __init__(self, initial_prices: np.array, window : int):
        """
        Initialize the data source with the price of all assets at the beginning of strategy execution.
        """
        self.prices = initial_prices
        self.price_relatives = None
        self.window = window
    