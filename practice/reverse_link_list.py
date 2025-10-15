class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def make_list_to_linked_list(arr):
    head = ListNode(arr[0])
    current = head
    for val in arr[1:]:
        current.next = ListNode(val)
        current = current.next
    return head


def print_linked_list(head):
    current = head
    while current:
        print(current.val)
        current = current.next

def reverse_linked_list(head):
    prev, cur = None, head
    while cur:
        next = cur.next
        cur.next = prev
        prev, cur = cur, next
    return prev


arr = [1, 2, 3, 4, 5]
head = make_list_to_linked_list(arr)
print_linked_list(head)
print("Reversed Linked List")
prev = reverse_linked_list(head)
print_linked_list(prev)
