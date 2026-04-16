# JSNAKE

A clean, arcade-style Snake game for the terminal. Built with Python and the Textual framework, it features a level-based progression system and balanced movement speed.

## Installation

### PowerShell
```bash
py -m pip install --upgrade pip
py -m pip install jsnake
jsnake
```

If PowerShell says `jsnake` is not recognized, close and reopen the terminal once.
You can also launch the game directly with:

```bash
py -m jsnake
```

### Standard Installation
```bash
pip install jsnake
jsnake
```

### Optional Cinematic Installer
If you want the animated installer experience, use the command that matches your shell.

PowerShell:
```powershell
irm https://raw.githubusercontent.com/Jithi/jsnake/main/setup_jsnake.py | py -
```

Bash:
```bash
curl -sSL https://raw.githubusercontent.com/Jithi/jsnake/main/setup_jsnake.py | python
```

## How to Play

Run the game from your terminal after installation:

```bash
jsnake
```

### Controls

- W / A / S / D: Move the snake
- P: Pause or resume the game
- R: Restart the current session
- Q: Quit the game

## Development

If you want to contribute or modify the game, you can install the developer dependencies:

```bash
pip install -e ".[dev]"
```

The core game logic is separated into its own engine, making it easy to test or extend.

## License

This project is licensed under the MIT License.
