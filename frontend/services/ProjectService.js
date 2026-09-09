/* Project Workspace Service */
import { mockProjects } from '../mock-data/projects.js';
import { sleep } from '../utils/helpers.js';

export class ProjectService {
  static async getProjects() {
    await sleep(200);
    return mockProjects;
  }

  static async getProjectById(id) {
    await sleep(150);
    return mockProjects.find(p => p.id === id) || mockProjects[0];
  }
}
