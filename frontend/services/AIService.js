/* Pilot AI Service Layer */
import { sleep } from '../utils/helpers.js';

export class AIService {
  static async askPilotAI(prompt, codeContext = '') {
    await sleep(600); // Realistic AI thinking delay

    if (prompt.toLowerCase().includes('explain') || prompt.toLowerCase().includes('how does')) {
      return {
        reply: `### Pilot AI Code Explanation\n\n` +
               `**Key Logic:**\n` +
               `1. The code initializes the necessary data structures and evaluates constraints.\n` +
               `2. Uses efficient iteration techniques to achieve optimal time complexity.\n\n` +
               `**Complexity:**\n` +
               `- Time Complexity: **O(N)**\n` +
               `- Space Complexity: **O(1)**`
      };
    }

    if (prompt.toLowerCase().includes('review') || prompt.toLowerCase().includes('bug')) {
      return {
        reply: `### Pilot AI Code Review Report\n\n` +
               `**Quality Score: 92/100**\n\n` +
               `**Pros:**\n` +
               `- Clean function scoping & PEP8 syntax.\n` +
               `- Good variable naming conventions.\n\n` +
               `**Suggestions:**\n` +
               `- Consider handling edge cases where input list is empty.`
      };
    }

    return {
      reply: `I analyzed your request. Here is the recommended approach for **${prompt}**:\n\n` +
             `\`\`\`python\n` +
             `# Python Solution recommended by Pilot AI\n` +
             `def solve(data):\n` +
             `    return [x for x in data if x % 2 == 0]\n` +
             `\`\`\``
    };
  }
}
