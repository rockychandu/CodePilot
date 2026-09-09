/* Integrated In-Browser Automated Test Runner */
import { AuthService } from '../services/AuthService.js';
import { ExecutionService } from '../services/ExecutionService.js';
import { ProblemService } from '../services/ProblemService.js';
import { store } from '../state/store.js';

export async function runBrowserTests() {
  const results = [];
  console.log('[Test Runner] Executing frontend unit test suite...');

  // Test 1: Auth Service Validation
  try {
    const res = await AuthService.login('alex.developer@codepilot.io', 'password123');
    results.push({ name: 'AuthService.login()', success: res.success });
  } catch (err) {
    results.push({ name: 'AuthService.login()', success: false, error: err.message });
  }

  // Test 2: Execution Simulator State Flow
  try {
    const execRes = await ExecutionService.run({ language: 'python', sourceCode: 'print("Hello Test")' });
    results.push({ name: 'ExecutionService.run()', success: execRes.status === 'Accepted' });
  } catch (err) {
    results.push({ name: 'ExecutionService.run()', success: false, error: err.message });
  }

  // Test 3: Problem Service Filter
  try {
    const { problems } = await ProblemService.getProblems({ difficulty: 'Easy' });
    results.push({ name: 'ProblemService.getProblems(Easy)', success: problems.length > 0 });
  } catch (err) {
    results.push({ name: 'ProblemService.getProblems(Easy)', success: false, error: err.message });
  }

  // Test 4: Store State Mutation
  try {
    store.set('test_key', 42);
    results.push({ name: 'store.set/get()', success: store.get('test_key') === 42 });
  } catch (err) {
    results.push({ name: 'store.set/get()', success: false, error: err.message });
  }

  return results;
}
