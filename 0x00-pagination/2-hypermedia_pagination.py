#!/usr/bin/env python3
"""
Module for paginating a dataset of popular baby names.

This module defines a Server class that reads a CSV file containing
data about baby names and provides pagination functionality to fetch
data in a more manageable way.
"""

import csv
import math
from typing import List


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


class Server:
    """Server class to paginate a database of popular baby names."""
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset."""
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]  # Skip the header row

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """Get a page of the dataset.

        Parameters:
        page (int): The page number (1-indexed).
        page_size (int): The number of items per page.

        Returns:
        List[List]: A list of rows for the specified page.
        """
        # Validate input
        assert isinstance(page, int) and page > 0, \
            "Page must be a positive integer"
        assert isinstance(page_size, int) and page_size > 0, \
            "Page size must be a positive integer"

        # Get the dataset
        dataset = self.dataset()

        # Calculate the indexes for pagination
        start_index, end_index = index_range(page, page_size)

        # Return the appropriate slice, or an empty list if out of bounds
        if start_index >= len(dataset):
            return []
        return dataset[start_index:end_index]

    def get_hyper(self, page: int = 1, page_size: int = 10) -> dict:
        """Get a hyper pagination dictionary.

        Parameters:
        page (int): The page number (1-indexed).
        page_size (int): The number of items per page.

        Returns:
        dict: A dictionary containing pagination details.
        """
        # Get the data for the current page
        data = self.get_page(page, page_size)

        # Calculate total number of pages
        total_items = len(self.dataset())
        total_pages = math.ceil(total_items / page_size)

        # Calculate next and previous page
        next_page = page + 1 if page < total_pages else None
        prev_page = page - 1 if page > 1 else None

        # Prepare and return the hyper pagination details
        return {
            'page_size': len(data),
            'page': page,
            'data': data,
            'next_page': next_page,
            'prev_page': prev_page,
            'total_pages': total_pages
        }
