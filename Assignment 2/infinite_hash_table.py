from __future__ import annotations
from typing import Generic, TypeVar
from data_structures.referential_array import ArrayR
from data_structures.linked_stack import LinkedStack

K = TypeVar("K")
V = TypeVar("V")


class InfiniteHashTable(Generic[K, V]):
    """
    Infinite Hash Table.

    Type Arguments:
        - K:    Key Type. In most cases should be string.
                Otherwise `hash` should be overwritten.
        - V:    Value Type.

    Unless stated otherwise, all methods have O(1) complexity.
    """

    TABLE_SIZE = 27
    length = 0

    def __init__(self) -> None:
        """
        Initialises a InfiniteHashTable object.

        Complexity: O(InfiniteHashTable.TABLE_SIZE)
        """
        self.table: ArrayR[tuple[K, InfiniteHashTable[K, V]]] = ArrayR(InfiniteHashTable.TABLE_SIZE)
        # O(InfiniteHashTable.TABLE_SIZE)

        self.level: int = 0
        self.length: int = 0

    def hash(self, key: K) -> int:
        """
        Hash the key for insert/retrieve/update into the hashtable.

        Arguments:
            -key: Key Type

        Complexity: O(1)
        """
        if self.level < len(key):
            return ord(key[self.level]) % (self.TABLE_SIZE - 1)

        return self.TABLE_SIZE - 1

    def __getitem__(self, key: K) -> V:
        """
        Get the value at a certain key

        :raises KeyError: when the key doesn't exist.

        Arguments:
            -key: Key Type

        Best Complexity: O(1) when key is located in the outermost Infinite Hash Table.
        Worst Complexity: O(n) when key is located in a nested Infinite Hash Table.
        where n is the number of nested hash tables in the hash table.
        """
        current_hash_table: InfiniteHashTable[tuple[K, InfiniteHashTable[K, V]]] = self

        for position in self.get_location(key):  # O(get_location)
            current_hash_table = current_hash_table.table[position][1]

        return current_hash_table

        # The value at a certain key is obtained by returned the hash table using the key positions returned by the
        # InfiniteHashTable class's get_location() function.

    def __setitem__(self, key: K, value: V) -> None:
        """
        Set an (key, value) pair in our hash table.

        Arguments:
            -key: Key Type
            -value: Value Type

        Best Complexity: O(1) when key is set in the outermost Infinite Hash Table.
        Worst Complexity: O(n) when key is set in a nested Infinite Hash Table.
        where n is the number of nested hash tables in the hash table.
        """
        current_hash_table: InfiniteHashTable[tuple[K, InfiniteHashTable[K, V]]] = self

        while True:  # O(n)
            position: int = current_hash_table.hash(key)

            if current_hash_table.table[position] is None:
                current_hash_table.table[position] = key, value
                current_hash_table.length += 1
                return

            elif type(current_hash_table.table[position][1]) is InfiniteHashTable:
                current_hash_table = current_hash_table.table[position][1]

            else:
                break

        # Using an infinite while loop, the position of the key from the beginning to the end of the hash table is
        # hashed according to its level and then checked to see what is stored in that hash table's position. If the
        # hash position in the hash table is None (indicating that there is space to insert the key value pair),
        # the key value pair will be inserted into the hash table and the length of the hash table will be incremented
        # by 1; if the key value pair has another hash table as its value, the method will traverse to the next
        # linked hash table.

        # If the hash position in the hash table already contains a key value pair and there is no following linked
        # hash table, the while loop will terminate and a new hash table will be created to address the collision.

        nested_hash_table: InfiniteHashTable[tuple[K, InfiniteHashTable[K, V]]] = InfiniteHashTable()
        nested_hash_table.level = current_hash_table.level + 1

        rehashed_key: K
        rehashed_value: V

        rehashed_key, rehashed_value = current_hash_table.table[position]
        nested_hash_table[rehashed_key] = rehashed_value
        nested_hash_table[key] = value

        current_hash_table.table[position] = f"{rehashed_key[:current_hash_table.level + 1]}*", nested_hash_table

        # To resolves collisions, a new hash table is created, and the original key value pair from the previous hash
        # table is stored and rehashed into the new hash table, followed by the given key value pair. The new hash
        # table is then stored as the value in the original hash table position.

    def __delitem__(self, key: K) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.

        Arguments:
            -key: Key Type

        Best Complexity: O(1) when there is no collapsing and key is located in the outermost Infinite Hash Table.
        Worst Complexity: O(len(positions)+len(current_hash_table.table)*n) when there is collapsing
        where n is the number of nested hash tables traversed in the hash table.
        """
        current_hash_table: InfiniteHashTable[tuple[K, InfiniteHashTable[K, V]]] = self

        nested_hash_table_record: LinkedStack[InfiniteHashTable[tuple[K, InfiniteHashTable[K, V]]]] = LinkedStack()
        positions: list[int] = self.get_location(key)
        key_position: int = positions.pop()

        for position in positions:  # O(len(positions))
            nested_hash_table_record.push(current_hash_table)
            current_hash_table = current_hash_table.table[position][1]

        current_hash_table.table[key_position] = None
        current_hash_table.length -= 1

        # The given key value pair is deleted from the hash table by traversing the hash table from start to end
        # using the key positions returned by the InfiniteHashTable class's get_location() function, and popping off
        # the last position of the list to be used to access the position in the hash table to set it as None and
        # decrementing the length of that hash table by 1.

        if current_hash_table.length == 1:
            for index in range(len(current_hash_table.table)):  # O(len(current_hash_table.table))
                if type(current_hash_table.table[index]) is tuple:
                    if type(current_hash_table.table[index][1]) is not InfiniteHashTable:

                        # If the hash table length is one after removing the key value pair, the hash table will be
                        # traversed through to locate the remaining key value pair and checked to determine if the
                        # value contains a connected hash table. If the remaining key value pair does not connect to
                        # another hierarchical hash table, the hash table will be collapsed.

                        key: K
                        value: V

                        key, value = current_hash_table.table[index]

                        # Before collapsing the hash table, the remaining key value pair is stored in a variable and
                        # will be reinserted into the determined hash table after collapsing

                        while not nested_hash_table_record.is_empty():  # O(n)
                            current_hash_table = nested_hash_table_record.pop()
                            key_position = positions.pop()

                            if current_hash_table.length > 1:
                                current_hash_table.table[key_position] = key, value
                                return

                            # By traversing the nested_hash_table_record stack to pop out any hash_table encountered
                            # while traversing the hash table, the previous hash tables are compared to see if their
                            # length is greater than one (meaning they hold more than one key pair, as if it is only
                            # one, it means it was the parent key value of the remaining key value pair that should
                            # be collapsed). If a hash table contains more than one key value pair, the remaining key
                            # value pair is inserted by replacing their parent key value pair.

                        current_hash_table.table[key_position] = key, value

                        # If the loop returns to the beginning of the hash table and nothing is done (meaning the
                        # remaining key value pair are the only key value pair left in the whole hash table),
                        # the remaining key value pair will simply be reinserted at the beginning of the hash table.

                    return

    def __len__(self):
        """
        Returns number of elements in the hash table

        Best Complexity: O(len(self.table)) when all keys are located in the outermost Infinite Hash Table.
        Complexity: O(len(self.table)^n) when all keys are located in a nested Infinite Hash Table.
        where n is the number of nested hash tables in the hash table.
        """
        length: int = 0

        for index in range(len(self.table)):  # O(len(self.table))
            if type(self.table[index]) is tuple and type(self.table[index][1]) is InfiniteHashTable:
                length += len(self.table[index][1])  # O(n)

            elif self.table[index] is not None:
                length += 1

        return length

        # The length is obtained by traversing through the outer initial hash tables and then recursively traversing
        # into any nested hash tables encountered, while incrementing length by 1 when encountering key value pairs
        # that do not contain hash tables as their value.

    def __str__(self) -> str:
        """
        String representation.
        Not required but may be a good testing tool.
        """
        raise NotImplementedError()

    def get_location(self, key) -> list[int]:
        """
        Get the sequence of positions required to access this key.

        :raises KeyError: when the key doesn't exist.

        Arguments:
            -key: Key Type

        Best Complexity: O(1) when an item is located at the outer most Infinite Hash Table.
        Worst Complexity: O(n) when an item is located at an inner Infinite Hash Table.
        where n is the number of nested hash tables in the hash table.
        """
        current_hash_table: InfiniteHashTable[tuple[K, InfiniteHashTable[K, V]]] = self
        positions: list[int] = []

        while True:  # O(n)
            position: int = current_hash_table.hash(key)
            positions.append(position)

            if current_hash_table.table[position] is None:
                raise KeyError(key)

            elif type(current_hash_table.table[position][1]) is InfiniteHashTable:
                current_hash_table = current_hash_table.table[position][1]

            else:
                if current_hash_table.table[position][0] == key:
                    return positions

                else:
                    raise KeyError(key)

        # Using an infinite while loop, the position of the key from the beginning to the end of the hash table will
        # be hashed according to its level and appended to the positions list. If the hash position in the hash table
        # is None, the method will raise a Key Error since the key value pair is not in the hash table; if the key
        # value pair has another hash table as its value, the method will traverse to the next linked hash table. When
        # it reaches the end of the hash table (value pair is not a hash table), it checks if the key at position is
        # the same as the given key parameter and returns the positions list, raising a Key Error if it is not.

    def __contains__(self, key: K) -> bool:
        """
        Checks to see if the given key is in the Hash Table

        :complexity: O(get_location)
        where get_location is the complexity of the get_location() method of the InfiniteHashTable class.
        """
        try:
            _ = self[key]

        except KeyError:
            return False

        else:
            return True
