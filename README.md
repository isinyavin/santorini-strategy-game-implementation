# Tower Building Stategy Game 

This repository contains an implementation of the board game **Santorini**. My implementation provides three different types of opponents based on difficulty.

Santorini is a strategy-based board game where players compete to be the first to build a tower and place their worker on the third level. The game is played on a 5x5 board, and each player controls two workers. On each turn, a player moves one of their workers and then builds on an adjacent square. The objective is to reach the third level of a tower before your opponent does.

For detailed rules and instructions on how to play the game, you can refer to the official Santorini rules [here](https://roxley.com/santorini).

![Santorini Gameplay](main_demo.gif)

## How to Play Using the GUI

This implementation includes a GUI that lets you play against three different levels of AI opponents: Random, Heuristic, and ML. The GUI can be launched using the following commands:

### 1. **Play Against a Random Opponent (Beginner)**

Launch the game with a random AI opponent:
```bash
python3 gui.py human random
```
In this mode, your opponent makes random moves with no strategy.

### 2. Play Against a Heuristic Opponent (Intermediate)

Launch the game with a heuristic AI opponent:

```bash
python3 gui.py human heuristic
```

In this mode, the AI uses a heuristic strategy to optimize its moves. The heuristic evaluates:

- **Height Advantage**: Prioritizes building and moving to higher levels.
- **Center Control**: Attempts to control the center of the board.
- **Worker Proximity**: Keeps workers close to prevent the opponent from blocking key moves.

These factors are weighted for each available move and optimal move is played. 

### 3. Play Against a Machine Learning Opponent (Advanced)

![Santorini Gameplay](ml_demo.gif)

Launch the game with a machine learning opponent:

```bash
python3 gui.py human ml
```

In every turn, the chosen move is determined by multiplying the heuristic score by the machine learning output. This allows the heuristic score to dominate in the early stages, where basic principles like height advantage and worker positioning are key. As the game progresses and becomes more strategically complex, the model output (which will yield higher scores) takes precedence.

### Explanation of the ML Model
The ML opponent uses a convolutional neural network  that processes board states represented as a 5x5 grid with separate channels for height and worker positions. The model was trained using simulated games, where board states were labeled based on whether they led to a victory. The CNN was fine-tuned using a combination of heuristic rules and reinforcement learning techniques.

The ML strategy combines heuristic evaluation with deep learning predictions. Early moves are guided by basic principles encapsulated in the heuristic score, while later moves are informed by the model, which was trained on 3.5 million simulated board states.