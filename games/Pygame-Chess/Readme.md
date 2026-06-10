# ♟️ AI Chess Game

A desktop Chess game built with **Python**, **Pygame**, **python-chess**, and **Stockfish AI**.

## Features

* Interactive chessboard UI
* Click-to-select piece movement
* Legal move validation
* Visual highlighting for selected pieces and legal moves
* AI opponent powered by Stockfish
* Checkmate detection
* Stalemate detection
* Winner display screen
* Clean object-oriented project structure

## Tech Stack

* Python 3.x
* Pygame
* python-chess
* Stockfish Engine

## Project Structure

```
.
├── ai.py
├── board.py
├── input_handler.py
├── loader.py
├── main.py
├── renderer.py
├── assets/
│   ├── board/
│   └── pieces/
├── requirements.txt
└── README.md
```
###  Create a virtual environment (Optional)

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` is unavailable:

```bash
pip install pygame python-chess stockfish
```

## Installing Stockfish

### macOS

```bash
brew install stockfish
```

### Ubuntu / Debian

```bash
sudo apt update
sudo apt install stockfish
```

### Windows

1. Download Stockfish.
2. Add the executable to your system PATH.

The project automatically searches for the Stockfish executable installed on your system.

## Running the Project

```bash
python main.py
```

## How to Play

* Click on a piece to select it.
* Legal moves are highlighted.
* Click a highlighted destination square to move.
* The AI automatically responds after your move.
* The game ends when a player is checkmated or a draw condition is reached.

## Requirements

* Python 3.9+
* Stockfish installed and accessible from PATH

## Future Improvements

* Pawn promotion UI
* Castling animations
* Move history panel
* Undo/Redo moves
* Multiple AI difficulty levels
* Game timer
* PGN export/import
* Sound effects

## Contributing

Contributions are welcome.

1. Fork the repository.
2. Create a new branch.
3. Commit your changes.
4. Open a Pull Request.

## License

This project is open source and available under the MIT License.
