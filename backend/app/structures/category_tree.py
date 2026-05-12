from typing import List, Dict, Optional, Any

class CategoryNode:
    def __init__(self, name: str):
        self.name = name
        self.children: List['CategoryNode'] = []

    def add_child(self, child_node: 'CategoryNode'):
        self.children.append(child_node)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "children": [child.to_dict() for child in self.children]
        }

class CategoryTree:
    """
    Organizes categories and subcategories in a tree structure.
    """
    def __init__(self):
        self.root = CategoryNode("Root")
        self._node_map: Dict[str, CategoryNode] = {"Root": self.root}

    def add_category(self, name: str, parent_name: str = "Root") -> bool:
        """
        Adds a new category under the specified parent.
        Returns True if successful, False if parent does not exist.
        """
        if name in self._node_map:
            return False # Category already exists
            
        if parent_name not in self._node_map:
            return False # Parent not found
            
        new_node = CategoryNode(name)
        self._node_map[name] = new_node
        self._node_map[parent_name].add_child(new_node)
        return True

    def get_subcategories(self, name: str) -> List[str]:
        """
        Returns a list of direct subcategory names for a given category.
        """
        if name not in self._node_map:
            return []
        return [child.name for child in self._node_map[name].children]

    def get_all_categories(self) -> Dict[str, Any]:
        """
        Returns the entire tree as a dictionary.
        """
        return self.root.to_dict()
