import logging
import os
import sys
from pathlib import Path

# Add the project root to sys.path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# Import CLI app
from src.ui.cli import app

if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    # Run the CLI app
    app() 