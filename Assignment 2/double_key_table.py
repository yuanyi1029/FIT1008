from __future__ import annotations
from typing import Generic, TypeVar, Iterator
from data_structures.hash_table import LinearProbeTable, FullError
from data_structures.referential_array import ArrayR

K1 = TypeVar('K1')
K2 = TypeVar('K2')
V = TypeVar('V')


class DoubleKeyTable(Generic[K1, K2, V]):
    """
    Double Hash Table.

    Type Arguments:
        - K1:   1st Key Type. In most cases should be string.
                Otherwise `hash1` should be overwritten.
        - K2:   2nd Key Type. In most cases should be string.
                Otherwise `hash2` should be overwritten.
        - V:    Value Type.

    Unless stated otherwise, all methods have O(1) complexity.
    """

    # No test case should exceed 1 million entries.
    TABLE_SIZES = [5, 13, 29, 53, 97, 193, 389, 769, 1543, 3079, 6151, 12289, 24593, 49157, 98317, 196613, 393241,
                   786433, 1572869]

    HASH_BASE = 31

    def __init__(self, sizes: list[int] | None = None, internal_sizes: list[int] | None = None) -> None:
        """
        Initialises a DoubleKeyTable object.

        Arguments:
            -sizes: List of top-level table sizes
            -internal_sizes: List of low-level table sizes

        Complexity: O(self.sizes[self.size_index])
        """
        if sizes is not None:
            self.sizes: list[int] = sizes
        else:
            self.sizes = DoubleKeyTable.TABLE_SIZES

        if internal_sizes is not None:
            self.internal_sizes: list[int] = internal_sizes
        else:
            self.internal_sizes = DoubleKeyTable.TABLE_SIZES

        self.size_index: int = 0
        self.array: ArrayR[tuple[K1, LinearProbeTable[K2, V]]] = ArrayR(self.sizes[self.size_index])
        # O(self.sizes[self.size_index])

        # Top-level table is created by using ArrayR with the argument self.sizes[self.size_index], which represents
        # the size of the table.

        self.count: int = 0

    def hash1(self, key: K1) -> int:
        """
        Hash the 1st key for insert/retrieve/update into the hashtable.

        Arguments:
            -key: 1st Key Type

        Complexity: O(len(key))
        """
        value: int = 0
        a: int = 31415

        for char in key:  # O(len(key))
            value = (ord(char) + a * value) % self.table_size
            a = a * self.HASH_BASE % (self.table_size - 1)

        return value

    def hash2(self, key: K2, sub_table: LinearProbeTable[K2, V]) -> int:
        """
        Hash the 2nd key for insert/retrieve/update into the hashtable.

        Arguments:
            -key: 2nd Key Type
            -sub_table: LinearProbeTable object

        Complexity: O(len(key))
        """
        value: int = 0
        a: int = 31415

        for char in key:  # O(len(key))
            value = (ord(char) + a * value) % sub_table.table_size
            a = a * self.HASH_BASE % (sub_table.table_size - 1)

        return value

    def _linear_probe(self, key1: K1, key2: K2, is_insert: bool) -> tuple[int, int]:
        """
        Find the correct position for this key in the hash table using linear probing.

        :raises KeyError: When the key pair is not in the table, but is_insert is False.
        :raises FullError: When a table is full and cannot be inserted.

        Arguments:
            -key1: 1st Key Type
            -key2: 2nd Key Type
            -is_insert: Specifies whether the key pair is inserted or not.

        Best Complexity: O(len(key1)+len(key2)*m) when key pairs are found in their initial hashing position.
        Worst Complexity: O(self.table_size*sub_table_linear_probe*m) when key pairs needs to be linear probed.

        where sub_table_linear_probe is the complexity of the _linear_probe() method of the LinearProbeTable class,
        and m is the comparison of keys.
        """
        key1_position: int = self.hash1(key1)  # O(len(key1))

        for _ in range(self.table_size):  # O(self.table_size)
            if self.array[key1_position] is None:
                if is_insert:
                    internal_hash_table: LinearProbeTable[K2, V] = LinearProbeTable(self.internal_sizes)
                    # O(internal_size)

                    internal_hash_table.hash = lambda k: self.hash2(k, internal_hash_table)
                    key2_position: int = self.hash2(key2, internal_hash_table)  # O(len(key2))
                    self.array[key1_position] = (key1, internal_hash_table)
                    return key1_position, key2_position

                else:
                    raise KeyError(key1)

                # Traverses the top-level table starting at position of key1 and when None is located and is_insert
                # is True (indicating that there is space for the key pair to be added). a low-level hash table is
                # generated and The location of key2 is determined. The low-level table and key1 are paired up into a
                # tuple and stored in the top-level table's None position.

                # A Key Error for key1 will be raised if None is located and is_insert is False in the position
                # (meaning there is nothing to be retrieved from the key1 position).

            elif self.array[key1_position][0] == key1:  # O(m)
                internal_hash_table = self.array[key1_position][1]
                key2_position = internal_hash_table._linear_probe(key2, is_insert) 
                # Best Complexity: O(len(key2)) when first position is empty
                # Worst Complexity: O(len(key2)+self.table_size*m) when entire table is searched

                return key1_position, key2_position

                # The _linear_probe function from the low-level hash table is used to find the position of key2 if
                # the tuple in position of key1 has key1 as its first value (index 0). The positions of keys 1 and 2
                # are then returned.

            key1_position = (key1_position + 1) % self.table_size

            # If None and key1 are not found in the top-level table, the initial key1 position obtained by hashing is
            # incremented by one and modded with table size.

        if is_insert:
            raise FullError("Table is full!")

        else:
            raise KeyError(key1, key2)

        # After iterating over the whole table, if nothing was returned and is_insert is True, Full Error will be
        # raised as there is no empty spaces in the top-level table to insert the new key pair.

        # A Key Error for key1 will be raised if is_insert is False (meaning key1 cannot be retrieved since it is not
        # present in the top-level table).

    def iter_keys(self, key: K1 | None = None) -> Iterator[K1 | K2]:
        """
        key = None:
            Returns an iterator of all top-level keys in hash table
        key = k:
            Returns an iterator of all keys in the bottom-hash-table for k.

        Arguments:
            -key: 1st Key Type

        Complexity: O(len(keys)*keys)
        where keys is the complexity of the keys() method of the DoubleKeyTable class.
        """
        for index in range(len(self.keys(key))):  # O(len(keys))
            yield self.keys(key)[index]  # O(keys)

        # Returns an iterator using the keys() method of the DoubleKeyTable class.

    def keys(self, key: K1 | None = None) -> list[K1]:
        """
        key = None: returns all top-level keys in the table.
        key = x: returns all bottom-level keys for top-level key x.

        Arguments:
            -key: 1st Key Type

        Complexity: O(self.table_size*(m+sub_table_keys))
        where sub_table_keys is the complexity of the keys() method of the LinearProbeTable class,
        and m is the comparison of keys.
        """
        if key is None:
            return [self.array[index][0] for index in range(self.table_size) if self.array[index] is not None]
            # O(self.table_size)

        # If key is None, a list of top-level table keys will be returned by iterating over the table and filtering
        # out None values.

        for index in range(self.table_size):  # O(self.table_size)
            if self.array[index] is not None and self.array[index][0] == key:  # O(m)
                internal_hash_table: LinearProbeTable[K2, V] = self.array[index][1]
                return internal_hash_table.keys()  # O(sub_table_keys)

        # If key is given, the top-level table will be traversed to locate the matching key, and the bottom-level
        # table keys for that key will be returned by calling the low-level hash table's keys() method.

        return []

        # If the key cannot be located in the top-level table, an empty list is returned.

    def iter_values(self, key: K1 | None = None) -> Iterator[V]:
        """
        key = None:
            Returns an iterator of all values in hash table
        key = k:
            Returns an iterator of all values in the bottom-hash-table for k.

        Arguments:
            -key: 1st Key Type

        Complexity: O(len(values)*values)
        where values is the complexity of the values() method of the DoubleKeyTable class.
        """
        for index in range(len(self.values(key))):  # O(len(values))
            yield self.values(key)[index]  # O(values)

        # Returns an iterator using the values() method of the DoubleKeyTable class.

    def values(self, key: K1 | None = None) -> list[V]:
        """
        key = None: returns all values in the table.
        key = x: returns all values for top-level key x.

        Arguments:
            -key: 1st Key Type

        Complexity: O(self.table_size*(m+sub_table_values))
        where sub_table_values is the complexity of the values() method of the LinearProbeTable class,
        and m is the comparison of keys.
        """
        if key is None:
            return [value for index in range(self.table_size) if self.array[index] is not None
                    for value in self.array[index][1].values()]

            # O(self.table_size)

        # If key is None, a list of all values in the table will be returned by iterating over the top-level table
        # and filtering out None values, and by calling the low-level hash table's values() method.

        for index in range(self.table_size):  # O(self.table_size)
            if self.array[index] is not None and self.array[index][0] == key:  # O(m)
                internal_hash_table: LinearProbeTable[K2, V] = self.array[index][1]
                return internal_hash_table.values()  # O(sub_table_values)

        # If key is given, the top-level table will be traversed to locate the matching key, and the bottom-level
        # table values for that key will be returned by calling the low-level hash table's values() method.

        return []

        # If the key cannot be located in the top-level table, an empty list is returned.

    def __contains__(self, key: tuple[K1, K2]) -> bool:
        """
        Checks to see if the given key is in the Hash Table

        Arguments:
            -key: Tuple of 1st and 2nd Key Types

        Complexity: O(_linear_probe)
        where _linear_probe is the complexity of the _linear_probe() method of the DoubleKeyTable class.
        """
        try:
            _ = self[key]  # O(_linear_probe)

        except KeyError:
            return False

        else:
            return True

    def __getitem__(self, key: tuple[K1, K2]) -> V:
        """
        Get the value at a certain key

        :raises KeyError: when the key doesn't exist.

        Arguments:
            -key: Tuple of 1st and 2nd Key Types

        Complexity: O(_linear_probe+sub_table_getitem)
        where _linear_probe is the complexity of the _linear_probe() method of the DoubleKeyTable class, and
        sub_table_setitem is the complexity of the __getitem__() method of the LinearProbeTable class.
        """
        key1_position: int
        key2_position: int

        key1_position, key2_position = self._linear_probe(key[0], key[1], False)  # O(_linear_probe)
        internal_hash_table: LinearProbeTable[K2, V] = self.array[key1_position][1]

        return internal_hash_table[key[1]]  # O(sub_table_getitem)

        # The key pairs' positions are obtained using the top-level table's linear probe method, which is then used
        # to identify the keys' low-level hash table. The value at a certain key pair is returned by calling the
        # low-level hash table's get function.

    def __setitem__(self, key: tuple[K1, K2], data: V) -> None:
        """
        Set an (key, value) pair in our hash table.

        Arguments:
            -key: Tuple of 1st and 2nd Key Types
            -data: Value Type

        Best Complexity: O(_linear_probe+sub_table_setitem) when there is no resizing.
        Worst Complexity: O(_linear_probe+sub_table_setitem+_rehash) when there is resizing.

        where _linear_probe is the complexity of the _linear_probe() method of the DoubleKeyTable class,
        sub_table_setitem is the complexity of the __setitem__() method of the LinearProbeTable class, and
        _rehash is the complexity of the _rehash() method of the DoubleKeyTable class.
        """
        key1_position: int
        key2_position: int

        key1_position, key2_position = self._linear_probe(key[0], key[1], True)  # O(_linear_probe)
        internal_hash_table: LinearProbeTable[K2, V] = self.array[key1_position][1]

        if internal_hash_table.is_empty():
            self.count += 1

        internal_hash_table[key[1]] = data  # O(sub_table_setitem)

        # The key pairs' positions are obtained using the top-level table's linear probe method, which is then used
        # to identify the keys' low-level hash table. If the low-level hash table is empty (meaning a new key1 is
        # added to the top-level table), the count is incremented by one. The data value is then inserted into the
        # table by calling the set function of the low-level hash table.

        if len(self) > self.table_size / 2:
            self._rehash()  # O(_rehash)

        # If the load factor exceeds 0.5, the top-level table is resized.

    def __delitem__(self, key: tuple[K1, K2]) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.

        Arguments:
            -key: Tuple of 1st and 2nd Key Types

        Best Complexity: O(_linear_probe+sub_table_delitem) when there is no probing.
        Worst Complexity: O(_linear_probe+sub_table_delitem+self.table_size^2) when table is full and the entire table
        is probed.

        where _linear_probe is the complexity of the _linear_probe() method of the DoubleKeyTable class, and
        sub_table_delitem is the complexity of the __delitem__() method of the LinearProbeTable class
        """
        key1_position: int
        key2_position: int

        key1_position, key2_position = self._linear_probe(key[0], key[1], False)  # O(_linear_probe)
        internal_hash_table: LinearProbeTable[K2, V] = self.array[key1_position][1]

        del internal_hash_table[key[1]]  # O(sub_table_delitem)

        # The key pairs' positions are obtained using the top-level table's linear probe method, which is then used
        # to identify the keys' low-level hash table. The key value pair is then deleted from the table by calling
        # the delete function of the low-level hash table.

        if internal_hash_table.is_empty():
            self.array[key1_position] = None
            self.count -= 1

            key1_position = (key1_position + 1) % self.table_size

            while self.array[key1_position] is not None:
                # Best Complexity: O(1) when there is no cluster
                # Worst Complexity: O(self.table_size) when table is full

                key1: K1
                internal_hash_table: LinearProbeTable[K2, V]

                key1, internal_hash_table = self.array[key1_position]

                self.array[key1_position] = None

                new_key1_position: int = self.hash1(key1)  # O(len(key1))

                while self.array[new_key1_position] is not None:  # O(self.table_size)
                    # Best Complexity: O(1) when there is no probing
                    # Worst Complexity: O(self.table_size) when the entire table is probed

                    new_key1_position = (new_key1_position + 1) % self.table_size

                self.array[new_key1_position] = key1, internal_hash_table

                key1_position = (key1_position + 1) % self.table_size

        # If the low-level hash table is empty after removing the key value pair (which means key1 in the top-level
        # table does not have a pair key), count should be decremented by one and key1's position in the top-level
        # table should be set to None. Following that, all elements in key1's cluster will be rehashed and reinserted
        # into their respective positions via linear probing.

    def _rehash(self) -> None:
        """
        Need to resize table and reinsert all values

        Best Complexity: O(len(original_array)*len(key1)) when there is no probing.
        Worst Complexity: O(len(original_array)*self.table_size) when the entire table is probed.
        """
        self.size_index += 1

        if self.size_index == len(self.sizes):
            return

        # The size index will be incremented by one, and if the index matches the length of the sizes list, the rehash
        # method will be halted since the top-level table cannot be resized any more because no additional sizes
        # are available in the list.

        original_array: ArrayR[tuple[K1, LinearProbeTable[K2, V]]] = self.array

        self.array: ArrayR[tuple[K1, LinearProbeTable[K2, V]]] = ArrayR(self.sizes[self.size_index])
        # O(self.sizes[self.size_index])

        # The top-level table is stored in the original_array variable, then it gets assigned a newly resized ArrayR
        # object, and all key value pairs have to be transferred from the original top-level table to the newly
        # created one.

        for elem in original_array:  # O(len(original_array))
            if elem is not None:
                key1: K1
                internal_hash_table: LinearProbeTable[K2, V]

                key1, internal_hash_table = elem

                new_key1_position: int = self.hash1(key1)  # O(len(key1))

                while self.array[new_key1_position] is not None:
                    # Best Complexity: O(1) when there is no probing
                    # Worst Complexity: O(self.table_size) when the entire table is probed

                    new_key1_position = (new_key1_position + 1) % self.table_size

                self.array[new_key1_position] = key1, internal_hash_table

        # By traversing through the original top-level table, all elements from the table will be rehashed and
        # reinserted into their respective positions via linear probing.

    @property
    def table_size(self) -> int:
        """
        Return the current size of the table (different from the length)

        Complexity: O(1)
        """
        return len(self.array)

    def __len__(self) -> int:
        """
        Returns number of elements in the hash table

        Complexity: O(1)
        """
        return self.count

    def __str__(self) -> str:
        """
        String representation.

        Not required but may be a good testing tool.

        Complexity:
        """
        raise NotImplementedError()
