"""
    gRPCAlchemy
    ~~~~~

    The Python micro framework for building gPRC application.
"""

__author__ = """GuangTian Li"""
__email__ = 'guangtian_li@qq.com'
__version__ = '0.2.4'

from .server import Server
from .blueprint import Blueprint, Context
from .globals import current_app
