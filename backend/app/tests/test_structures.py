import pytest
from app.structures.priority_queue import PriorityQueueManager
from app.structures.history_stack import IncidentHistoryStack
from app.structures.category_tree import CategoryTree

def test_priority_queue_manager():
    pq = PriorityQueueManager()
    
    pq.push("Incident 1", "LOW")
    pq.push("Incident 2", "CRITICAL")
    pq.push("Incident 3", "HIGH")
    pq.push("Incident 4", "MEDIUM")
    
    assert pq.size() == 4
    assert pq.pop() == "Incident 2"  # CRITICAL
    assert pq.pop() == "Incident 3"  # HIGH
    assert pq.pop() == "Incident 4"  # MEDIUM
    assert pq.pop() == "Incident 1"  # LOW
    assert pq.is_empty()

def test_incident_history_stack():
    stack = IncidentHistoryStack()
    
    stack.push({"action": "create", "id": 1})
    stack.push({"action": "assign", "id": 1})
    stack.push({"action": "resolve", "id": 1})
    
    assert stack.size() == 3
    assert stack.pop()["action"] == "resolve"
    assert stack.peek()["action"] == "assign"
    assert stack.size() == 2
    
    stack.clear()
    assert stack.is_empty()

def test_category_tree():
    tree = CategoryTree()
    
    tree.add_category_path(["Infrastructure", "Building A", "Room 101"])
    tree.add_category_path(["Infrastructure", "Building B"])
    tree.add_category_path(["IT", "Network", "WiFi"])
    
    assert tree.search_category("Infrastructure") is True
    assert tree.search_category("WiFi") is True
    assert tree.search_category("NonExistent") is False
    
    infra_subs = tree.get_subcategories(["Infrastructure"])
    assert "Building A" in infra_subs
    assert "Building B" in infra_subs
    assert len(infra_subs) == 2
    
    network_subs = tree.get_subcategories(["IT", "Network"])
    assert network_subs == ["WiFi"]

    display = tree.display()
    assert display["name"] == "root"
    assert any(c["name"] == "Infrastructure" for c in display["children"])
