"""
H. perforatum Network Toxicology Analysis Package

A network-proximity pipeline that separates effect size from statistical
evidence under target-count asymmetry, applied to H. perforatum constituents
(Hyperforin, Quercetin) and the drug-induced liver injury (DILI) module.
"""

__version__ = "2.1.0"
__author__ = "Antony Bevan"

from .core import network, proximity, permutation
from .utils import data_loader, validators
from .analysis import rwr, shortest_path

__all__ = [
    "network",
    "proximity", 
    "permutation",
    "data_loader",
    "validators",
    "rwr",
    "shortest_path",
]
