/**
 * Project Workspace Service
 * Real REST API integration for CodePilot Developer Workspaces
 */

import { AuthService } from './AuthService.js';

const API_BASE = 'http://127.0.0.1:5000/api/v1/projects';

function getAuthHeaders() {
  const token = AuthService.getToken();
  return {
    'Content-Type': 'application/json',
    ...(token ? { 'Authorization': `Bearer ${token}` } : {})
  };
}

export class ProjectService {
  /**
   * Fetch all projects for the authenticated user
   */
  static async getProjects() {
    try {
      const res = await fetch(API_BASE, {
        headers: getAuthHeaders()
      });
      if (!res.ok) {
        if (res.status === 401) return [];
        throw new Error(`Failed to load projects (${res.status})`);
      }
      return await res.json();
    } catch (err) {
      console.error('[ProjectService.getProjects] Error:', err);
      return [];
    }
  }

  /**
   * Fetch detailed project workspace by ID including file tree
   */
  static async getProjectById(id) {
    try {
      const res = await fetch(`${API_BASE}/${id}`, {
        headers: getAuthHeaders()
      });
      if (!res.ok) {
        throw new Error(`Project ${id} not found`);
      }
      return await res.json();
    } catch (err) {
      console.error(`[ProjectService.getProjectById(${id})] Error:`, err);
      return null;
    }
  }

  /**
   * Create a new project workspace with scaffolded multi-file templates
   */
  static async createProject({ title, description, language, template }) {
    const res = await fetch(API_BASE, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify({
        title: title || 'Untitled Project',
        description: description || '',
        language: (language || 'python').toLowerCase(),
        template: (template || 'cli').toLowerCase()
      })
    });
    if (!res.ok) {
      const errData = await res.json().catch(() => ({}));
      throw new Error(errData.error || 'Failed to create project');
    }
    return await res.json();
  }

  /**
   * Rename project title and/or description
   */
  static async renameProject(id, { title, description }) {
    const res = await fetch(`${API_BASE}/${id}`, {
      method: 'PATCH',
      headers: getAuthHeaders(),
      body: JSON.stringify({ title, description })
    });
    if (!res.ok) {
      const errData = await res.json().catch(() => ({}));
      throw new Error(errData.error || 'Failed to rename project');
    }
    return await res.json();
  }

  /**
   * Duplicate project workspace
   */
  static async duplicateProject(id) {
    const res = await fetch(`${API_BASE}/${id}/duplicate`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify({})
    });
    if (!res.ok) {
      const errData = await res.json().catch(() => ({}));
      throw new Error(errData.error || 'Failed to duplicate project');
    }
    return await res.json();
  }

  /**
   * Delete project workspace
   */
  static async deleteProject(id) {
    const res = await fetch(`${API_BASE}/${id}`, {
      method: 'DELETE',
      headers: getAuthHeaders()
    });
    if (!res.ok) {
      const errData = await res.json().catch(() => ({}));
      throw new Error(errData.error || 'Failed to delete project');
    }
    return true;
  }

  /**
   * Create or update a project file
   */
  static async updateFile(projectId, filename, content) {
    const res = await fetch(`${API_BASE}/${projectId}/files`, {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: JSON.stringify({ filename, content })
    });
    if (!res.ok) {
      const errData = await res.json().catch(() => ({}));
      throw new Error(errData.error || 'Failed to save file');
    }
    return await res.json();
  }

  /**
   * Delete a project file
   */
  static async deleteFile(projectId, filename) {
    const res = await fetch(`${API_BASE}/${projectId}/files/${encodeURIComponent(filename)}`, {
      method: 'DELETE',
      headers: getAuthHeaders()
    });
    if (!res.ok) {
      const errData = await res.json().catch(() => ({}));
      throw new Error(errData.error || 'Failed to delete file');
    }
    return true;
  }

  /**
   * Export project as formatted JSON package
   */
  static async exportProject(id) {
    const res = await fetch(`${API_BASE}/${id}/export`, {
      headers: getAuthHeaders()
    });
    if (!res.ok) {
      throw new Error('Failed to export project');
    }
    return await res.json();
  }
}
