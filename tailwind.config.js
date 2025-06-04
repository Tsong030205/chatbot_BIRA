/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./static/**/*.js",
  ],
  theme: {
    extend: {
      colors: {
        'primary': '#1a5f38',
        'secondary': '#2d8a4f',
      },
    },
  },
  plugins: [],
} 