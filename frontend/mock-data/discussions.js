/* Mock Community Discussions Dataset */

export const mockDiscussions = [
  {
    id: 'disc_1',
    title: 'How to optimize Python dictionary lookups for Two Sum in O(N)?',
    category: 'Algorithms',
    author: 'dev_newbie',
    authorAvatar: 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=100&auto=format&fit=crop&q=80',
    createdAt: '2026-09-08T14:30:00Z',
    upvotes: 42,
    repliesCount: 8,
    tags: ['python', 'hash-map', 'dsa'],
    content: `I tried solving Two Sum using double nested loops in Python, but it timed out on large arrays. How does a Python hash map improve this to O(N)?`,
    replies: [
      {
        id: 'r_1',
        author: 'alex_dev',
        createdAt: '2026-09-08T15:10:00Z',
        upvotes: 19,
        content: `By storing visited numbers as keys in a dictionary \`seen[num] = i\`, you can check if \`target - num\` exists in O(1) average time!`
      }
    ]
  },
  {
    id: 'disc_2',
    title: 'Best Python practices for writing clean asynchronous APIs',
    category: 'Python',
    author: 'py_guru',
    authorAvatar: 'https://images.unsplash.com/photo-1570295999919-56ceb5ecca61?w=100&auto=format&fit=crop&q=80',
    createdAt: '2026-09-07T11:00:00Z',
    upvotes: 89,
    repliesCount: 15,
    tags: ['python', 'asyncio', 'architecture'],
    content: `When building high concurrency services in Python, using \`asyncio\` and task pools prevents thread blocking on I/O operations.`
  }
];
