#!/usr/bin/env python3
""" LIFOCache module
"""
from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """ LIFOCache provides a caching system using LIFO algorithm """

    def __init__(self):
        """ Initialize the cache """
        super().__init__()
        self.order = []  # List to keep track of the order of keys

    def put(self, key, item):
        """ Add an item in the cache """
        if key is not None and item is not None:
            # If the key is already in cache, remove it and re-add it
            if key in self.cache_data:
                self.order.remove(key)
            self.cache_data[key] = item
            self.order.append(key)  # Track the order of keys

            # Check if we exceed the limit defined by MAX_ITEMS
            if len(self.cache_data) > BaseCaching.MAX_ITEMS:
                last_key = self.order.pop()  # Pop the last inserted key (LIFO)
                del self.cache_data[last_key]  # Remove it from the cache
                print("DISCARD: {}".format(last_key))

    def get(self, key):
        """ Get an item by key """
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data[key]
