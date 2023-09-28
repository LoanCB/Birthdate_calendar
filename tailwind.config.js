/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./base/templates/**/*.{html,js}", "./node_modules/flowbite/**/*.js"],
  plugins: [
        require('flowbite/plugin')
  ],
  theme: {
    extend: {
      colors: {
        main: {
          500: '#006889'
        },
        secondary: {
          500: '#6C1F87'
        }
      }
    },
  },
  plugins: [],
}
