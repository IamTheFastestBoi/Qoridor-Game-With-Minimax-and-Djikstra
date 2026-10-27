Quoridor AI Engine

A playable Quoridor game built with Python and Pygame, featuring a custom AI opponent. The AI uses the Minimax algorithm with Alpha-Beta pruning and Dijkstra's algorithm to calculate paths and strategically place walls.

Features

Interactive GUI: Built with Pygame, featuring a modern dark theme and intuitive visual feedback. ( THE PYGAME GUI WAS BUILT BY AI NOT ME )

Smart AI: The PC opponent doesn't just walk; it uses path delta calculations to strategically trap the player and funnel them into longer routes. 

Alpha-Beta Pruning: Optimized decision-making tree so the AI thinks and reacts efficiently.

Legal Move Validation: The engine prevents players (and the AI) from completely blocking the path to the goal, adhering strictly to Quoridor rules.

Requirements

To run this game, you need Python installed on your system along with the Pygame library.

Install Python (3.x recommended).

Install Pygame by running this command in your terminal or command prompt:

pip install pygame


How to Run

Download or clone this repository.

Open your terminal or command prompt.

Navigate to the folder containing the game files.

Run the main script:

python main_qoridor.py


How to Play

Your goal is to reach the opposite end of the board before the PC does. You can either move your pawn or place a wall to block your opponent.

Controls

M - Switch to Move Mode. Click on an adjacent green square to move your pawn.

O - Switch to Obstacle (Wall) Mode. Click on a small intersection (anchor) between squares to select it.

H - Place a Horizontal wall at your selected anchor.

V - Place a Vertical wall at your selected anchor.

ESC - Deselect your current anchor.

Note: You start with 10 walls. Once you run out, you can only move your pawn.

Under the Hood

The AI engine evaluates board states by simulating future moves up to a certain depth. It calculates the shortest paths for both itself and the player using a custom Dijkstra implementation. The evaluation function actively rewards the AI for finding "traps"—wall placements that force the player into exponentially longer routes rather than just simple blocks.
