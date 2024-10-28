#!/usr/bin/env python3
"""
Module for calculating index ranges for pagination.

This module contains a function `index_range` that computes the start
and end indexes for a specific page in a paginated data structure.
"""


def index_range(page, page_size):
    """
    Returns a tuple of size two containing a start index and an end index
    corresponding to the range of indexes to return in a list for the
    given pagination parameters.

    Parameters:
    page (int): The page number (1-indexed).
    page_size (int): The number of items per page.

    Returns:
    tuple: A tuple containing the start index and end index.
    """
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    return (start_index, end_index)
