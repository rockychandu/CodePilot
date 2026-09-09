/* Mock Courses Dataset */

export const mockCourses = [
  {
    id: 'course_1',
    title: 'Python Core Mastery & Backend Systems',
    category: 'Python',
    difficulty: 'Beginner to Advanced',
    instructor: 'Guido van Rossum (Guest Lead)',
    rating: 4.9,
    studentsCount: 14200,
    lessonsCount: 24,
    duration: '18h 45m',
    progress: 65,
    thumbnail: 'https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=400&auto=format&fit=crop&q=80',
    description: 'Master Python syntax, object-oriented programming, async I/O, data structures, and building API servers with Python Flask/FastAPI.',
    lessons: [
      { id: 'l1', title: '1. Python Syntax & Control Flow', type: 'video', duration: '25m', completed: true },
      { id: 'l2', title: '2. Lists, Dicts, and Hash Sets', type: 'video', duration: '35m', completed: true },
      { id: 'l3', title: '3. Python OOP & Magic Methods', type: 'pdf', duration: '15m', completed: true },
      { id: 'l4', title: '4. Memory Management & Garbage Collection', type: 'pdf', duration: '20m', completed: false },
      { id: 'l5', title: '5. Building REST APIs with Python', type: 'video', duration: '45m', completed: false }
    ]
  },

  {
    id: 'course_2',
    title: 'Data Structures & Algorithms with Python',
    category: 'DSA',
    difficulty: 'Intermediate',
    instructor: 'Dr. Evelyn Reed',
    rating: 4.8,
    studentsCount: 9800,
    lessonsCount: 32,
    duration: '26h 10m',
    progress: 40,
    thumbnail: 'https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=400&auto=format&fit=crop&q=80',
    description: 'Comprehensive guide to solving FAANG-level DSA problems using clean Python code.',
    lessons: [
      { id: 'l201', title: '1. Time & Space Complexity Analysis', type: 'video', duration: '30m', completed: true },
      { id: 'l202', title: '2. Two Pointers & Sliding Window', type: 'video', duration: '40m', completed: true },
      { id: 'l203', title: '3. Trees & Graph Traversals in Python', type: 'pdf', duration: '25m', completed: false }
    ]
  },

  {
    id: 'course_3',
    title: 'AI & Machine Learning Engineering in Python',
    category: 'AI/ML',
    difficulty: 'Advanced',
    instructor: 'Prof. Marcus Vance',
    rating: 4.95,
    studentsCount: 6300,
    lessonsCount: 28,
    duration: '22h 30m',
    progress: 10,
    thumbnail: 'https://images.unsplash.com/photo-1677442136019-21780efad99a?w=400&auto=format&fit=crop&q=80',
    description: 'Build neural networks, fine-tune LLMs, and optimize machine learning models using PyTorch & Python.',
    lessons: [
      { id: 'l301', title: '1. NumPy Vectorization & Matrix Math', type: 'video', duration: '35m', completed: true },
      { id: 'l302', title: '2. Deep Learning with PyTorch', type: 'video', duration: '50m', completed: false }
    ]
  }
];
