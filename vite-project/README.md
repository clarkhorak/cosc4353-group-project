# cosc4353-group-project
Software Design class group project

# Volunteer Management System

This is a web-based Volunteer Management System developed for a non-profit organization. The system helps match volunteers to events and tasks based on location, skills, availability, and preferences, while allowing administrators to efficiently manage operations.

## Features

- User registration and authentication
- Profile management (skills, preferences, location, availability)
- Event and task creation/management
- Volunteer matching algorithm
- Email notifications (assignments, updates, reminders)
- Participation history tracking

## Tech Stack

- **Frontend**: React (Vite)
- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL (managed via Render)
- **Hosting**: Render
- **Email Notifications**: SendGrid or Mailgun

## Development Methodology

- **Agile (Scrum)**: Project is broken into 4 sprints
- Weekly standups and continuous deployment
- Source control and CI/CD via GitHub

## Getting Started

To run the project locally:

```bash
npm install       # Install dependencies
npm run dev       # Start development server
```


## Coding Languages Used

## 1. TypeScript
We used **TypeScript** for all our React components and logic files. TypeScript is a superset of JavaScript that adds static typing, which helps catch errors early and improves code maintainability. All files with the `.tsx` extension are written in TypeScript, allowing us to use both React JSX and type annotations.

## 2. JavaScript
Some configuration files (such as `vite.config.js`) and scripts may use **JavaScript**. JavaScript is the core language of the web and is used for scripting and configuration where type safety is less critical.

## 3. CSS
We used **CSS** (`.css` files) for styling the application. CSS allows us to define the look and feel of the user interface, including layout, colors, fonts, and responsiveness.

## 4. JSON
**JSON** (JavaScript Object Notation) files are used for configuration (such as `package.json`) and for storing data in a structured, human-readable format. JSON is essential for managing project dependencies and settings.

## 5. Markdown
We used **Markdown** (`.md` files) for documentation, such as this file and the project instructions. Markdown provides a simple way to format text for project documentation.

---

**How We Used Them:**
- **TypeScript**: For building the main application, including all React components, state management, and logic.
- **JavaScript**: For configuration files and scripts required by build tools.
- **CSS**: For styling the user interface and ensuring a consistent look and feel.
- **JSON**: For configuration files and structured data storage.
- **Markdown**: For writing documentation and instructions for contributors and users.