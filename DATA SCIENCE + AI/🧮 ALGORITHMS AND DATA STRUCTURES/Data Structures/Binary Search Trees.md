# Binary Search Trees

> Ordered binary tree data structure where left child < parent < right child, enabling efficient search, insertion, and deletion operations.

## 📖 Definition

A Binary Search Tree (BST) is a binary tree that satisfies the BST property:
- All nodes in left subtree < current node
- All nodes in right subtree > current node  
- Both subtrees are also BSTs

## ⚡ Time Complexity

| Operation | Average | Worst Case |
|-----------|---------|------------|
| **Search** | O(log n) | O(n) |
| **Insert** | O(log n) | O(n) |
| **Delete** | O(log n) | O(n) |
| **Traversal** | O(n) | O(n) |

*Worst case occurs in unbalanced tree (becomes linear)*

## 🐍 Python Implementation

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class BST:
    def __init__(self):
        self.root = None
    
    def insert(self, val):
        """Insert value into BST"""
        self.root = self._insert_recursive(self.root, val)
    
    def _insert_recursive(self, node, val):
        if not node:
            return TreeNode(val)
        
        if val < node.val:
            node.left = self._insert_recursive(node.left, val)
        elif val > node.val:
            node.right = self._insert_recursive(node.right, val)
        
        return node
    
    def search(self, val):
        """Search for value in BST"""
        return self._search_recursive(self.root, val)
    
    def _search_recursive(self, node, val):
        if not node or node.val == val:
            return node
        
        if val < node.val:
            return self._search_recursive(node.left, val)
        else:
            return self._search_recursive(node.right, val)
    
    def delete(self, val):
        """Delete value from BST"""
        self.root = self._delete_recursive(self.root, val)
    
    def _delete_recursive(self, node, val):
        if not node:
            return node
        
        if val < node.val:
            node.left = self._delete_recursive(node.left, val)
        elif val > node.val:
            node.right = self._delete_recursive(node.right, val)
        else:
            # Node to be deleted found
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            
            # Node has two children - find inorder successor
            min_node = self._find_min(node.right)
            node.val = min_node.val
            node.right = self._delete_recursive(node.right, min_node.val)
        
        return node
    
    def _find_min(self, node):
        """Find minimum value node in subtree"""
        current = node
        while current.left:
            current = current.left
        return current
    
    def inorder(self):
        """Inorder traversal - returns sorted order"""
        result = []
        self._inorder_recursive(self.root, result)
        return result
    
    def _inorder_recursive(self, node, result):
        if node:
            self._inorder_recursive(node.left, result)
            result.append(node.val)
            self._inorder_recursive(node.right, result)
    
    def find_min(self):
        """Find minimum value in BST"""
        if not self.root:
            return None
        return self._find_min(self.root).val
    
    def find_max(self):
        """Find maximum value in BST"""
        if not self.root:
            return None
        
        current = self.root
        while current.right:
            current = current.right
        return current.val
    
    def is_valid_bst(self):
        """Check if tree is valid BST"""
        return self._is_valid_bst_helper(self.root, float('-inf'), float('inf'))
    
    def _is_valid_bst_helper(self, node, min_val, max_val):
        if not node:
            return True
        
        if node.val <= min_val or node.val >= max_val:
            return False
        
        return (self._is_valid_bst_helper(node.left, min_val, node.val) and
                self._is_valid_bst_helper(node.right, node.val, max_val))
```

## 🎯 Applications

1. **Database Indexing**: B-trees (variant of BST)
2. **Expression Parsing**: Operator precedence
3. **File Systems**: Directory structures
4. **Priority Queues**: Binary heaps
5. **Auto-complete**: Trie structures

## 🔗 Related Topics

- [[Binary Trees]] - General tree structure
- [[AVL Trees]] - Self-balancing BST
- [[Heaps]] - Complete binary trees
- [[Graphs]] - General graph structures

---

*See also: [[Binary Trees]], [[AVL Trees]], [[Heaps]], [[algorithms_and_ds]]*