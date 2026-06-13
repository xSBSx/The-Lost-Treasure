# 🗝️ The Lost Treasure

A modern, fully playable Python text-adventure game featuring a custom graphical interface, live inventory tracking, and a dynamic real-time area map.

Built entirely in Python, this project reimagines classic interactive fiction by replacing the standard terminal with a stylized, dark-fantasy dashboard built on `customtkinter`. 

## ✨ Features

* **Custom Graphical UI:** A beautiful, multi-panel dashboard featuring parchment-colored text, gold accents, and deep cavernous backgrounds.
* **Live 'Satchel' Inventory:** No need to type `inventory`. Your items update visually in the left sidebar the moment you pick them up or drop them.
* **Dynamic Mini-Map:** A visual map tracks your location, highlights locked doors (🔒), and shows available exits in real-time.
* **Interactive Codex:** A right-hand scanner that automatically reads the room you are in, providing lore and hints for items on the floor and in your pockets.
* **Environmental Hazards:** Survive the pitch-black tunnels by finding a way to light your torch, or face the Grue!
* **Instant Reset:** A built-in refresh button to wipe the board and restart your adventure without closing the app.

## 🚀 Installation & Setup

To play the game on your local machine, you will need Python installed.

1. **Download the Game:**
   Download the `game.py` file directly, or clone this repository to your computer:
   ```bash
   git clone [https://github.com/YourUsername/The-Lost-Treasure.git](https://github.com/YourUsername/The-Lost-Treasure.git)
2. Install the UI Library:
  This game uses CustomTkinter for its graphical interface. Install it via your terminal/command prompt:
  pip install customtkinter
3. Run the Game:
  Navigate to the folder where you saved the game and run:
  python game.py

🎮 How to Play
Type your commands into the prompt (>) at the bottom of the screen and press Enter.

Available Commands:

go [direction] — Move (directions: north, south, east, west)

look — Describe your current location

take [item] — Pick up an item from the ground

drop [item] — Drop an item from your satchel

light torch — Light an unlit torch (requires flint)

examine [item] — Inspect an item more closely

quit — Exit the game safely

Shortcuts:

Press F1 or click the ? button at any time to pull up the command list.

Click RESTART to reset the board to the very beginning.

📂 Project Structure
Everything you need to run the game is cleanly packed into a single, highly-organized script:

game.py — Contains the world map data, the core logic engine, the command parser, and the CustomTkinter UI framework.

Built with Python and CustomTkinter.
