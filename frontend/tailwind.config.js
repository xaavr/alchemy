/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        // Add 'jura' as a custom font family
        'jura': ['Jura', 'sans-serif'],
      },
    },
  },
  plugins: [],
}