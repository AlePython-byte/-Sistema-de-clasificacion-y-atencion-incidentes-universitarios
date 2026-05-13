class CategoryTree:
    def __init__(self) -> None:
        self._categories: dict[str, dict] = {}
        self._roots: list[str] = []

    def add_category(self, name: str, parent_name: str | None = None) -> None:
        category_name = self._normalize_name(name)
        if not category_name:
            raise ValueError("Category name cannot be empty.")

        if category_name in self._categories:
            return

        if parent_name is None:
            self._categories[category_name] = {"name": category_name, "children": []}
            self._roots.append(category_name)
            return

        parent_category_name = self._normalize_name(parent_name)
        parent_category = self._categories.get(parent_category_name)
        if parent_category is None:
            raise ValueError(f"Parent category '{parent_category_name}' does not exist.")

        self._categories[category_name] = {"name": category_name, "children": []}
        parent_category["children"].append(category_name)

    def find_category(self, name: str) -> dict | None:
        category_name = self._normalize_name(name)
        category = self._categories.get(category_name)
        if category is None:
            return None

        return self._build_category_dict(category_name)

    def get_tree(self) -> dict:
        return {
            "categories": [
                self._build_category_dict(category_name)
                for category_name in self._roots
            ]
        }

    def get_children(self, name: str) -> list[str]:
        category_name = self._normalize_name(name)
        category = self._categories.get(category_name)
        if category is None:
            return []

        return category["children"].copy()

    def category_exists(self, name: str) -> bool:
        return self._normalize_name(name) in self._categories

    def clear(self) -> None:
        self._categories.clear()
        self._roots.clear()

    def _build_category_dict(self, name: str) -> dict:
        category = self._categories[name]
        return {
            "name": category["name"],
            "children": [
                self._build_category_dict(child_name)
                for child_name in category["children"]
            ],
        }

    def _normalize_name(self, name: str) -> str:
        return name.strip()
