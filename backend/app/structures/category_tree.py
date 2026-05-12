from typing import Dict, List, Optional


class CategoryNode:
    """
    Represents a node in the category tree.
    """

    def __init__(self, name: str):
        self.name = name
        self.children: Dict[str, 'CategoryNode'] = {}

    def add_child(self, child_name: str) -> 'CategoryNode':
        if child_name not in self.children:
            self.children[child_name] = CategoryNode(child_name)
        return self.children[child_name]

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "children": [child.to_dict() for child in self.children.values()]
        }


class CategoryTree:
    """
    Organizes categories and subcategories in a hierarchical tree structure.
    """

    def __init__(self):
        self.root = CategoryNode("root")

    def add_category_path(self, path: List[str]) -> None:
        """
        Adds a category hierarchy. e.g., ["Infrastructure", "Building A", "Room 101"]
        """
        current = self.root
        for part in path:
            current = current.add_child(part)

    def get_subcategories(self, path: List[str]) -> List[str]:
        """
        Returns names of immediate subcategories for a given path.
        """
        current = self.root
        for part in path:
            if part in current.children:
                current = current.children[part]
            else:
                return []
        return list(current.children.keys())

    def search_category(self, name: str) -> bool:
        """
        Performs a depth-first search to find if a category exists.
        """
        return self._search_recursive(self.root, name)

    def _search_recursive(self, node: CategoryNode, name: str) -> bool:
        if node.name == name:
            return True
        for child in node.children.values():
            if self._search_recursive(child, name):
                return True
        return False

    def display(self) -> Dict:
        """
        Returns a dictionary representation of the tree.
        """
        return self.root.to_dict()
