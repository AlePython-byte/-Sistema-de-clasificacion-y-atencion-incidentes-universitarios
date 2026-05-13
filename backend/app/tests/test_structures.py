import pytest

from app.structures.category_tree import CategoryTree
from app.structures.history_stack import IncidentHistoryStack
from app.structures.priority_queue import PriorityQueueManager


def test_priority_queue_returns_critical_before_high_and_low() -> None:
    queue = PriorityQueueManager()

    queue.add_incident({"id": "1", "priority": "LOW"})
    queue.add_incident({"id": "2", "priority": "CRITICAL"})
    queue.add_incident({"id": "3", "priority": "HIGH"})

    assert queue.get_next_incident()["id"] == "2"
    assert queue.get_next_incident()["id"] == "3"
    assert queue.get_next_incident()["id"] == "1"


def test_priority_queue_preserves_insertion_order_for_same_priority() -> None:
    queue = PriorityQueueManager()

    queue.add_incident({"id": "first", "priority": "HIGH"})
    queue.add_incident({"id": "second", "priority": "HIGH"})

    assert queue.get_next_incident()["id"] == "first"
    assert queue.get_next_incident()["id"] == "second"


def test_priority_queue_empty_size_peek_and_clear_work() -> None:
    queue = PriorityQueueManager()

    assert queue.is_empty()
    assert queue.size() == 0
    assert queue.peek_next_incident() is None

    queue.add_incident({"id": "1"})

    assert not queue.is_empty()
    assert queue.size() == 1
    assert queue.peek_next_incident()["id"] == "1"
    assert queue.size() == 1

    queue.clear()

    assert queue.is_empty()
    assert queue.size() == 0


def test_history_stack_push_and_pop_work_as_lifo() -> None:
    stack = IncidentHistoryStack()

    stack.push_event({"id": "event-1"})
    stack.push_event({"id": "event-2"})

    assert stack.pop_event()["id"] == "event-2"
    assert stack.pop_event()["id"] == "event-1"
    assert stack.pop_event() is None


def test_history_stack_peek_does_not_remove_event() -> None:
    stack = IncidentHistoryStack()
    stack.push_event({"id": "event-1"})

    assert stack.peek_event()["id"] == "event-1"
    assert stack.size() == 1


def test_history_stack_get_events_returns_copy() -> None:
    stack = IncidentHistoryStack()
    stack.push_event({"id": "event-1"})

    events = stack.get_events()
    events.append({"id": "external-event"})

    assert stack.size() == 1
    assert stack.get_events() == [{"id": "event-1"}]


def test_history_stack_empty_size_and_clear_work() -> None:
    stack = IncidentHistoryStack()

    assert stack.is_empty()
    assert stack.size() == 0

    stack.push_event({"id": "event-1"})
    assert not stack.is_empty()
    assert stack.size() == 1

    stack.clear()
    assert stack.is_empty()
    assert stack.size() == 0


def test_category_tree_adds_root_categories() -> None:
    tree = CategoryTree()

    tree.add_category("Technology")
    tree.add_category("Infrastructure")

    assert tree.category_exists("Technology")
    assert tree.category_exists("Infrastructure")
    assert len(tree.get_tree()["categories"]) == 2


def test_category_tree_adds_subcategories_and_returns_children() -> None:
    tree = CategoryTree()

    tree.add_category("Technology")
    tree.add_category("Internet", parent_name="Technology")
    tree.add_category("Projector", parent_name="Technology")

    assert tree.get_children("Technology") == ["Internet", "Projector"]


def test_category_tree_finds_existing_category() -> None:
    tree = CategoryTree()

    tree.add_category("Security")
    tree.add_category("Access", parent_name="Security")

    category = tree.find_category("Security")

    assert category == {
        "name": "Security",
        "children": [{"name": "Access", "children": []}],
    }


def test_category_tree_returns_none_when_category_does_not_exist() -> None:
    tree = CategoryTree()

    assert tree.find_category("Unknown") is None


def test_category_tree_raises_error_when_parent_does_not_exist() -> None:
    tree = CategoryTree()

    with pytest.raises(ValueError, match="Parent category 'Unknown' does not exist."):
        tree.add_category("Internet", parent_name="Unknown")


def test_category_tree_does_not_duplicate_categories() -> None:
    tree = CategoryTree()

    tree.add_category("Technology")
    tree.add_category("Technology")

    assert len(tree.get_tree()["categories"]) == 1


def test_category_tree_rejects_empty_category_names_and_can_clear() -> None:
    tree = CategoryTree()

    with pytest.raises(ValueError, match="Category name cannot be empty."):
        tree.add_category("   ")

    tree.add_category("Technology")
    tree.clear()

    assert tree.get_tree() == {"categories": []}
    assert not tree.category_exists("Technology")
