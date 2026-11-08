/** @type {import('tailwindcss').Config} */
module.exports = {
  theme: {
    extend: {
      colors: {
        brand: {
          primary: '#6366f1',
          secondary: '#06b6d4',
          muted: '#a1a1aa',
          surface: '#fff',
          foreground: '#09090b',
        },
      },
      fontFamily: {
        sans: ['Plus Jakarta Sans', 'system-ui', '-apple-system', 'sans-serif'],
      },
      borderRadius: {
        'custom-sm': '6px',
        'custom-md': 'var(--radius-sm)',
        'custom-lg': '9999px',
        'custom-xl': 'var(--radius-lg)',
      },
      boxShadow: {
        'custom-card': '0 1px 3px rgba(0,0,0,0.3)',
        'custom-elevated': '0 4px 20px rgba(0, 0, 0, 0.2)',
      },
    },
  },
  plugins: [],
};
