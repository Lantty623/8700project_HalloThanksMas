# CPSC 8700 Project - HalloThanksMas

**HalloThanksMas** is a holiday-themed catching game built in Python. The game consists of three levels, each representing a different holiday theme: Halloween, Thanksgiving, and Christmas. Each level has its own objective, point system, and fun graphics. Players can enjoy the game while learning to manage objectives, dodge obstacles, and score high!

## Overview

This game is part of the CPSC 8700 Software Design course project. Students were given the freedom to select their teammates and decide the game concept, programming language, and interface. The inspiration comes from the holiday season, where stores often sell combined decorations for Halloween, Thanksgiving, and Christmas—referred to as *HalloThanksMas*. Hence, the game’s name reflects this theme.

## Game Details

- **Levels**: The game has three levels:
  - **Level 1**: Trick-or-Treating - Collect the falling candy into your pumpkin basket to gain points, but watch out! Catching ghosts will reduce the score. 
  - **Level 2**: Harvesting Festival - Gather food items to complete different Thanksgiving dinner combination set to earn different points, but watch out! The turkey might fly somewhere else.
  - **Level 3**: Santa's Present - Catch the present that is rain from the sky, but watch out! Snow will slowly build up from the ground as time pass. Please dodge those snowball and snowman. 

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
- **Python**: Version 3.8 or higher
- **Pygame**: For game development and graphics
  - Install using:
    ```bash
    pip install pygame
    ```
- **Pillow**: For image handling
  - Install using:
    ```bash
    pip install pillow
    ```
- **Tkinter**: Used for graphical user interface elements
  - On Linux, you may need to install it using:
    ```bash
    sudo apt-get install python3-tk
    ```
- **qtawesome**: For icons and styling.
  - Install using:
    ```bash
    pip install qtawesome
    ```
- **PyQt5** (or **PySide6**): Required for `qtpy` to provide Qt bindings.
  - Install using:
    ```bash
    pip install PyQt5
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