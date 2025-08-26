# Overview

This is a comprehensive multi-functional translation web application built with Python Flask. The application provides a modern dashboard-style interface for real-time voice translation, file translation with drag & drop functionality, translation history management, and detailed user statistics. The system includes secure user authentication, profile management with photo uploads, and a fully French-localized interface with responsive design.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Backend Architecture

**Flask Framework**: The application uses Flask as the primary web framework with a modular blueprint structure separating authentication, main routes, and dashboard functionality. The application follows the Model-View-Controller (MVC) pattern with clear separation of concerns.

**Database Layer**: Uses SQLAlchemy ORM with Flask-Migrate for database migrations. The system is configured to work with SQLite by default but can be easily switched to PostgreSQL or other databases via environment configuration. The database schema includes User and Translation models with proper relationships and cascade deletion.

**Authentication System**: Implements Flask-Login for session management with secure password hashing using Werkzeug. CSRF protection is provided through Flask-WTF forms. The system includes user registration, login, logout, and profile management capabilities.

**Translation Engine**: Integrates Google Translate API (googletrans) for text translation services with automatic language detection using langdetect. The system supports both voice-to-text translation and file-based translation workflows.

## Frontend Architecture

**Template System**: Uses Jinja2 templating with a base template that provides a consistent dashboard layout. The design features a fixed sidebar navigation and main content area with responsive Bootstrap 5 framework.

**User Interface**: Implements a modern dashboard design with a two-column layout - fixed sidebar for navigation and main content area. The interface is fully localized in French with Font Awesome icons and custom CSS for enhanced user experience.

**JavaScript Functionality**: Modular JavaScript classes handle voice recognition (VoiceTranslation), file upload with drag & drop (FileTranslation), and dashboard interactions. Uses Web Speech API for real-time voice capture and translation.

## Data Storage Solutions

**File Management**: Implements secure file upload handling with configurable upload directories for user files and profile photos. File validation ensures only allowed extensions (.txt, .json for translations, image formats for profiles) are accepted with size limits.

**Translation History**: Stores all translations with metadata including source/target languages, translation type (voice/file), timestamps, and update tracking. Users can view, edit, and export their translation history.

## Security Mechanisms

**Input Validation**: All forms use Flask-WTF with comprehensive validation rules. File uploads are secured with extension validation and size limits. User input is properly sanitized to prevent injection attacks.

**Session Security**: Implements secure session management with configurable secret keys and CSRF protection. ProxyFix middleware is included for HTTPS support in production environments.

# External Dependencies

**Translation Services**: Google Translate API (googletrans) for text translation and langdetect for automatic language detection. These services provide the core translation functionality without requiring API keys for basic usage.

**Frontend Libraries**: Bootstrap 5 for responsive UI framework, Font Awesome for iconography, and standard web APIs (Web Speech API) for voice recognition functionality.

**Python Packages**: Core dependencies include Flask ecosystem packages (Flask-SQLAlchemy, Flask-Migrate, Flask-Login, Flask-WTF), security libraries (Werkzeug), and utility packages for language processing.

**Database**: Configured for SQLite by default with easy migration to PostgreSQL or other SQL databases through environment configuration and Flask-Migrate.