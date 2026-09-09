# CodePilot — Algorithmic Contest & Rating Engine

## 1. Contest Lifecycle
1. **Creation & Publishing**: Admins schedule contests with specific start/end timestamps and problem assignments.
2. **Registration**: Developers register before or during active contest windows.
3. **Live Submissions**: Submissions are evaluated against real test cases with penalty point accounting.
4. **Scoring Formula**:
   $$\text{Rank Score} = \text{Solved Problems} \times 1000 - \text{Penalty (minutes)}$$
   Wrong submissions prior to acceptance incur a penalty (default: 10 minutes per wrong submission).

---

## 2. Real-Time Leaderboards
- **Global**: Ranks developers by total accumulated XP and problems solved.
- **Contest Live Board**: Sorts participants in descending score and ascending penalty order.
- **Streak Board**: Tracks consecutive days with verified code submissions.
