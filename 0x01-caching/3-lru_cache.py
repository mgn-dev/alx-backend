#!/usr/bin/env python3
""" LRUCache module
"""
from base_caching import BaseCaching


class LRUCache(BaseCaching):
    """ LRUCache provides a caching system using LRU algorithm """

    def __init__(self):
        """ Initialize the cache """
        super().__init__()
        self.order = []  # List to keep track of the order of keys

    def put(self, key, item):
        """ Add an item in the cache """
        if key is not None and item is not None:
            if key in self.cache_data:
                # If the key already exists, remove it and update the order
                self.order.remove(key)
            elif len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                # Cache is full, discard the least recently used item
                lru_key = self.order.pop(0)  # Remove the first item (LRU)
                del self.cache_data[lru_key]  # Remove from cache
                print("DISCARD: {}".format(lru_key))

            # Add the new key-value pair to the cache and order
            self.cache_data[key] = item
            self.order.append(key)  # Update the order of keys

    def get(self, key):
        """ Get an item by key """
        if key is None or key not in self.cache_data:
            return None

        # Move the accessed key to the end of the order list
        self.order.remove(key)
        self.order.append(key)  # Update the order since it's recently used
        return self.cache_data[key]
