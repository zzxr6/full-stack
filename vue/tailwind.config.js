/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './index.html',
    './src/**/*.html',
    './src/**/*.vue',
    './src/**/*.jsx',
  ],
  theme: {
    extend: {},
    screens: {
      '2xl': {'max': '1536px'},
      'xl': {'max': '1280px'},
      'lg': {'max': '1024px'},
      'mlg': {'max': '826px'},
      'md': {'max': '768px'},
      'sm': {'max': '640px'},
    },
  },
  plugins: [],
}

