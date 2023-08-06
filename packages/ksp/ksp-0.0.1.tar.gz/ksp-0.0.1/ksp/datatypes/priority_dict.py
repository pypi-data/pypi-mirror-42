#  Copyright 2002 David Eppstein, UC Irvine
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
# http://code.activestate.com/recipes/117228/
from __future__ import generators

class PriorityDictionary(dict):
    def __init__(self):
        '''Initialize PriorityDictionary by creating binary heap of pairs
        (value, key).  Note that changing or removing a dict entry will not
        remove the old pair from the heap until it is found by smallest() or
		until the heap is rebuilt.'''
        self.__heap = []
        dict.__init__(self)

    def smallest(self):
        '''Find smallest item after removing deleted items from heap.'''
        if len(self) == 0:
            raise IndexError("smallest of empty PriorityDictionary")
        heap = self.__heap
        while heap[0][1] not in self or self[heap[0][1]] != heap[0][0]:
            last_item = heap.pop()
            insertion_point = 0
            while 1:
                small_child = 2*insertion_point+1
                if small_child+1 < len(heap) and \
                        heap[small_child] > heap[small_child+1]:
                    small_child += 1
                if small_child >= len(heap) or last_item <= heap[small_child]:
                    heap[insertion_point] = last_item
                    break
                heap[insertion_point] = heap[small_child]
                insertion_point = small_child
        return heap[0][1]

    def __iter__(self):
        '''Create destructive sorted iterator of PriorityDictionary.'''
        def iterfn():
            while len(self) > 0:
                x = self.smallest()
                yield x
                del self[x]
        return iterfn()

    def __setitem__(self, key, val):
        '''Change value stored in dictionary and add corresponding pair to heap.
        Rebuilds the heap if the number of deleted items grows too large, to
        avoid memory leakage.'''
        dict.__setitem__(self, key, val)
        heap = self.__heap
        if len(heap) > 2 * len(self):
            self.__heap = [(v,k) for k,v in self.items()]
            self.__heap.sort()  # builtin sort likely faster than O(n) heapify
        else:
            new_pair = (val,key)
            insertion_point = len(heap)
            heap.append(None)
            while insertion_point > 0 and \
                    new_pair < heap[(insertion_point-1)//2]:
                heap[insertion_point] = heap[(insertion_point-1)//2]
                insertion_point = (insertion_point-1)//2
            heap[insertion_point] = new_pair

    def setdefault(self, key, val):
        '''Reimplement setdefault to call our customized __setitem__.'''
        if key not in self:
            self[key] = val
        return self[key]

    def update(self, other):
        for key in other.keys():
            self[key] = other[key]
