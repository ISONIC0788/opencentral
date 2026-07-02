/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  darkMode: 'class', // Supports dark mode toggling
  theme: {
    extend: {
      animation: {
        'path-slow': 'pathMove 25s linear infinite',
      },
      keyframes: {
        pathMove: {
          '0%': { strokeDashoffset: '1000', opacity: '0.3' },
          '50%': { opacity: '0.6' },
          '100%': { strokeDashoffset: '0', opacity: '0.3' },
        }
      }
    },
  },
  plugins: [],
}