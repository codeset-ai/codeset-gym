"""Test result collectors for different programming languages."""

from .factory import TestResultCollectorFactory
from .base import TestResultCollector

__all__ = [
    "TestResultCollectorFactory",
    "TestResultCollector",
]