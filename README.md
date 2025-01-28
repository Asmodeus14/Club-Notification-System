
# Club Notification System - Vue Project with Tailwind CSS

This is a Vue.js project integrated with Tailwind CSS, used for the Club Notification System. Follow the instructions below to set up, install dependencies, and run the Vue app locally.

## Prerequisites

Ensure that the following software is installed on your machine:

- [Node.js](https://nodejs.org/) (LTS version recommended)
- [npm](https://www.npmjs.com/) (Node Package Manager, comes with Node.js)

To check if you have Node.js and npm installed, run:

```bash
node -v
npm -v
```

## Setup Instructions

### 1. Clone the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/Asmodeus14/Club-Notification-System
```

### 2. Navigate to the Project Directory

After cloning the repo, navigate into the project folder:

```bash
cd Club-Notification-System
```

### 3. Install Dependencies

Run the following command to install all the required dependencies for the project:

```bash
npm install
```

### 4. Install Tailwind CSS (If not already installed)

If Tailwind CSS is not installed, you can install it manually:

```bash
npm install tailwindcss postcss autoprefixer
```

Then, create the Tailwind configuration files:

```bash
npx tailwindcss init
```

### 5. Configure Tailwind CSS

Add Tailwind’s base, components, and utilities to your `src/assets/tailwind.css` (if the file doesn't exist, create it):

```css
/* src/assets/tailwind.css */
@tailwind base;
@tailwind components;
@tailwind utilities;
```

In the `vue.config.js` file (create it if it doesn't exist), add the following content to make sure Tailwind CSS is processed correctly by Vue:

```javascript
// vue.config.js
module.exports = {
  css: {
    loaderOptions: {
      postcss: {
        plugins: [require('tailwindcss'), require('autoprefixer')],
      },
    },
  },
};
```

### 6. Update `index.css`

Ensure that `src/index.css` includes the Tailwind directives:

```css
/* src/index.css */
@import './assets/tailwind.css';
```

### 7. Run the Development Server

After completing the setup, start the development server to see the project in action:

```bash
npm run serve
```

This will run the Vue.js development server. You can access the app by navigating to [http://localhost:8080](http://localhost:8080) in your browser.

## Project Structure

```
Club-Notification-System/
│
├── src/
│   ├── assets/
│   │   └── tailwind.css  # Tailwind CSS styles
│   ├── components/
│   │   ├── Login.vue     # Login component
│   │   └── LoginForm.vue # Form component
│   ├── App.vue           # Main Vue component
│   └── main.js           # Entry point for the Vue app
│
├── package.json          # Project dependencies and scripts
├── vue.config.js         # Configuration for Vue and PostCSS
├── .gitignore            # Git ignore file (node_modules, dist, etc.)
└── README.md             # This README file
```

### Default `.gitignore` 

The following files and folders are ignored by default (no need to commit them to your repository):

```
node_modules/          # Directory containing all npm packages
dist/                  # Production build folder
.DS_Store              # macOS system files
.idea/                 # IDE configuration files (e.g., JetBrains)
*.log                  # Log files
```

## Running in Production Mode

To build the app for production, use:

```bash
npm run build
```

This will create an optimized production build in the `dist/` folder.

## Linting and Formatting

To check for any linting issues, run:

```bash
npm run lint
```

To fix any auto-fixable issues:

```bash
npm run lint -- --fix
```

## Troubleshooting

1. **Missing Tailwind CSS Classes**: If you don’t see Tailwind styles applied, ensure you've followed the steps to configure Tailwind in `tailwind.css` and `vue.config.js`.
2. **Dependencies Not Installing**: If you face issues while installing dependencies, try deleting `node_modules` and running `npm install` again:
   ```bash
   rm -rf node_modules
   npm install
   ```

## License

This project is licensed under the MIT License.
