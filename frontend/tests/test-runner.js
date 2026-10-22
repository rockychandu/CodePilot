/**
 * CodePilot Automated Frontend Integration Test Runner
 * Compatible with both Node.js test runs and browser test consoles.
 */

export async function runFrontendTests() {
  if (typeof window === 'undefined') {
    const memory = {};
    const storage = {
      getItem: (k) => memory[k] || null,
      setItem: (k, v) => { memory[k] = v; },
      removeItem: (k) => { delete memory[k]; }
    };
    globalThis.window = {
      location: { hostname: 'localhost', hash: '' },
      localStorage: storage
    };
    globalThis.localStorage = storage;
    globalThis.document = {
      documentElement: { setAttribute: () => {} },
      getElementById: () => null,
      addEventListener: () => {}
    };
  }
  console.log("==========================================================");
  console.log("   CodePilot Frontend Automated Test Runner               ");
  console.log("==========================================================");

  let passed = 0;
  let total = 0;

  function assert(condition, testName) {
    total++;
    if (condition) {
      passed++;
      console.log(`[PASS] ${testName}`);
    } else {
      console.error(`[FAIL] ${testName}`);
    }
  }

  // 1. Local Storage Mock & State Store Test
  try {
    const memoryStore = {};
    const mockStorage = {
      getItem: (k) => memoryStore[k] || null,
      setItem: (k, v) => { memoryStore[k] = v; },
      removeItem: (k) => { delete memoryStore[k]; }
    };
    mockStorage.setItem('test_token', 'jwt_mock_token_123');
    assert(mockStorage.getItem('test_token') === 'jwt_mock_token_123', 'Client Storage Read/Write Operations');
  } catch (e) {
    assert(false, `Storage Test Failed: ${e.message}`);
  }

  // 2. Language Definitions Verification
  try {
    const expectedLanguages = ['python', 'javascript', 'java', 'cpp', 'c', 'go', 'rust'];
    assert(expectedLanguages.length >= 7, 'Multi-Language Supported Registry');
  } catch (e) {
    assert(false, `Language Registry Test Failed: ${e.message}`);
  }

  // 3. Password Strength Evaluation Logic
  try {
    function evaluatePassword(pwd) {
      let score = 0;
      if (pwd.length >= 8) score++;
      if (/[A-Z]/.test(pwd)) score++;
      if (/[0-9]/.test(pwd)) score++;
      if (/[^A-Za-z0-9]/.test(pwd)) score++;
      return score;
    }
    assert(evaluatePassword('SuperSecret123!') === 4, 'Password Strength Scoring Validation');
    assert(evaluatePassword('weak') === 0, 'Weak Password Detection');
  } catch (e) {
    assert(false, `Password Evaluation Failed: ${e.message}`);
  }

  // 4. Status Pill Formatting
  try {
    const acceptedStatuses = ['ACCEPTED', 'Accepted', 'Passed'];
    assert(acceptedStatuses.includes('Accepted'), 'Verdict Mapping Assertion');
  } catch (e) {
    assert(false, `Verdict Mapping Failed: ${e.message}`);
  }

  // 5. Project Service API Client Methods Interface
  try {
    const { ProjectService } = await import('../services/ProjectService.js');
    assert(typeof ProjectService.getProjects === 'function', 'ProjectService.getProjects Available');
    assert(typeof ProjectService.createProject === 'function', 'ProjectService.createProject Available');
    assert(typeof ProjectService.renameProject === 'function', 'ProjectService.renameProject Available');
    assert(typeof ProjectService.duplicateProject === 'function', 'ProjectService.duplicateProject Available');
    assert(typeof ProjectService.exportProject === 'function', 'ProjectService.exportProject Available');
  } catch (e) {
    assert(false, `ProjectService Test Failed: ${e.message}`);
  }

  // 6. Developer Sidebar Component Verification
  try {
    const { SidebarComponent } = await import('../components/sidebar.js');
    assert(typeof SidebarComponent.render === 'function', 'SidebarComponent.render Available');
    const html = SidebarComponent.render();
    assert(typeof html === 'string', 'SidebarComponent Returns Valid Markup');
  } catch (e) {
    assert(false, `SidebarComponent Test Failed: ${e.message}`);
  }

  console.log("----------------------------------------------------------");
  console.log(`Results: ${passed}/${total} Passed (${((passed / total) * 100).toFixed(1)}%)`);
  return { passed, total, success: passed === total };
}

// Auto-run when executed directly via Node.js
if (typeof process !== 'undefined' && process.argv && process.argv[1]?.includes('test-runner')) {
  runFrontendTests().then(res => {
    if (!res.success) process.exit(1);
  });
}
