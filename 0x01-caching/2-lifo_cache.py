#!/usr/bin/python3
""" LIFOCache module
"""
from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """ LIFOCache implements a caching system using the LIFO algorithm """

    def __init__(self):
        """ Initialize the cache """
        super().__init__()
        self.keys = []  # List to keep track of the order of keys

    def put(self, key, item):
        """ Add an item in the cache """
        if key is not None and item is not None:
            if key in self.cache_data:
                # Update the existing key and move it to the end
                self.keys.remove(key)
            elif len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                # Cache is full, pop last item (most recently added) from cache
                last_key = self.keys.pop()  # LIFO: remove last inserted key
                del self.cache_data[last_key]  # Remove from cache
                print("DISCARD: {}".format(last_key))

            self.cache_data[key] = item  # Add the new key-value pair
            self.keys.append(key)  # Track the order of keys

    def get(self, key):
        """ Get an item by key """
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data[key]
