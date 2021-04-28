from .datasource import DataSource
import numpy as np
import math


class KernelBasedDataSource(DataSource):
    # A 1D array of the index set for which the market windows are similar to the final window via Euclidean distance 
    window = 1 
    similarity_set: np.array
    threshold: int
    # modifying the constructors to include the window size
    def __init__(self, initial_prices: np.array, window: int, threshold=0.5):
        """
        Initialize the data source with the price of all assets at the beginning of strategy execution.
        """
        self.prices = initial_prices
        self.price_relatives = None
        self.similarity_set = None
        self.window = window
        self.threshold = threshold

    def sample_selection(self) -> None:
        self.similarity_set = None
        if self.prices.shape[1] < self.window:
            return
        similarity_set = np.array
        similarity_set = None
        length = self.price_relatives.T.shape[0]
        t = length - 1
        if length > self.window + 1:
            # initialize our final window 
            if (self.price_relatives.ndim == 1):
                final_window = np.array(self.price_relatives[t - self.window + 1]).T
                for i in range(t - self.window + 2, length):
                    prv = np.array(self.price_relatives[i]).T
                    final_window = np.column_stack((final_window, prv))
                for i in range(self.window, length):
                    # create window matrix for the current i
                    curr_window = np.array(self.price_relatives[i - self.window]).T
                    for j in range(i - self.window + 1, i):
                        prv = np.array(self.price_relatives[j]).T
                        curr_window = np.column_stack((curr_window, prv))
                    # now compare that window matrix to the final window matrix via euclidean distance
                    distance = ((final_window - curr_window) ** 2).sum()
                    distance = math.sqrt(distance)
                    if distance < self.threshold:
                        if similarity_set is None:
                            similarity_set = np.array(i)
                        else:
                            similarity_set = np.column_stack((similarity_set, [i]))
            else:
                final_window = np.array(self.price_relatives[:, t - self.window + 1]).T
                for i in range(t - self.window + 2, length):
                    prv = np.array(self.price_relatives[:, i]).T
                    final_window = np.column_stack((final_window, prv))
                for i in range(self.window, length):
                    # create window matrix for the current i
                    curr_window = np.array(self.price_relatives[:, i - self.window]).T
                    for j in range(i - self.window + 1, i):
                        prv = np.array(self.price_relatives[:, j]).T
                        curr_window = np.column_stack((curr_window, prv))
                    # now compare that window matrix to the final window matrix via euclidean distance
                    distance = ((final_window - curr_window) ** 2).sum()
                    distance = math.sqrt(distance)
                    if distance < self.threshold:
                        if similarity_set is None:
                            similarity_set = np.array(i)
                        else:
                            similarity_set = np.column_stack((similarity_set, [i]))
            self.similarity_set = similarity_set