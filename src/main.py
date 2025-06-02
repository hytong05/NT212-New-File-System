import sys
import os

# Add the src directory to the Python path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ui.cli import CLI

def main():
    cli = CLI()
    cli.start()

if __name__ == "__main__":
    main()