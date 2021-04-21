from .datasource import DataSource
import numpy as np
import math


class CorrelationDrivenDataSource(DataSource):

    window = 2
    rho = 0.2 
    similarity_set = None
    similarity_set_size = 0
    # modifying the constructors to include the window size
    def __init__(self, initial_prices: np.array, window):
        """
        Initialize the data source with the price of all assets at the beginning of strategy execution.
        """
        self.prices = initial_prices
        self.price_relatives = None
        self.similarity_set = None
        self.window = window

    def sample_selection(self) -> None:

        sample_set = None
        len = self.price_relatives.shape[1]
        t = len - 1
        if len > self.window + 1:
        # initialize our final window
            final_window = np.array(self.price_relatives[:, t - self.window + 1]).T
            for i in range(t - self.window + 2, len):
                prv = np.array(self.price_relatives[:, i]).T
                final_window = np.column_stack((final_window, prv))

            for i in range(self.window + 1, len):
            # create window matrix for the current initial index
                curr_window = np.array(self.price_relatives[:, i - self.window]).T
                for j in range(i - self.window + 1, i):
                    prv = np.array(self.price_relatives[:, j]).T
                    curr_window = np.column_stack((curr_window, prv))

            # now compute correlation coefficient using CORN Formula
            vectorized_curr_window = np.empty(0)
            vectorized_final_window = np.empty(0)

            for item in curr_window:
                vectorized_curr_window = np.append(vectorized_curr_window, item)
            for item in final_window:
                vectorized_final_window = np.append(vectorized_final_window, item)

            cov = sum((vectorized_curr_window - np.mean(vectorized_curr_window)) * (vectorized_final_window - np.mean(vectorized_final_window)))
            sx = np.sqrt(sum((vectorized_curr_window - np.mean(vectorized_curr_window)) ** 2.0))
            sy = np.sqrt(sum((vectorized_final_window - np.mean(vectorized_final_window)) ** 2.0))
            corr = cov / (sx * sy)

            # Compare against rho
            if corr >= self.rho:
                self.similarity_set_size += 1
                if sample_set is None:
                    sample_set = [i]
                else:
                    sample_set = np.append(sample_set, i)

        self.similarity_set = sample_set