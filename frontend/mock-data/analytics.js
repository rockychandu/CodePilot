/* Mock Analytics & Chart Dataset */

export const mockAnalytics = {
  codingHours: 148,
  problemsSolved: 142,
  accuracyRate: '84.5%',
  currentStreak: 7,

  // 365-day Activity Heatmap simulation data
  heatmapData: Array.from({ length: 365 }, (_, i) => ({
    day: i,
    count: Math.random() > 0.4 ? Math.floor(Math.random() * 8) : 0
  })),

  // Skill progression radar chart points
  skillBreakdown: [
    { label: 'Python Core', score: 92 },
    { label: 'Data Structures', score: 85 },
    { label: 'Algorithms', score: 78 },
    { label: 'System Design', score: 65 },
    { label: 'Database & SQL', score: 88 },
    { label: 'AI & ML', score: 70 }
  ],

  // Rating graph over time
  ratingHistory: [
    { date: 'Jan', rating: 1500 },
    { date: 'Feb', rating: 1580 },
    { date: 'Mar', rating: 1620 },
    { date: 'Apr', rating: 1710 },
    { date: 'May', rating: 1690 },
    { date: 'Jun', rating: 1780 },
    { date: 'Jul', rating: 1845 }
  ],

  // Difficulty distribution
  difficultyDistribution: {
    easy: 75,
    medium: 52,
    hard: 15
  }
};
