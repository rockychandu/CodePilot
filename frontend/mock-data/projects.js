/* Mock Projects Dataset */

export const mockProjects = [
  {
    id: 'proj_1',
    title: 'Python Microservice Framework',
    description: 'Lightweight asynchronous web service framework written in pure Python with custom routing.',
    language: 'Python',
    stars: 342,
    forks: 89,
    author: 'alex_dev',
    updatedAt: '2026-09-08',
    readme: `# Python Microservice Framework\n\nHigh performance REST API microservice starter with built-in AST code validation and JSON serialization.`,
    files: [
      { name: 'main.py', content: `import sys\n\ndef start_server():\n    print("Starting Python API Server on port 5000...")\n    print("Server ready.")\n\nif __name__ == '__main__':\n    start_server()` },
      { name: 'config.py', content: `PORT = 5000\nDEBUG = True\nSECRET_KEY = "codepilot_secret"` },
      { name: 'README.md', content: `# Python Microservice Framework` }
    ]
  },
  {
    id: 'proj_2',
    title: 'AI Neural Net Trainer in Python',
    description: 'Clean matrix multiplication neural network trainer built from scratch without external dependencies.',
    language: 'Python',
    stars: 520,
    forks: 140,
    author: 'ai_wizard',
    updatedAt: '2026-09-07',
    files: [
      { name: 'model.py', content: `class NeuralNet:\n    def __init__(self, layers):\n        self.layers = layers\n    def forward(self, x):\n        return x * 0.9` },
      { name: 'train.py', content: `from model import NeuralNet\n\nnet = NeuralNet([10, 5, 1])\nprint("Model training loss: 0.042")` }
    ]
  }
];
