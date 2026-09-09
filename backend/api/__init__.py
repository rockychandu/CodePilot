"""
CodePilot API Blueprints Registration
"""

from backend.api.auth_routes import auth_bp
from backend.api.execution_routes import execution_bp
from backend.api.problem_routes import problem_bp
from backend.api.contest_routes import contest_bp
from backend.api.course_routes import course_bp
from backend.api.project_routes import project_bp
from backend.api.ai_routes import ai_bp
from backend.api.history_routes import history_bp
from backend.api.search_routes import search_bp
from backend.api.notification_routes import notification_bp
from backend.api.admin_routes import admin_bp

def register_blueprints(app):
    """Register all modular domain blueprints on the Flask application."""
    app.register_blueprint(auth_bp)
    app.register_blueprint(execution_bp)
    app.register_blueprint(problem_bp)
    app.register_blueprint(contest_bp)
    app.register_blueprint(course_bp)
    app.register_blueprint(project_bp)
    app.register_blueprint(ai_bp)
    app.register_blueprint(history_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(notification_bp)
    app.register_blueprint(admin_bp)
