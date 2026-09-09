/* Comprehensive Problems Dataset */

export const mockProblems = [
  {
    id: 'prob_1',
    title: 'Two Sum (Python Solution)',
    difficulty: 'Easy',
    category: 'Algorithms',
    topic: 'Array & Hash Map',
    acceptanceRate: '49.2%',
    solvedCount: 12450,
    likes: 8520,
    description: `Given an array of integers \`nums\` and an integer \`target\`, return indices of the two numbers such that they add up to \`target\`.

You may assume that each input would have **exactly one solution**, and you may not use the same element twice.

You can return the answer in any order.`,
    examples: [
      {
        input: 'nums = [2,7,11,15], target = 9',
        output: '[0,1]',
        explanation: 'Because nums[0] + nums[1] == 9, we return [0, 1].'
      },
      {
        input: 'nums = [3,2,4], target = 6',
        output: '[1,2]',
        explanation: 'Because nums[1] + nums[2] == 6, we return [1, 2].'
      }
    ],
    constraints: [
      '2 <= nums.length <= 10^4',
      '-10^9 <= nums[i] <= 10^9',
      '-10^9 <= target <= 10^9',
      'Only one valid answer exists.'
    ],
    hints: [
      'A really brute force way would be to search for all possible pairs, which is O(N^2).',
      'Can we use a Python dictionary (Hash Map) to check complement presence in O(1) time?'
    ],
    starterCode: {
      python: `def two_sum(nums, target):\n    # Write your Python solution here\n    seen = {}\n    for i, num in enumerate(nums):\n        diff = target - num\n        if diff in seen:\n            return [seen[diff], i]\n        seen[num] = i\n    return []\n\n# Driver Code\nnums = [2, 7, 11, 15]\ntarget = 9\nprint(two_sum(nums, target))`,
      cpp: `#include <iostream>\n#include <vector>\n#include <unordered_map>\nusing namespace std;\n\nvector<int> twoSum(vector<int>& nums, int target) {\n    unordered_map<int, int> mp;\n    for (int i = 0; i < nums.size(); i++) {\n        int diff = target - nums[i];\n        if (mp.count(diff)) return {mp[diff], i};\n        mp[nums[i]] = i;\n    }\n    return {};\n}\n\nint main() {\n    cout << "[0, 1]" << endl;\n    return 0;\n}`,
      java: `import java.util.*;\n\npublic class Solution {\n    public static int[] twoSum(int[] nums, int target) {\n        Map<Integer, Integer> map = new HashMap<>();\n        for (int i = 0; i < nums.length; i++) {\n            int complement = target - nums[i];\n            if (map.containsKey(complement)) {\n                return new int[] { map.get(complement), i };\n            }\n            map.put(nums[i], i);\n        }\n        return new int[]{};\n    }\n    public static void main(String[] args) {\n        System.out.println("[0, 1]");\n    }\n}`,
      javascript: `function twoSum(nums, target) {\n    const map = new Map();\n    for (let i = 0; i < nums.length; i++) {\n        const diff = target - nums[i];\n        if (map.has(diff)) return [map.get(diff), i];\n        map.set(nums[i], i);\n    }\n    return [];\n}\n\nconsole.log(twoSum([2, 7, 11, 15], 9));`
    }
  },

  {
    id: 'prob_2',
    title: 'Valid Parentheses String (Python)',
    difficulty: 'Medium',
    category: 'Data Structures',
    topic: 'Stack & String',
    acceptanceRate: '41.5%',
    solvedCount: 8900,
    likes: 6200,
    description: `Given a string \`s\` containing just the characters \`'('\`, \`')'\`, \`'{'\`, \`'}'\`, \`'['\` and \`']'\`, determine if the input string is valid.

An input string is valid if:
1. Open brackets must be closed by the same type of brackets.
2. Open brackets must be closed in the correct order.
3. Every close bracket has a corresponding open bracket of the same type.`,
    examples: [
      { input: 's = "()"', output: 'true' },
      { input: 's = "()[]{}"', output: 'true' },
      { input: 's = "(]"', output: 'false' }
    ],
    constraints: [
      '1 <= s.length <= 10^4',
      's consists of parentheses only \'()[]{}\'.'
    ],
    hints: [
      'Use a stack to keep track of opening brackets.',
      'When encountering a closing bracket, pop from the stack and verify matching bracket types.'
    ],
    starterCode: {
      python: `def is_valid(s: str) -> bool:\n    stack = []\n    mapping = {")": "(", "}": "{", "]": "["}\n    for char in s:\n        if char in mapping:\n            top = stack.pop() if stack else '#'\n            if mapping[char] != top:\n                return False\n        else:\n            stack.append(char)\n    return not stack\n\n# Test\nprint(is_valid("()[]{}"))`
    }
  },

  {
    id: 'prob_3',
    title: 'Binary Tree Level Order Traversal (Python)',
    difficulty: 'Medium',
    category: 'Data Structures',
    topic: 'Trees & BFS',
    acceptanceRate: '63.8%',
    solvedCount: 7100,
    likes: 5400,
    description: `Given the root of a binary tree, return the level order traversal of its nodes' values. (i.e., from left to right, level by level).`,
    examples: [
      { input: 'root = [3,9,20,null,null,15,7]', output: '[[3],[9,20],[15,7]]' }
    ],
    constraints: [
      'The number of nodes in the tree is in the range [0, 2000].',
      '-1000 <= Node.val <= 1000'
    ],
    hints: [
      'A Queue (collections.deque in Python) is ideal for Breadth-First Search (BFS).'
    ],
    starterCode: {
      python: `from collections import deque\n\nclass TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\ndef level_order(root):\n    if not root: return []\n    result, queue = [], deque([root])\n    while queue:\n        level = []\n        for _ in range(len(queue)):\n            node = queue.popleft()\n            level.append(node.val)\n            if node.left: queue.append(node.left)\n            if node.right: queue.append(node.right)\n        result.append(level)\n    return result\n\n# Test\nroot = TreeNode(3, TreeNode(9), TreeNode(20, TreeNode(15), TreeNode(7)))\nprint(level_order(root))`
    }
  },

  {
    id: 'prob_4',
    title: 'Merge K Sorted Lists (Python)',
    difficulty: 'Hard',
    category: 'Algorithms',
    topic: 'Heap & Linked List',
    acceptanceRate: '50.1%',
    solvedCount: 4300,
    likes: 7100,
    description: `You are given an array of \`k\` linked-lists \`lists\`, each linked-list is sorted in ascending order. Merge all the linked-lists into one sorted linked-list and return it.`,
    examples: [
      { input: 'lists = [[1,4,5],[1,3,4],[2,6]]', output: '[1,1,2,3,4,4,5,6]' }
    ],
    constraints: [
      'k == lists.length',
      '0 <= k <= 10^4',
      '0 <= lists[i].length <= 500'
    ],
    hints: [
      'Use Python\'s min-heap module (\`heapq\`) to retrieve the smallest element across all k lists efficiently.'
    ],
    starterCode: {
      python: `import heapq\n\nclass ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\ndef merge_k_lists(lists):\n    min_heap = []\n    for idx, node in enumerate(lists):\n        if node:\n            heapq.heappush(min_heap, (node.val, idx, node))\n    \n    dummy = ListNode(0)\n    curr = dummy\n    while min_heap:\n        val, idx, node = heapq.heappop(min_heap)\n        curr.next = node\n        curr = curr.next\n        if node.next:\n            heapq.heappush(min_heap, (node.next.val, idx, node.next))\n    return dummy.next\n\nprint("Merged K Lists ready")`
    }
  }
];
