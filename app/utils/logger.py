from sys import stderr

from loguru import logger

logger.remove()
logger.add(sink=stderr, format='<white>{time:DD.MM.YYYY HH:mm:ss}</white>'
                               ' | <level>{level: <8}</level>'
                               ' | <cyan>{line}</cyan>'
                               ' - <b><m>{message}</m></b>'
                               ' - <w>{extra}</w>')
logger.add(sink="logs.log", format='{time:DD.MM.YYYY HH:mm:ss}'
                                   ' | {level: <8}'
                                   ' | {line}'
                                   ' - {message}'
                                   ' - {extra}')
