# coding=utf-8
from __future__ import absolute_import
import numpy as np

def random_superposition(dim):
    u"""
    Args:
        dim: Specified size returns a 2^dim length array.
    Returns:
        Normalized random array.
    """
    state_vector = np.random.standard_normal(dim).astype(complex)
    state_vector += 1j * np.random.normal(dim)
    state_vector /= np.linalg.norm(state_vector)
    return state_vector
