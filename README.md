# CPSC 8700 Project - HalloThanksMas

**HalloThanksMas** is a holiday-themed catching game built in Python. The game consists of three levels, each representing a different holiday theme: Halloween, Thanksgiving, and Christmas. Each level features a unique design for the catching container, items to catch, and increasing levels of difficulty.

## Overview

This game is part of the CPSC 8700 Software Design course project. Students were given the freedom to select their teammates and decide the game concept, programming language, and interface. The inspiration comes from the holiday season, where stores often sell combined decorations for Halloween, Thanksgiving, and Christmas—referred to as *HalloThanksMas*. Hence, the game’s name reflects this theme.

## Game Details

- **Levels**: The game has three levels:
  - **Level 1**: Halloween-themed - Features a spooky background and requires the player to catch candy for points, but watch out! Catching ghosts will reduce the score. Sound effects for item catches and themed background music add to the Halloween atmosphere.
  - **Level 2**: Thanksgiving-themed - Adds a unique combo-based scoring system where players need to collect a set of themed items (turkey, pie, mash). Each completed set contributes to the score based on item-specific points (e.g., turkey: 100, pie: 50, mash: 150). Players receive sound feedback for item catches and completed sets, alongside
  - **Level 3**: Christmas-themed - To be continued...
- Each level includes:
  - A uniquely designed catching container
  - Themed items to catch
  - Increasing levels of difficulty in catching items

## Project Requirements

The objective of the project is to design a simple game that combines all three holiday themes. The requirements include:

- Using **Python** or **C++** as the programming language
- Implementing at least **two design patterns** chosen by the team
- Creating a **simple interface** for gameplay
- Developing a **single-player** experience where:
  - The player can accumulate points across levels
  - The player has the option to **save and continue** the game
  - A **scoreboard** maintains player scores

### Dependencies

To run the **HalloThanksMas Game**, you need to have the following dependencies installed on your system:

**Required:**
- **Python**: Version 3.7 or higher
- **Pygame**: For game development and graphics
  - Install using:
    ```bash
    pip install pygame
    ```
- **Tkinter**: Used for graphical user interface elements
  - On Linux, you may need to install it using:
    ```bash
    sudo apt-get install python3-tk
    ```

Ensure these dependencies are correctly installed before running the game.

## How to Play

1. Clone the repository:
   ```bash
   git clone https://github.com/Lantty623/8700project_HalloThanksMas.git
   ```
2. Navigate to the project directory:
    ```bash
    cd 8700project_HalloThanksMas
    ```
3. Run the game:
    ```bash
    python game.py
    ```

## Acknowledgments

We would like to extend our gratitude to the following sources for providing assets that made the HalloThanksMas game possible:

- **Images and Art**: 
  - Many of the images and design elements in this project were sourced from [Google Images](https://images.google.com/) and [Canva](https://www.canva.com/). 
  - These assets helped bring the holiday themes to life across all levels of the game.

- **Background Music**: 
  - The immersive background music in each level was composed with the help of [AIVA](https://www.aiva.ai/), an AI music composition platform that added a festive atmosphere to the gameplay.

- **Sound Effects**: 
  - Sound effects, which enhance the player’s experience when interacting with items in the game, were sourced from [Zapsplat](https://www.zapsplat.com/). These sounds include effects for catching items and completing sets.

Please note that all assets were used in compliance with the respective terms and licenses of each source.


## License
This project is licensed under the MIT License. See the LICENSE file for more details.