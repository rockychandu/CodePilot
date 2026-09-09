/* Admin Panel Page Module */
import { mockUsers } from '../mock-data/users.js';

export class AdminPage {
  static async render() {
    return `
      <div class="page-wrapper">
        <div class="page-header">
          <div>
            <h1>Admin Operations & System Status</h1>
            <p class="text-secondary">System audit logs, user role assignments, content moderation, and engine status.</p>
          </div>
        </div>

        <div class="card" style="margin-bottom: var(--space-8);">
          <h3 style="margin-bottom: var(--space-4);">Registered Users Management</h3>
          <div class="table-container">
            <table class="data-table">
              <thead>
                <tr>
                  <th>User ID</th>
                  <th>Name</th>
                  <th>Email</th>
                  <th>Role</th>
                  <th>Rating</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                ${mockUsers.map(u => `
                  <tr>
                    <td><code>${u.id}</code></td>
                    <td><strong>${u.name}</strong></td>
                    <td>${u.email}</td>
                    <td><span class="badge-tag badge-easy">${u.role.toUpperCase()}</span></td>
                    <td>${u.rating || 1500}</td>
                    <td>
                      <button class="btn btn-secondary btn-sm">Edit Role</button>
                    </td>
                  </tr>
                `).join('')}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    `;
  }
}
