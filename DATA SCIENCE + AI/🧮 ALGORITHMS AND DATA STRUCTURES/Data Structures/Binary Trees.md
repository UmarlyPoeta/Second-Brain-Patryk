# Binary Trees

> Hierarchical data structure where each node has at most two children, referred to as left and right child. Forms the foundation for many advanced tree structures.

## 📖 Definition

A binary tree is a tree data structure in which each node has at most two children. The topmost node is called the root, and nodes with no children are called leaves.

## 🌳 Tree Terminology

- **Root**: Top node of the tree
- **Parent**: Node that has children
- **Child**: Node connected below another node
- **Leaf**: Node with no children
- **Height**: Length of longest path from node to leaf
- **Depth**: Length of path from root to node
- **Level**: All nodes at same depth

## 🔢 Types of Binary Trees

### 1. Full Binary Tree
Every node has either 0 or 2 children.

### 2. Complete Binary Tree
All levels filled except possibly the last, which is filled left to right.

### 3. Perfect Binary Tree
All internal nodes have two children and all leaves are at same level.

### 4. Balanced Binary Tree
Height difference between left and right subtrees ≤ 1 for all nodes.

## 🐍 Python Implementation

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
    
    def __str__(self):
        return str(self.val)

class BinaryTree:
    def __init__(self, root=None):
        self.root = root
    
    # Tree Traversals
    def inorder(self, node=None, result=None):
        """Left -> Root -> Right (gives sorted order for BST)"""
        if result is None:
            result = []
        if node is None:
            node = self.root
        
        if node:
            self.inorder(node.left, result)
            result.append(node.val)
            self.inorder(node.right, result)
        return result
    
    def preorder(self, node=None, result=None):
        """Root -> Left -> Right (good for copying tree)"""
        if result is None:
            result = []
        if node is None:
            node = self.root
        
        if node:
            result.append(node.val)
            self.preorder(node.left, result)
            self.preorder(node.right, result)
        return result
    
    def postorder(self, node=None, result=None):
        """Left -> Right -> Root (good for deleting tree)"""
        if result is None:
            result = []
        if node is None:
            node = self.root
        
        if node:
            self.postorder(node.left, result)
            self.postorder(node.right, result)
            result.append(node.val)
        return result
    
    def level_order(self):
        """Breadth-First Traversal using queue"""
        if not self.root:
            return []
        
        from collections import deque
        result = []
        queue = deque([self.root])
        
        while queue:
            node = queue.popleft()
            result.append(node.val)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        return result
    
    def height(self, node=None):
        """Calculate height of tree - O(n)"""
        if node is None:
            node = self.root
        if not node:
            return -1
        
        return 1 + max(self.height(node.left), self.height(node.right))
    
    def size(self, node=None):
        """Count total nodes - O(n)"""
        if node is None:
            node = self.root
        if not node:
            return 0
        
        return 1 + self.size(node.left) + self.size(node.right)
    
    def is_balanced(self, node=None):
        """Check if tree is balanced - O(n)"""
        if node is None:
            node = self.root
        
        def check_balance(node):
            if not node:
                return 0, True
            
            left_height, left_balanced = check_balance(node.left)
            right_height, right_balanced = check_balance(node.right)
            
            balanced = (left_balanced and right_balanced and 
                       abs(left_height - right_height) <= 1)
            height = 1 + max(left_height, right_height)
            
            return height, balanced
        
        _, balanced = check_balance(node)
        return balanced
    
    def insert_level_order(self, val):
        """Insert node in level order (complete tree)"""
        new_node = TreeNode(val)
        
        if not self.root:
            self.root = new_node
            return
        
        from collections import deque
        queue = deque([self.root])
        
        while queue:
            node = queue.popleft()
            
            if not node.left:
                node.left = new_node
                return
            elif not node.right:
                node.right = new_node
                return
            else:
                queue.append(node.left)
                queue.append(node.right)
    
    def search(self, val, node=None):
        """Search for value in tree - O(n)"""
        if node is None:
            node = self.root
        if not node:
            return False
        
        if node.val == val:
            return True
        
        return self.search(val, node.left) or self.search(val, node.right)
    
    def print_tree(self, node=None, level=0, prefix="Root: "):
        """Pretty print tree structure"""
        if node is None:
            node = self.root
        if node:
            print(" " * (level * 4) + prefix + str(node.val))
            if node.left or node.right:
                if node.left:
                    self.print_tree(node.left, level + 1, "L--- ")
                else:
                    print(" " * ((level + 1) * 4) + "L--- None")
                if node.right:
                    self.print_tree(node.right, level + 1, "R--- ")
                else:
                    print(" " * ((level + 1) * 4) + "R--- None")

