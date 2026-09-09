/* Hash-based Single Page Application Router */

export class Router {
  constructor(routes = {}, appContainerId = 'app-content') {
    this.routes = routes;
    this.containerId = appContainerId;
    this.currentPath = '';

    window.addEventListener('hashchange', () => this.handleRoute());
    if (document.readyState === 'complete' || document.readyState === 'interactive') {
      setTimeout(() => this.handleRoute(), 0);
    } else {
      window.addEventListener('load', () => this.handleRoute());
    }
  }

  addRoute(path, pageComponent) {
    this.routes[path] = pageComponent;
  }

  navigate(path) {
    window.location.hash = path.startsWith('#') ? path : `#${path}`;
  }

  getHashPath() {
    const hash = window.location.hash.slice(1);
    return hash.split('?')[0] || '/';
  }

  getQueryParams() {
    const hash = window.location.hash;
    const queryIndex = hash.indexOf('?');
    if (queryIndex === -1) return {};
    
    const queryString = hash.slice(queryIndex + 1);
    const params = {};
    queryString.split('&').forEach(param => {
      const [key, value] = param.split('=');
      if (key) params[decodeURIComponent(key)] = decodeURIComponent(value || '');
    });
    return params;
  }

  matchRoute(currentPath) {
    // Exact match
    if (this.routes[currentPath]) {
      return { component: this.routes[currentPath], params: {} };
    }

    // Dynamic param route matching (e.g. /problems/:id)
    for (const routePath in this.routes) {
      if (routePath.includes(':')) {
        const routeParts = routePath.split('/').filter(Boolean);
        const pathParts = currentPath.split('/').filter(Boolean);

        if (routeParts.length === pathParts.length) {
          const params = {};
          let match = true;

          for (let i = 0; i < routeParts.length; i++) {
            if (routeParts[i].startsWith(':')) {
              const paramName = routeParts[i].slice(1);
              params[paramName] = pathParts[i];
            } else if (routeParts[i] !== pathParts[i]) {
              match = false;
              break;
            }
          }

          if (match) {
            return { component: this.routes[routePath], params };
          }
        }
      }
    }

    return null;
  }

  async handleRoute() {
    const path = this.getHashPath();
    this.currentPath = path;
    const container = document.getElementById(this.containerId);

    if (!container) return;

    // Scroll to top
    window.scrollTo(0, 0);

    const routeMatch = this.matchRoute(path);

    if (routeMatch) {
      const { component, params } = routeMatch;
      const queryParams = this.getQueryParams();
      
      try {
        container.innerHTML = await component.render({ params, queryParams, router: this });
        if (component.afterRender) {
          await component.afterRender({ params, queryParams, router: this });
        }
      } catch (err) {
        console.error(`[Router] Error rendering route ${path}:`, err);
        container.innerHTML = `<div class="page-wrapper text-center"><h2>Error Loading Page</h2><p class="text-muted">${err.message}</p></div>`;
      }
    } else {
      // 404 Page
      container.innerHTML = `
        <div class="page-wrapper text-center" style="padding: 5rem 1rem;">
          <h1 style="font-size: 5rem; color: var(--accent-cyan);">404</h1>
          <h2 style="margin-bottom: 1rem;">Page Not Found</h2>
          <p class="text-secondary" style="max-width: 500px; margin: 0 auto 2rem auto;">
            The page <code>${path}</code> does not exist or has been moved.
          </p>
          <a href="#/dashboard" class="btn btn-primary">Return to Dashboard</a>
        </div>
      `;
    }

    // Update active nav links
    document.querySelectorAll('.nav-link').forEach(link => {
      const href = link.getAttribute('href');
      if (href === `#${path}` || (path !== '/' && href && href.startsWith(`#${path}`))) {
        link.classList.add('active');
      } else {
        link.classList.remove('active');
      }
    });
  }
}
