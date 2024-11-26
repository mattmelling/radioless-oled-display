import os
import logging
from .cli import main

logging.basicConfig(level=os.environ.get('LOG_LEVEL', 'INFO'))

if __name__ == '__main__':
    main()