# Example usage
def create_example_tree():
    """
    Create example tree:
           1
          / \\
         2   3
        / \\
       4   5
    """
    tree = BinaryTree()
    tree.root = TreeNode(1)
    tree.root.left = TreeNode(2)
    tree.root.right = TreeNode(3)
    tree.root.left.left = TreeNode(4)
    tree.root.left.right = TreeNode(5)
    return tree
```

## ☕ Java Implementation

```java
import java.util.*;

class TreeNode {
    int val;
    TreeNode left;
    TreeNode right;
    
    TreeNode() {}
    TreeNode(int val) { this.val = val; }
    TreeNode(int val, TreeNode left, TreeNode right) {
        this.val = val;
        this.left = left;
        this.right = right;
    }
}

public class BinaryTree {
    private TreeNode root;
    
    public BinaryTree() {
        this.root = null;
    }
    
    public BinaryTree(TreeNode root) {
        this.root = root;
    }
    
    // Recursive traversals
    public List<Integer> inorderTraversal() {
        List<Integer> result = new ArrayList<>();
        inorderHelper(root, result);
        return result;
    }
    
    private void inorderHelper(TreeNode node, List<Integer> result) {
        if (node != null) {
            inorderHelper(node.left, result);
            result.add(node.val);
            inorderHelper(node.right, result);
        }
    }
    
    public List<Integer> preorderTraversal() {
        List<Integer> result = new ArrayList<>();
        preorderHelper(root, result);
        return result;
    }
    
    private void preorderHelper(TreeNode node, List<Integer> result) {
        if (node != null) {
            result.add(node.val);
            preorderHelper(node.left, result);
            preorderHelper(node.right, result);
        }
    }
    
    public List<Integer> postorderTraversal() {
        List<Integer> result = new ArrayList<>();
        postorderHelper(root, result);
        return result;
    }
    
    private void postorderHelper(TreeNode node, List<Integer> result) {
        if (node != null) {
            postorderHelper(node.left, result);
            postorderHelper(node.right, result);
            result.add(node.val);
        }
    }
    
    // Iterative level order traversal
    public List<Integer> levelOrder() {
        List<Integer> result = new ArrayList<>();
        if (root == null) return result;
        
        Queue<TreeNode> queue = new LinkedList<>();
        queue.offer(root);
        
        while (!queue.isEmpty()) {
            TreeNode node = queue.poll();
            result.add(node.val);
            
            if (node.left != null) queue.offer(node.left);
            if (node.right != null) queue.offer(node.right);
        }
        
        return result;
    }
    
    // Tree properties
    public int height() {
        return height(root);
    }
    
    private int height(TreeNode node) {
        if (node == null) return -1;
        return 1 + Math.max(height(node.left), height(node.right));
    }
    
    public int size() {
        return size(root);
    }
    
    private int size(TreeNode node) {
        if (node == null) return 0;
        return 1 + size(node.left) + size(node.right);
    }
    
    public boolean isBalanced() {
        return isBalanced(root) != -1;
    }
    
    private int isBalanced(TreeNode node) {
        if (node == null) return 0;
        
        int leftHeight = isBalanced(node.left);
        if (leftHeight == -1) return -1;
        
        int rightHeight = isBalanced(node.right);
        if (rightHeight == -1) return -1;
        
        if (Math.abs(leftHeight - rightHeight) > 1) return -1;
        
        return Math.max(leftHeight, rightHeight) + 1;
    }
    
