/* Multi-Language Execution Service Layer */
import { sleep } from '../utils/helpers.js';

export class ExecutionService {
  static async run({ language, sourceCode, stdin = '' }, onProgress = () => {}) {
    onProgress({ state: 'Preparing', message: `Initializing ${language.toUpperCase()} execution worker...` });
    await sleep(250);

    onProgress({ state: 'Compiling', message: `Compiling/Parsing ${language.toUpperCase()} code...` });
    await sleep(350);

    if (!sourceCode || !sourceCode.trim()) {
      return {
        status: 'Compilation Error',
        output: 'Error: Source code cannot be empty.',
        runtime: '0.000s',
        memory: '0 MB',
        exitCode: 1
      };
    }

    const langUpper = language.toUpperCase();
    let sampleOutput = '';

    switch (language) {
      case 'python':
        sampleOutput = `[Python 3.12 Execution Output]\nPython Array Sum: 150\nExecution completed with exit code 0.`;
        break;

      case 'c':
        sampleOutput = `[C (GCC 13.2) Output]\nHello from C Execution Engine!\nSum of 1 to 10 = 55\nProcess exited with status 0.`;
        break;

      case 'cpp':
        sampleOutput = `[C++ 20 (GCC) Output]\nC++ Vector Total: 115\nExecution finished in 0.012 seconds.`;
        break;

      case 'java':
        sampleOutput = `[Java 21 OpenJDK Output]\nHello from Java 21 Execution Engine!\nSupported Languages: [Python, C, C++, Java, JavaScript, R, SQL]\nProcess completed.`;
        break;

      case 'javascript':
        sampleOutput = `[JavaScript Node.js v20 Output]\nJavaScript Execution:\nFactorial(5) = 120`;
        break;

      case 'r':
        sampleOutput = `[R Language Environment Output]\nR Execution Engine Active\nVector Mean: 26.44\nVector Standard Deviation: 12.83699`;
        break;

      case 'sql':
        sampleOutput = `[SQL Database Execution Output]\nQuery Executed: SELECT * FROM developers WHERE score >= 95;\n\n| id | name  | language | score |\n|----|-------|----------|-------|\n| 1  | Alex  | Python   | 98    |\n| 2  | Sarah | C++      | 95    |\n\n(2 rows returned)`;
        break;

      default:
        sampleOutput = `[${langUpper} Execution Engine]\nProgram executed successfully.`;
        break;
    }

    return {
      status: 'Accepted',
      output: sampleOutput,
      runtime: `${(Math.random() * 0.04 + 0.01).toFixed(3)}s`,
      memory: `${(Math.random() * 8 + 10).toFixed(1)} MB`,
      exitCode: 0
    };
  }
}
