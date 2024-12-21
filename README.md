# Bogalho Room Creator

Bogalho Room Creator is a Python-based tool designed to streamline the process of designing and managing game rooms for GameMaker projects. It enables developers to work efficiently by leveraging a drag-and-drop interface and processing game-related files directly from the GameMaker project.

**Note**: This project is a work in progress. Contributions and feedback are welcome to help improve its functionality and usability.

## Features

- **Room Design Automation**: Process GameMaker room files to generate GML code automatically.
- **Game Project Integration**: Supports reading and processing objects directly from GameMaker project folders.
- **Customizable Workflow**: Adaptable to your game's specific room size and grid configurations.

## Getting Started

### Prerequisites

Ensure you have the following installed on your system:

- Python 3.7 or later
- GameMaker (for project integration)

### Installation

1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/FranciscoRoqu/Bogalho-Room-Creator.git
   ```

2. Navigate to the project directory:
   ```bash
   cd Bogalho-Room-Creator
   ```

### Usage

1. Place your GameMaker project folder inside the `gamefiles` directory.
2. Run the main script:
   ```bash
   python main.py
   ```
3. Follow the prompts to process room files or manage objects.

## Project Structure

```
Bogalho-Room-Creator/
├── .gitattributes         # Repository attributes
├── gamefiles/             # Placeholder for GameMaker project files
├── main.py                # Main script to run the application
└── .git/                  # Git version control metadata
```

## Configuration

The default room size is 1366x768 pixels, with a 16x16 pixel grid. You can adjust these parameters in the script if necessary.

## Requirements

- `os`: Standard library module for operating system interactions.
- `tkinter`: Standard library module for GUI creation.
- `pyautogui`: Used for retrieving the current mouse position programmatically. (Will be added later)

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m 'Add some feature'
   ```
4. Push to the branch:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request.

## Acknowledgments

Special thanks to the GameMaker community for inspiring this tool!