    public boolean search(int val) {
        return search(root, val);
    }
    
    private boolean search(TreeNode node, int val) {
        if (node == null) return false;
        if (node.val == val) return true;
        return search(node.left, val) || search(node.right, val);
    }
    
    public void insertLevelOrder(int val) {
        if (root == null) {
            root = new TreeNode(val);
            return;
        }
        
        Queue<TreeNode> queue = new LinkedList<>();
        queue.offer(root);
        
        while (!queue.isEmpty()) {
            TreeNode node = queue.poll();
            
            if (node.left == null) {
                node.left = new TreeNode(val);
                return;
            } else if (node.right == null) {
                node.right = new TreeNode(val);
                return;
            } else {
                queue.offer(node.left);
                queue.offer(node.right);
            }
        }
    }
    
    // Getters and setters
    public TreeNode getRoot() { return root; }
    public void setRoot(TreeNode root) { this.root = root; }
}
```

## ⚡ C++ Implementation

```cpp
#include <iostream>
#include <vector>
#include <queue>
#include <algorithm>

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    
    TreeNode() : val(0), left(nullptr), right(nullptr) {}
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
    TreeNode(int x, TreeNode* left, TreeNode* right) : val(x), left(left), right(right) {}
};

class BinaryTree {
private:
    TreeNode* root;
    
    void destroyTree(TreeNode* node) {
        if (node) {
            destroyTree(node->left);
            destroyTree(node->right);
            delete node;
        }
    }
    
    void inorderHelper(TreeNode* node, std::vector<int>& result) {
        if (node) {
            inorderHelper(node->left, result);
            result.push_back(node->val);
            inorderHelper(node->right, result);
        }
    }
    
    void preorderHelper(TreeNode* node, std::vector<int>& result) {
        if (node) {
            result.push_back(node->val);
            preorderHelper(node->left, result);
            preorderHelper(node->right, result);
        }
    }
    
    void postorderHelper(TreeNode* node, std::vector<int>& result) {
        if (node) {
            postorderHelper(node->left, result);
            postorderHelper(node->right, result);
            result.push_back(node->val);
        }
    }
    
public:
    BinaryTree() : root(nullptr) {}
    
    BinaryTree(TreeNode* root) : root(root) {}
    
    ~BinaryTree() {
        destroyTree(root);
    }
    
    // Traversals
    std::vector<int> inorderTraversal() {
        std::vector<int> result;
        inorderHelper(root, result);
        return result;
    }
    
    std::vector<int> preorderTraversal() {
        std::vector<int> result;
        preorderHelper(root, result);
        return result;
    }
    
    std::vector<int> postorderTraversal() {
        std::vector<int> result;
        postorderHelper(root, result);
        return result;
    }
    
    std::vector<int> levelOrder() {
        std::vector<int> result;
        if (!root) return result;
        
        std::queue<TreeNode*> q;
        q.push(root);
        
        while (!q.empty()) {
            TreeNode* node = q.front();
            q.pop();
            result.push_back(node->val);
            
            if (node->left) q.push(node->left);
            if (node->right) q.push(node->right);
        }
        
        return result;
    }
    
    // Tree properties
    int height() {
        return height(root);
    }
    
    int height(TreeNode* node) {
        if (!node) return -1;
        return 1 + std::max(height(node->left), height(node->right));
    }
    
    int size() {
        return size(root);
    }
    
    int size(TreeNode* node) {
        if (!node) return 0;
        return 1 + size(node->left) + size(node->right);
    }
    
    bool isBalanced() {
        return checkBalance(root).second;
    }
    
    std::pair<int, bool> checkBalance(TreeNode* node) {
        if (!node) return {0, true};
        
        auto left = checkBalance(node->left);
        auto right = checkBalance(node->right);
        
        bool balanced = left.second && right.second && 
                       abs(left.first - right.first) <= 1;
        int height = 1 + std::max(left.first, right.first);
        
        return {height, balanced};
    }
    
