from __future__ import annotations
from threedeebeetree import Point, BeeNode
from ratio import Percentiles


def make_ordering(my_coordinate_list: list[Point]) -> list[Point]:
    """
    Returns a list of ordered points which produces a balanced a ThreeDeeBeeTree.

    Arguments:
        -my_coordinate_list: List of points

    Complexity: O(_make_ordering_aux)
    where _make_ordering_aux is the complexity of the _make_ordering_aux() method
    """

    def _make_ordering_aux(coordinate_list: list[Point]) -> list[Point]:
        """
        Auxiliary function of make_ordering() method

        Arguments:
            -coordinate_list: List of points

        Complexity: O(N(log^2)N)
        where N is the number of points in the list
        """
        if len(coordinate_list) < 18:
            return coordinate_list

        # Base case: For any node in the 3DBT, splitting its children by those with a negative offset of one of the
        # three axis and those with a positive offset of the same axis have a size ratio of at most 1:7 (Or both sides
        # have at most 17 nodes).

        x_percentiles = Percentiles()
        y_percentiles = Percentiles()
        z_percentiles = Percentiles()

        for point in coordinate_list:  # O(NlogN)
            x_percentiles.add_point(point[0])
            y_percentiles.add_point(point[1])
            z_percentiles.add_point(point[2])

        a: float = 1 / 8 * 100

        # The ratio of "a" is derived based on the concept of dividing the space into 8 octant (representing each child
        # of a node), where each axis (x, y, z) has a ratio of 1:3. When multiplied by two, it becomes a 2:6 ratio,
        # reflecting the subdivision of space into smaller regions.

        valid_x_root: list[Point[0]] = x_percentiles.ratio(a, a)
        valid_y_root: list[Point[1]] = y_percentiles.ratio(a, a)
        valid_z_root: list[Point[2]] = z_percentiles.ratio(a, a)

        # By calculating the percentiles using the x_percentiles.ratio(a, a), y_percentiles.ratio(a, a),
        # and z_percentiles.ratio(a, a) functions, a valid range of coordinates is obtained for each axis. These ranges
        # represent the subdivisions or octant in which the points will be categorized.

        root_element: Point | None = None

        for point in coordinate_list:  # O(n)
            if point[0] in valid_x_root and point[1] in valid_y_root and point[2] in valid_z_root:
                root_element = point
                break

        if root_element is None:
            return coordinate_list

        # During the iteration over the input list, the coordinates of each point are compared against the valid ranges
        # obtained from the percentiles. If a point falls within the valid range for all three axes (x, y, z),
        # it is considered a valid root node. This filtering process helps identify the appropriate root node for the
        # current octant, ensuring that each subtree contains points within the desired ratio range.

        # If a valid root node cannot be found within the input list, indicating that no point satisfies the criteria
        # for the desired ratio range, the original list is returned as it is. This ensures that the algorithm
        # handles cases where the input data does not have a suitable root node, allowing for the possibility of
        # empty or incomplete octant in the resulting tree structure.

        coordinate_list = [point for point in coordinate_list if point != root_element]  # O(N)

        octant = [[] for _ in range(8)]

        root_node = BeeNode(root_element, None)

        for point in coordinate_list:  # O(N)
            index: int = root_node.get_child_index(point)
            octant[index].append(point)

        # After removing the root element from the coordinate list using list comprehension, the algorithm proceeds to
        # create empty lists for each of the eight octant. Then, it initializes a root node object of type BeeNode using
        # the root element to access the get_child_index method.

        # During the iteration over the remaining points in the coordinate list, each point is assigned to the
        # appropriate octant based on its child index relative to the root node. The points are appended to their
        # respective octant lists.

        ordered_points: list[Point] = [root_element]

        for children in octant:  # O(logN)
            ordered_points.extend(_make_ordering_aux(children))  # O(NlogN)

        # The ordered_points list is initialized with the root element. The algorithm recursively calls
        # _make_ordering_aux on each child octant and extends the ordered_points list with the resulting ordered points
        # from each octant.

        return ordered_points

    return _make_ordering_aux(my_coordinate_list)  # O(_make_ordering_aux)
