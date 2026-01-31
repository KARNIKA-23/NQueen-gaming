# N-Queens 2.5D Visualizer

An interactive, 2.5D isometric visualization of the classic N-Queens problem, built with Python and Pygame. This project features a beautiful UI, animated elements, and an AI solver to demonstrate the backtracking algorithm.

## 🌟 Features

- **2.5D Isometric Graphics:** A visually appealing board with depth and perspective.
- **Interactive Gameplay:** Manually place and remove queens to try and solve the puzzle yourself.
- **AI Solver:** Watch the backtracking algorithm solve the puzzle step-by-step in real-time.
- **Dynamic Board Size:** Support for board sizes ranging from 4x4 to 12x12.
- **360° Rotation:** Rotate the board using the keyboard or by dragging with the mouse to view it from any angle.
- **Visual Effects:**
  - Floating animations for queens.
  - Dynamic lighting and shadows.
  - Attack indicators (red dots) for invalid moves.
  - "Interface Colour Waves" mouse trail effect.
  - Balloon celebration animation upon winning.
- **Web Version:** Includes a Streamlit-based web interface (`gaming.py`).

## 🛠️ Installation

Ensure you have Python installed (Python 3.10+ recommended).

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/n-queens-2.5d.git
   cd n-queens-2.5d
   ```

2. **Install dependencies:**
   ```bash
   pip install pygame streamlit
   ```

## 🚀 Usage

### Desktop Application (Pygame)
Run the main visualizer with rich graphics and animations:
```bash
python main.py
```

### Web Application (Streamlit)
Run the lightweight web version:
```bash
streamlit run gaming.py
```

## 🎮 Controls

| Action | Input |
|--------|-------|
| **Place / Remove Queen** | Left Click on a tile |
| **Rotate Board** | Drag Mouse (Left Button) or Left/Right Arrow Keys |
| **Reset Board** | Click "Reset" Button |
| **Start AI Solver** | Click "Solve (AI)" Button |
| **Change Board Size** | Click "+" or "-" Buttons |

## 🧠 The N-Queens Problem

The N-Queens puzzle is the problem of placing N chess queens on an N×N chessboard so that no two queens threaten each other. Thus, a solution requires that no two queens share the same row, column, or diagonal.

## 📄 License

This project is open source and available under the MIT License.