    bool search(int val) {
        return search(root, val);
    }
    
    bool search(TreeNode* node, int val) {
        if (!node) return false;
        if (node->val == val) return true;
        return search(node->left, val) || search(node->right, val);
    }
    
    void insertLevelOrder(int val) {
        if (!root) {
            root = new TreeNode(val);
            return;
        }
        
        std::queue<TreeNode*> q;
        q.push(root);
        
        while (!q.empty()) {
            TreeNode* node = q.front();
            q.pop();
            
            if (!node->left) {
                node->left = new TreeNode(val);
                return;
            } else if (!node->right) {
                node->right = new TreeNode(val);
                return;
            } else {
                q.push(node->left);
                q.push(node->right);
            }
        }
    }
    
    TreeNode* getRoot() { return root; }
    void setRoot(TreeNode* newRoot) { root = newRoot; }
};
```

## 🔄 Tree Traversals

| Traversal | Order | Use Case |
|-----------|--------|----------|
| **Inorder** | Left → Root → Right | Get sorted order in BST |
| **Preorder** | Root → Left → Right | Copy/serialize tree |
| **Postorder** | Left → Right → Root | Delete tree safely |
| **Level Order** | Level by level | Print by levels |

## ⚡ Time Complexity

| Operation | Average | Worst Case |
|-----------|---------|------------|
| Search | O(log n) | O(n) |
| Insertion | O(log n) | O(n) |
| Deletion | O(log n) | O(n) |
| Traversal | O(n) | O(n) |
| Height | O(n) | O(n) |

## 🎯 Applications

### 1. Expression Trees
```python
# Build expression tree for (a + b) * c
class ExprNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

def evaluate_expression_tree(root):
    if not root:
        return 0
    
    # Leaf node (operand)
    if not root.left and not root.right:
        return float(root.val)
    
    # Internal node (operator)
    left_val = evaluate_expression_tree(root.left)
    right_val = evaluate_expression_tree(root.right)
    
    if root.val == '+':
        return left_val + right_val
    elif root.val == '-':
        return left_val - right_val
    elif root.val == '*':
        return left_val * right_val
    elif root.val == '/':
        return left_val / right_val
```

### 2. Decision Trees
```python
class DecisionNode:
    def __init__(self, feature=None, threshold=None, value=None):
        self.feature = feature      # Feature to split on
        self.threshold = threshold  # Split threshold
        self.value = value         # Prediction value (for leaf)
        self.left = None           # Left child
        self.right = None          # Right child
    
    def is_leaf(self):
        return self.value is not None
```

## 🔗 Related Topics

- [[Binary Search Trees]] - Ordered binary trees
- [[AVL Trees]] - Self-balancing binary trees
- [[Heaps]] - Complete binary trees with heap property
- [[Graphs]] - Generalization of trees

## 💡 Tips and Best Practices

1. **Recursive thinking**: Most tree operations are naturally recursive
2. **Base case**: Always handle null/empty nodes
3. **Memory management**: Important in C++ to avoid memory leaks
4. **Balanced trees**: Consider self-balancing variants for guaranteed performance
5. **Traversal choice**: Pick appropriate traversal for your use case

## 📝 Practice Problems

1. **Maximum Depth**: Find maximum depth of binary tree
2. **Same Tree**: Check if two trees are identical
3. **Symmetric Tree**: Check if tree is symmetric
4. **Path Sum**: Check if path from root to leaf sums to target
5. **Level Order Traversal II**: Bottom-up level order traversal
6. **Binary Tree Zigzag Level Order**: Alternate left-to-right traversal
7. **Lowest Common Ancestor**: Find LCA of two nodes
8. **Serialize/Deserialize**: Convert tree to string and back

---

*See also: [[Binary Search Trees]], [[AVL Trees]], [[Heaps]], [[algorithms_and_ds]]*