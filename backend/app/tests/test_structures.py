import pytest
from app.structures.priority_queue import PriorityQueueManager
from app.structures.history_stack import IncidentHistoryStack
from app.structures.category_tree import CategoryTree
from app.schemas.incident_schema import IncidentPriority

def test_priority_queue_manager():
    pq = PriorityQueueManager()
    
    # Enqueue incidents with different priorities
    pq.enqueue({"id": 1, "priority": IncidentPriority.LOW})
    pq.enqueue({"id": 2, "priority": IncidentPriority.CRITICAL})
    pq.enqueue({"id": 3, "priority": IncidentPriority.HIGH})
    pq.enqueue({"id": 4, "priority": IncidentPriority.MEDIUM})
    pq.enqueue({"id": 5, "priority": IncidentPriority.CRITICAL}) # Tie-breaker test

    assert pq.size() == 5
    
    # Dequeue should return CRITICAL first, and the first CRITICAL added (id=2)
    first = pq.dequeue()
    assert first is not None
    assert first["id"] == 2
    assert first["priority"] == IncidentPriority.CRITICAL
    
    # Next should be the second CRITICAL (id=5)
    second = pq.dequeue()
    assert second is not None
    assert second["id"] == 5
    
    # Next should be HIGH (id=3)
    third = pq.dequeue()
    assert third is not None
    assert third["id"] == 3
    
    # Next should be MEDIUM (id=4)
    fourth = pq.dequeue()
    assert fourth is not None
    assert fourth["id"] == 4
    
    # Next should be LOW (id=1)
    fifth = pq.dequeue()
    assert fifth is not None
    assert fifth["id"] == 1
    
    assert pq.is_empty()
    assert pq.dequeue() is None

def test_incident_history_stack():
    stack = IncidentHistoryStack()
    
    assert stack.is_empty()
    
    stack.push({"incident_id": "A", "action": "CREATE"})
    stack.push({"incident_id": "A", "action": "UPDATE_STATUS", "status": "IN_PROGRESS"})
    
    assert stack.size() == 2
    
    top = stack.peek()
    assert top is not None
    assert top["action"] == "UPDATE_STATUS"
    assert stack.size() == 2
    
    popped = stack.pop()
    assert popped is not None
    assert popped["action"] == "UPDATE_STATUS"
    assert stack.size() == 1
    
    popped2 = stack.pop()
    assert popped2 is not None
    assert popped2["action"] == "CREATE"
    assert stack.is_empty()
    
    assert stack.pop() is None

def test_category_tree():
    tree = CategoryTree()
    
    # Add categories
    assert tree.add_category("Technology") is True
    assert tree.add_category("Facilities") is True
    assert tree.add_category("Software", parent_name="Technology") is True
    assert tree.add_category("Hardware", parent_name="Technology") is True
    assert tree.add_category("Plumbing", parent_name="Facilities") is True
    
    # Test invalid parent
    assert tree.add_category("Desks", parent_name="NonExistent") is False
    
    # Test duplicate
    assert tree.add_category("Technology") is False
    
    # Test subcategories
    tech_subs = tree.get_subcategories("Technology")
    assert len(tech_subs) == 2
    assert "Software" in tech_subs
    assert "Hardware" in tech_subs
    
    fac_subs = tree.get_subcategories("Facilities")
    assert len(fac_subs) == 1
    assert "Plumbing" in fac_subs
    
    # Test non-existent category subcategories
    assert tree.get_subcategories("AlienTech") == []
    
    # Test all categories dict
    all_cats = tree.get_all_categories()
    assert all_cats["name"] == "Root"
    assert len(all_cats["children"]) == 2
    names = [child["name"] for child in all_cats["children"]]
    assert "Technology" in names
    assert "Facilities" in names
