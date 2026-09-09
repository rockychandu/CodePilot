/**
 * CodePilot Main Single Page Application Entrypoint
 * Initializes router, routes, navbar, footer, command palette, and reactive state.
 */

import { Router } from './utils/router.js';
import { store } from './state/store.js';
import { AuthService } from './services/AuthService.js';
import { NavbarComponent } from './components/navbar.js';
import { FooterComponent } from './components/footer.js';
import { GlobalSearchComponent } from './components/global-search.js';

// Import Pages
import { LandingPage } from './pages/landing.js';
import { DashboardPage } from './pages/dashboard.js';
import { IdePage } from './pages/ide.js';
import { ProblemListPage } from './pages/problems/problem-list.js';
import { ProblemDetailPage } from './pages/problems/problem-detail.js';
import { ContestListPage } from './pages/contests/contest-list.js';
import { CourseListPage } from './pages/learning/course-list.js';
import { CourseDetailPage } from './pages/learning/course-detail.js';
import { ProjectListPage } from './pages/projects/project-list.js';
import { HistoryPage } from './pages/history.js';
import { ProfilePage } from './pages/profile.js';
import { SettingsPage } from './pages/settings.js';
import { AdminPage } from './pages/admin.js';
import { RuntimeDiagnosticsPage } from './pages/runtime-diagnostics.js';
import { AIPage } from './pages/ai.js';
import { LoginPage } from './pages/auth/login.js';
import { RegisterPage } from './pages/auth/register.js';
import { ForgotPasswordPage } from './pages/auth/forgot-password.js';
import { ResetPasswordPage } from './pages/auth/reset-password.js';
import { VerifyEmailPage } from './pages/auth/verify-email.js';

// Route Registry Mapping
const routes = {
  '/': LandingPage,
  '/home': LandingPage,
  '/dashboard': DashboardPage,
  '/ide': IdePage,
  '/problems': ProblemListPage,
  '/problems/:id': ProblemDetailPage,
  '/contests': ContestListPage,
  '/courses': CourseListPage,
  '/courses/:slug': CourseDetailPage,
  '/learning': CourseListPage,
  '/projects': ProjectListPage,
  '/history': HistoryPage,
  '/profile': ProfilePage,
  '/profile/:username': ProfilePage,
  '/settings': SettingsPage,
  '/admin': AdminPage,
  '/diagnostics': RuntimeDiagnosticsPage,
  '/runtime-diagnostics': RuntimeDiagnosticsPage,
  '/ai': AIPage,
  '/login': LoginPage,
  '/register': RegisterPage,
  '/forgot-password': ForgotPasswordPage,
  '/reset-password': ResetPasswordPage,
  '/verify-email': VerifyEmailPage
};

// Initialize Application
function initApp() {
  // Sync current user state
  const currentUser = AuthService.getCurrentUser();
  if (currentUser && AuthService.isAuthenticated()) {
    store.set('currentUser', currentUser);
    store.set('isAuthenticated', true);
  } else {
    store.set('currentUser', null);
    store.set('isAuthenticated', false);
  }

  // Render Navbar & Footer
  const navbarContainer = document.getElementById('navbar-container');
  if (navbarContainer) {
    navbarContainer.innerHTML = NavbarComponent.render();
    NavbarComponent.attachEvents();
  }

  const footerContainer = document.getElementById('footer-container');
  if (footerContainer) {
    footerContainer.innerHTML = FooterComponent.render();
  }

  // Initialize Global Search Command Palette (Ctrl+K)
  const paletteHolder = document.getElementById('command-palette-holder');
  if (paletteHolder) {
    const searchModal = new GlobalSearchComponent('command-palette-holder');
    paletteHolder.innerHTML = searchModal.render();
    searchModal.attachEvents();
  }

  // Initialize Hash-based SPA Router
  const router = new Router(routes, 'app-content');

  // Listen for login/logout state changes to update Navbar
  store.subscribe('isAuthenticated', () => {
    if (navbarContainer) {
      navbarContainer.innerHTML = NavbarComponent.render();
      NavbarComponent.attachEvents();
    }
  });

  return router;
}

// Start application when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initApp);
} else {
  initApp();
}
