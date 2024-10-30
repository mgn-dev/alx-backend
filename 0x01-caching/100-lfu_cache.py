#!/usr/bin/env python3
""" LFUCache module
"""
from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """ LFUCache provides a caching system using LFU algorithm """

    def __init__(self):
        """ Initialize the cache """
        super().__init__()
        self.frequency = {}  # Dictionary to keep track of access frequencies
        self.order = []      # List to keep LRU access order in same frequency

    def put(self, key, item):
        """ Add an item in the cache """
        if key is None or item is None:
            return

        if key in self.cache_data:
            # Update the existing item
            self.cache_data[key] = item
            self.frequency[key] += 1  # Increase frequency
            self.order.remove(key)     # Remove the key from order
            self.order.append(key)      # Append it to the end for LRU
            return

        # If the cache is full, we must remove an item
        if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            # Find the least frequently used items
            min_freq = min(self.frequency.values())
            # Get candidates with the minimum frequency
            candidates = \
                [k for k, v in self.frequency.items() if v == min_freq]

            if candidates:
                # Among the candidates, find the least recently used
                lru_key = self.order[self.order.index(candidates[0])]
                del self.cache_data[lru_key]  # Remove from cache
                del self.frequency[lru_key]    # Remove frequency tracking
                self.order.remove(lru_key)      # Update order
                print("DISCARD: {}".format(lru_key))

        # Add the new key-value pair to cache
        self.cache_data[key] = item
        self.frequency[key] = 1  # New item frequency
        self.order.append(key)    # Track access order

    def get(self, key):
        """ Retrieve an item by key """
        if key is None or key not in self.cache_data:
            return None

        # Update the frequency and order
        self.frequency[key] += 1  # Increase frequency
        self.order.remove(key)     # Remove key from the order
        self.order.append(key)      # Append it to the end for LRU
        return self.cache_data[key]
