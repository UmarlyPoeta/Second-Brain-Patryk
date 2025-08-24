# AVL Trees

> Self-balancing binary search tree where the height difference between left and right subtrees cannot be more than one for all nodes.

## 📖 Definition

AVL (Adelson-Velsky and Landis) trees are self-balancing binary search trees. In an AVL tree, the heights of the two child subtrees of any node differ by at most one. If at any time they differ by more than one, rebalancing is done to restore this property.

## 🔑 Key Properties

- **Height Balance**: |height(left) - height(right)| ≤ 1 for every node
- **BST Property**: Left subtree < node < right subtree
- **Self-Balancing**: Automatically maintains balance through rotations
- **Guaranteed Height**: O(log n) height ensures O(log n) operations

## ⚡ Time & Space Complexity

- **Search**: O(log n)
- **Insert**: O(log n)
- **Delete**: O(log n)
- **Space**: O(n)

## 🔄 Rotation Operations

### Single Rotations
- **Left Rotation**: When right subtree is heavier
- **Right Rotation**: When left subtree is heavier

### Double Rotations
- **Left-Right Rotation**: Left child has heavy right subtree
- **Right-Left Rotation**: Right child has heavy left subtree

## 🐍 Python Implementation

```python
class AVLNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def get_height(self, node):
        if not node:
            return 0
        return node.height
    
    def get_balance(self, node):
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)
    
    def update_height(self, node):
        if node:
            node.height = 1 + max(self.get_height(node.left), 
                                 self.get_height(node.right))
    
    def right_rotate(self, y):
        x = y.left
        T2 = x.right
        
        # Perform rotation
        x.right = y
        y.left = T2
        
        # Update heights
        self.update_height(y)
        self.update_height(x)
        
        return x
    
    def left_rotate(self, x):
        y = x.right
        T2 = y.left
        
        # Perform rotation
        y.left = x
        x.right = T2
        
        # Update heights
        self.update_height(x)
        self.update_height(y)
        
        return y
    
    def insert(self, root, data):
        # Step 1: Perform normal BST insertion
        if not root:
            return AVLNode(data)
        
        if data < root.data:
            root.left = self.insert(root.left, data)
        elif data > root.data:
            root.right = self.insert(root.right, data)
        else:
            return root  # Duplicate keys not allowed
        
        # Step 2: Update height
        self.update_height(root)
        
        # Step 3: Get balance factor
        balance = self.get_balance(root)
        
        # Step 4: Rebalance if needed
        # Left Left Case
        if balance > 1 and data < root.left.data:
            return self.right_rotate(root)
        
        # Right Right Case
        if balance < -1 and data > root.right.data:
            return self.left_rotate(root)
        
        # Left Right Case
        if balance > 1 and data > root.left.data:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
        
        # Right Left Case
        if balance < -1 and data < root.right.data:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)
        
        return root
```

## ☕ Java Implementation

```java
class AVLNode {
    int data, height;
    AVLNode left, right;
    
    AVLNode(int data) {
        this.data = data;
        this.height = 1;
    }
}

public class AVLTree {
    
    int getHeight(AVLNode node) {
        return node == null ? 0 : node.height;
    }
    
    int getBalance(AVLNode node) {
        return node == null ? 0 : getHeight(node.left) - getHeight(node.right);
    }
    
    void updateHeight(AVLNode node) {
        if (node != null) {
            node.height = 1 + Math.max(getHeight(node.left), getHeight(node.right));
        }
    }
    
    AVLNode rightRotate(AVLNode y) {
        AVLNode x = y.left;
        AVLNode T2 = x.right;
        
        // Perform rotation
        x.right = y;
        y.left = T2;
        
        // Update heights
        updateHeight(y);
        updateHeight(x);
        
        return x;
    }
    
    AVLNode leftRotate(AVLNode x) {
        AVLNode y = x.right;
        AVLNode T2 = y.left;
        
        // Perform rotation
        y.left = x;
        x.right = T2;
        
        // Update heights
        updateHeight(x);
        updateHeight(y);
        
        return y;
    }
    
    AVLNode insert(AVLNode node, int data) {
        // Step 1: BST insertion
        if (node == null) return new AVLNode(data);
        
        if (data < node.data)
            node.left = insert(node.left, data);
        else if (data > node.data)
            node.right = insert(node.right, data);
        else
            return node; // Duplicates not allowed
        
        // Step 2: Update height
        updateHeight(node);
        
        // Step 3: Get balance
        int balance = getBalance(node);
        
        // Step 4: Rebalance
        // Left Left Case
        if (balance > 1 && data < node.left.data)
            return rightRotate(node);
        
        // Right Right Case
        if (balance < -1 && data > node.right.data)
            return leftRotate(node);
        
        // Left Right Case
        if (balance > 1 && data > node.left.data) {
            node.left = leftRotate(node.left);
            return rightRotate(node);
        }
        
        // Right Left Case
        if (balance < -1 && data < node.right.data) {
            node.right = rightRotate(node.right);
            return leftRotate(node);
        }
        
        return node;
    }
}
```

## 🎯 Applications

1. **Database Indexing**: Maintain sorted indices efficiently
2. **Memory Management**: Balanced allocation trees
3. **File Systems**: Directory structures
4. **Real-time Systems**: Guaranteed O(log n) performance

## 🆚 AVL vs Other Trees

| Tree Type | Insert | Search | Delete | Balance | Space |
|-----------|--------|--------|--------|---------|-------|
| **AVL Tree** | O(log n) | O(log n) | O(log n) | Strict | O(n) |
| **Red-Black** | O(log n) | O(log n) | O(log n) | Relaxed | O(n) |
| **BST** | O(n) | O(n) | O(n) | None | O(n) |
| **Splay Tree** | O(log n)* | O(log n)* | O(log n)* | Self-adjusting | O(n) |

*Amortized time complexity

## 🔗 Related Topics

- [[Binary Search Trees]] - Foundation for AVL trees
- [[Binary Trees]] - Basic tree structure
- [[Hash Tables]] - Alternative for fast lookups
- [[Red-Black Trees]] - Another self-balancing BST

---

*See also: [[Binary Search Trees]], [[Binary Trees]], [[algorithms_and_ds]]*