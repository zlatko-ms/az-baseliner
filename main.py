#!/usr/bin/python3

import logging
from logging import Logger
from azbaseliner.calculator import Calculator

logging.basicConfig(format="[%(asctime)s] [%(levelname)s] %(message)s", level=logging.INFO)
logger: Logger = logging.getLogger("main")

logger.info("starting processing ")
c: Calculator = Calculator()
logger.info("helloer just said that 2+2=" + str(c.add(2, 2)))
logger.info("finished processing ")
