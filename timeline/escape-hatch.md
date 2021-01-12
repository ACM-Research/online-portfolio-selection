# Escape Hatch

Here are potential problems with the project, as well as potential solutions.

# Problem 1: There are too many update rules to study

## Solution

Since we study 3 different types of strategies, there's two ways we can reduce the update rules.

### Option A: Study a fewer number of strategy types

This is a nuclear option—the value of the project is derived by learning most the different types of strategies described in the original paper.

Pattern-matching strategies in particular may be harder to understand, so that's the first thing I'd cut if time is running low.

### Option B: Reduce the number of update rules studied/implemented

This is a slightly better option, but still not ideal. Since each type of strategy has many different variants (many of which are very similar to each other), it may be feasible to not implement a few of them.

# Problem 2: Backtesting is hard to implement

## Solution

While it is more fun to implement a backtester, there's also various open-source projects that can be leveraged to rescue the project:

- [https://www.turingtrader.org/](https://www.turingtrader.org/)
- [https://github.com/mementum/backtrader](https://github.com/mementum/backtrader)

This should remove the focus on building reporting infrastructure and reorient focus on the trading strategies.

# Problem 3: All the strategies perform equally well/badly on the chosen portfolio

## Solution

First of all, *oof*. But there is still a project to be salvaged from this. Try a different portfolio. Some combinations of things to try:

- A portfolio of mostly stable stocks
- A portfolio of mostly stable stocks, with some stocks increasing wildly
- A portfolio of low-value (penny) stocks
- A portfolio of stocks that dipped in value, then recovered
- A portfolio of stocks that dipped in value and stayed there
- and any combination thereof....