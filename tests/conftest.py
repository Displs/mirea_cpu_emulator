import pytest
from loguru import logger

from domain.cpu import CPU
from domain.memory import Memory


@pytest.fixture
def memory():
    return Memory(1024)


@pytest.fixture
def cpu(memory):
    logger.info('CPU сконфигурирован')
    return CPU(memory)
