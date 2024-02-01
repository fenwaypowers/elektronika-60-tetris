import os
import configparser
import sys
import logging
from dataclasses import dataclass
from typing import Dict

@dataclass
class Controls:
    move_left: int
    move_right: int
    move_down: int
    hard_drop: int
    rotate_clockwise: int
    rotate_anti_clockwise: int
    quit: int

def load_controls(config_path: os.PathLike) -> Controls:
    '''
    Load and validate the controls configuration. Exits the program if the configuration is invalid.
    '''
    logging.basicConfig(level=logging.ERROR)

    try:
        cfg = configparser.ConfigParser()
        cfg.read(config_path)
    except Exception as e:
        logging.error(f"Failed to load controls config file from {config_path}: {e}")
        sys.exit(1)

    try:
        # Convert the key names from the ini file to their curses equivalent or ord() value for characters
        controls = Controls(
            move_left=get_key_code(cfg.get('controls', 'move_left')),
            move_right=get_key_code(cfg.get('controls', 'move_right')),
            move_down=get_key_code(cfg.get('controls', 'move_down')),
            hard_drop=get_key_code(cfg.get('controls', 'hard_drop')),
            rotate_clockwise=get_key_code(cfg.get('controls', 'rotate_clockwise')),
            rotate_anti_clockwise=get_key_code(cfg.get('controls', 'rotate_anti_clockwise')),
            quit=get_key_code(cfg.get('controls', 'quit'))
        )
    except Exception as e:
        logging.error(f"Error in controls config file {config_path}: {e}")
        sys.exit(1)

    return controls

def get_key_code(key_name: str) -> int:
    """
    Convert a key name to its curses equivalent or ASCII ordinal value without initializing curses.
    """
    # Predefined mapping of common curses key names to their values
    curses_keys = {
        "KEY_DOWN": 258,
        "KEY_UP": 259,
        "KEY_LEFT": 260,
        "KEY_RIGHT": 261,
        "KEY_ENTER": 10,
        "SPACE": 32,
    }

    # Check if the key name is a special curses key
    if key_name in curses_keys:
        return curses_keys[key_name]
    
    # Otherwise, return the ASCII ordinal value
    return ord(key_name)

# Example usage
if __name__ == '__main__':
    config_path = 'settings.ini'  # The path to your controls configuration file
    controls = load_controls(config_path)
    print(controls)

