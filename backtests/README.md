# Backtesting

1. Write a main method with the necessary code:

```python
info: TradingMarketStrategyInfo = {
    # strategies array: pass in initialized strategies!
    'strategies': [BAHStrategy(6)],
    # datasource factory: initialize datasources with those intial prices inside the array!
    'datasource_factory': lambda initial_prices: [DataSource(initial_prices)],
    # frequencies: use the olps.util module to define frequencies!
    'frequencies': [minute(5)],
}
# Define a data directory
data_dir = Path('.') / 'data'
# Define the path. You should change this depending on what portfolio you're backtesting.
path = data_dir / 'mar29test' / 'merged' / 'AAPL-BBY-DIS-TSLA-TWTR-UBER.csv'
# Create a market object with the info and path.
market = TradingMarket(info, path)
# Main loop: run through all the ticks
while market.can_advance():
    market.advance()
# Save the return
backtest_name = 'mar29test' # make sure to change this for every new backtest!
for strategy in market.strategies:
    name = type(strategy).__name__
    np.savetxt(f'{backtest_name}-wealth-{name}.txt', strategy.cumulative_wealth)
```

If you need a more comprehensive example, see `mar29test.py`.

2. Modify the strategies you're running via the `strategies` array in the `TradingMarketStrategyInfo` dict. Make sure you give them a DataSource and a frequency as defined above.

3. Provide them with a merged source of ticks via the `path` variable. To merge ticks, see below.

4. Run the code and collect the cumulative wealth from the `.txt` files to graph over time. To run the code, remain in the root directory of this repo and run `python3 -m backtests.mar29test`, with the last part being the name of your backtest module in the `backtests/` folder.

5. Done! Make sure you commit your backtest results in a folder called `results` and your backtest file in `backtests`.

---

# Generating Merged Tick Files

1. Create a folder in `data/` with a unique name. Dump all the tick CSVs in there. Note that the tick CSVs must use _local time_, not UTC.

2. Run the tick merger by running `python3 -m olps.data_preprocessor ./data/dir-name`, where `dir-name` is the name of the folder you just created.

3. The merged tick file CSV (usable by the backtester) will be in `./data/dir-name/merged`.
