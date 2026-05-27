module.exports = {
  content: ['./index.html', './src/**/*.{js,jsx,ts,tsx}'],
  theme: {
    extend: {
      colors: {
        cinematic: '#0b0b0b',
        accent: '#c59a6a',
        danger: '#d34b4b'
      },
      fontFamily: {
        display: ['"Playfair Display"', 'serif'],
        body: ['Manrope', 'sans-serif']
      }
    },
  },
  plugins: [],
}
