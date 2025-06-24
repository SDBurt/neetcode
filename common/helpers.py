from typing import List, Optional

# Definition for singly-linked list, as provided by LeetCode.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    def __repr__(self):
        return f"ListNode({self.val}, next={self.next.val if self.next else None})"

    def __eq__(self, other):
        if not isinstance(other, ListNode):
            return False
        
        l1 = self
        l2 = other
        while l1 and l2:
            if l1.val != l2.val:
                return False
            l1 = l1.next
            l2 = l2.next
        
        return l1 is None and l2 is None


def create_linked_list(items: List) -> Optional[ListNode]:
    """Creates a ListNode chain from a Python list."""
    if not items:
        return None
    
    head = ListNode(items[0])
    current = head
    for item in items[1:]:
        current.next = ListNode(item)
        current = current.next
        
    return head

def linked_list_to_list(head: Optional[ListNode]) -> List:
    """Converts a ListNode chain back to a Python list."""
    items = []
    current = head
    while current:
        items.append(current.val)
        current = current.next
    return items 