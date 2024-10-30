#!/usr/bin/python3
""" LIFOCache module
"""
from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """ LIFOCache provides a caching system using LIFO algorithm """

    def __init__(self):
        """ Initialize the cache """
        super().__init__()
        self.keys = []  # List to keep track of the order of keys

    def put(self, key, item):
        """ Add an item in the cache """
        if key is not None and item is not None:
            # If the key already exists, we'll update and keep its position
            if key in self.cache_data:
                self.keys.remove(key)

            self.cache_data[key] = item
            self.keys.append(key)

            # Check if we exceed the limit defined by MAX_ITEMS
            if len(self.cache_data) > BaseCaching.MAX_ITEMS:
                last_key = self.keys.pop()  # Pop the last inserted key (LIFO)
                del self.cache_data[last_key]  # Remove it from the cache
                print("DISCARD: {}".format(last_key))

    def get(self, key):
        """ Get an item by key """
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data[key]
