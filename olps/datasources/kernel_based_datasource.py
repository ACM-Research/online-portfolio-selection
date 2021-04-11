from .datasource import DataSource
import numpy as np

class Kernel_Based_DataSource(DataSource):
    # size of the windows
    window 
    # A 1D array of the index set for which the market windows are similar to the final window via Euclidean distance 
    sample_selection:np.array

    # modifying the constructors to include the window size
    def __init__(self, initial_prices: np.array):
        """
        Initialize the data source with the price of all assets at the beginning of strategy execution.
        """
        self.prices = initial_prices
        self.price_relatives = None
        window = 2
        self.sample_selection = None
     def __init__(self, initial_prices: np.array, window : int):
        """
        Initialize the data source with the price of all assets at the beginning of strategy execution.
        """
        self.prices = initial_prices
        self.price_relatives = None
        self.window = window
        self.sample_selection = None
    
    def sample_selection(self)->None:
        len = price_relatives.shape[1]
          t = len - 1
        if len > window + 1:
            # initialize our final window 
            final_window = np.array(price_relatives[:, t-window+1]).T
             for i in range(t - window + 2, len):
                 prv = np.array(price_relatives[:, i]).T
                final_window = np.column_stack((final_window, prv))
            for i in range(window + 1, len):
                # create window matrix for the current i
                 print("In loop setting up current window")
                 curr_window = np.array(price_relatives[:, i - window]).T
                 for j in range(i - window + 1, i):
                    prv = np.array(price_relatives[:, j]).T
                    curr_window = np.column_stack((curr_window, prv))
                # now compare that window matrix to the final window matrix via euclidean distance
                distance = ((final_window - curr_window) ** 2).sum()
                distance = math.sqrt(distance)
                # chose a random parameter for now, discuss at build night
                if distance >= .5:
                    continue
                if sample_set is None:
                    sample_set = [i]
                else:
                    sample_set = np.append(sample_set, i)

    


    