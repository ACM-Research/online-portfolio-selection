from .datasource import DataSource
import numpy as np
import math


class CorrelationDrivenDataSource(DataSource):

    window : int
    rho : float 
    similarity_set : np.array
    similarity_set_size : int
    # modifying the constructors to include the window size
    def __init__(self, initial_prices: np.array, window = 2, rho = 0.2):
        """
        Initialize the data source with the price of all assets at the beginning of strategy execution.
        """
        super().__init__(initial_prices)
        self.similarity_set = None
        self.similarity_set_size = 0
        self.window = window
        self.rho = rho


    def sample_selection(self) -> None:

        self.similarity_set_size = 0

        sample_set = None
        length = self.price_relatives.T.shape[0]
        t = length - 1
        if length > self.window + 1:
        # initialize our final window
            if (self.price_relatives.ndim == 1):

                final_window = np.array(self.price_relatives[t - self.window + 1]).T
                for i in range(t - self.window + 2, length):
                    prv = np.array(self.price_relatives[i]).T
                    final_window = np.column_stack((final_window, prv))
                for i in range(self.window + 1, length):
                # create window matrix for the current initial index
                    curr_window = np.array(self.price_relatives[i - self.window]).T
                    for j in range(i - self.window + 1, i):
                        prv = np.array(self.price_relatives[j]).T
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

            else:
                
                final_window = np.array(self.price_relatives[:, t - self.window + 1]).T
                for i in range(t - self.window + 2, length):
                    prv = np.array(self.price_relatives[:, i]).T
                    final_window = np.column_stack((final_window, prv))
                for i in range(self.window + 1, length):
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