/* Mock Contests Dataset */

export const mockContests = [
  {
    id: 'contest_101',
    title: 'CodePilot Biweekly Speedrun #42',
    status: 'Live', // 'Live' | 'Upcoming' | 'Completed'
    startTime: '2026-09-09T10:00:00Z',
    endTime: '2026-09-09T13:00:00Z',
    duration: '2 Hours',
    participantsCount: 3840,
    problemsCount: 4,
    prizePool: '$1,500 + CodePilot Badges',
    leaderboard: [
      { rank: 1, username: 'tourist_clone', solved: 4, score: 800, penalty: '00:42:15' },
      { rank: 2, username: 'alex_dev', solved: 4, score: 800, penalty: '00:54:10' },
      { rank: 3, username: 'python_ninja', solved: 3, score: 550, penalty: '00:38:20' }
    ]
  },
  {
    id: 'contest_102',
    title: 'Python Grand Master Challenge',
    status: 'Upcoming',
    startTime: '2026-09-12T15:00:00Z',
    endTime: '2026-09-12T17:30:00Z',
    duration: '2.5 Hours',
    participantsCount: 1920,
    problemsCount: 5,
    prizePool: 'Swag Pack + 5,000 XP'
  },
  {
    id: 'contest_100',
    title: 'CodePilot Weekly #41',
    status: 'Completed',
    startTime: '2026-09-02T10:00:00Z',
    endTime: '2026-09-02T12:00:00Z',
    duration: '2 Hours',
    participantsCount: 4120,
    winner: 'tourist_clone'
  }
];
