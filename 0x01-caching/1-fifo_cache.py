#!/usr/bin/python3
""" FIFOCache module
"""
from collections import deque
from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """ FIFOCache provides a caching system using FIFO algorithm """

    def __init__(self):
        """ Initialize the cache and the order of keys """
        super().__init__()
        self.order = deque()

    def put(self, key, item):
        """ Add an item in the cache """
        if key is not None and item is not None:
            if key not in self.cache_data:
                self.order.append(key)  # Keep track of the insertion order

            self.cache_data[key] = item

            if len(self.cache_data) > BaseCaching.MAX_ITEMS:
                oldest_key = self.order.popleft()  # Get the first item (FIFO)
                del self.cache_data[oldest_key]  # Remove it from the cache
                print("DISCARD: {}".format(oldest_key))

    def get(self, key):
        """ Get an item by key """
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data[key]
