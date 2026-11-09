/** @type {import('tailwindcss').Config} */
module.exports = {
  theme: {
    extend: {
      colors: {
        brand: {
          primary: '#f79ce0',
          secondary: '#55cdff',
          muted: '#e2e4e7',
          surface: '#fff',
          foreground: '#08090a',
        },
      },
      fontFamily: {
        sans: ['ui-sans-serif', 'system-ui', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'Helvetica Neue', 'Arial', 'Noto Sans', 'sans-serif', 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol', 'Noto Color Emoji'],
      },
      borderRadius: {
        'custom-sm': '8px',
        'custom-md': 'var(--border-radius)',
        'custom-lg': '4px',
        'custom-xl': '50%',
      },
      boxShadow: {
        'custom-card': '0 4px 12px rgba(0,0,0,.1),0 0 0 2px rgba(0,0,0,.2)',
        'custom-elevated': '0 4px 12px rgba(0,0,0,.1)',
        'custom-hover': '0 0 0 2px rgba(0,0,0,.4)',
      },
      keyframes: {
        'fade-in-up': {
          '0%': {"opacity": "0", "transform": "translateY(16px)"},
          '100%': {"opacity": "1", "transform": "translateY(0)"},
        },
        'fade-in-down': {
          '0%': {"opacity": "0", "transform": "translateY(-16px)"},
          '100%': {"opacity": "1", "transform": "translateY(0)"},
        },
        'float': {
          '0%, 100%': {"transform": "translateY(0)"},
          '50%': {"transform": "translateY(-6px)"},
        },
        'pulse-glow': {
          '0%, 100%': {"opacity": "0.35", "transform": "scale(1)"},
          '50%': {"opacity": "0.75", "transform": "scale(1.04)"},
        },
        'marquee': {
          '0%': {"transform": "translateX(0%)"},
          '100%': {"transform": "translateX(-50%)"},
        },
        'shimmer': {
          '0%': {"background-position": "-200% 0"},
          '100%': {"background-position": "200% 0"},
        },
        'accordion-down': {
          '0%': {"height": "0", "opacity": "0"},
          '100%': {"height": "var(--radix-accordion-content-height, auto)", "opacity": "1"},
        },
        'accordion-up': {
          '0%': {"height": "var(--radix-accordion-content-height, auto)", "opacity": "1"},
          '100%': {"height": "0", "opacity": "0"},
        },
        'scale-subtle': {
          '0%, 100%': {"transform": "scale(1)"},
          '50%': {"transform": "scale(1.02)"},
        },
        'badge-ping': {
          '0%': {"transform": "scale(1)", "opacity": "0.8"},
          '75%, 100%': {"transform": "scale(2)", "opacity": "0"},
        },
        'swipe-out-left': {
          'from': {"transform": "var(--y) translateX(var(--swipe-amount-x))", "opacity": "1"},
          'to': {"transform": "var(--y) translateX(calc(var(--swipe-amount-x) - 100%))", "opacity": "0"},
        },
        'swipe-out-right': {
          'from': {"transform": "var(--y) translateX(var(--swipe-amount-x))", "opacity": "1"},
          'to': {"transform": "var(--y) translateX(calc(var(--swipe-amount-x) + 100%))", "opacity": "0"},
        },
      },
      animation: {
        'fade-in-up': 'fade-in-up 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards',
        'fade-in-down': 'fade-in-down 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards',
        'float': 'float 4s ease-in-out infinite',
        'pulse-glow': 'pulse-glow 3.5s ease-in-out infinite',
        'marquee': 'marquee 30s linear infinite',
        'shimmer': 'shimmer 2s linear infinite',
        'accordion-down': 'accordion-down 0.2s ease-out',
        'accordion-up': 'accordion-up 0.2s ease-out',
        'scale-subtle': 'scale-subtle 3s ease-in-out infinite',
        'badge-ping': 'badge-ping 1.5s cubic-bezier(0, 0, 0.2, 1) infinite',
        'swipe-out-left': 'swipe-out-left 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards',
        'swipe-out-right': 'swipe-out-right 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards',
      },
      transitionTimingFunction: {
        'spring': 'cubic-bezier(0.16, 1, 0.3, 1)',
        'bounce-soft': 'cubic-bezier(0.34, 1.56, 0.64, 1)',
        'smooth-out': 'cubic-bezier(0, 0, 0.2, 1)',
        'smooth-in-out': 'cubic-bezier(0.4, 0, 0.2, 1)',
        'accelerate': 'cubic-bezier(0.4, 0, 1, 1)',
        'custom-ease-1': 'cubic-bezier(.32, .72, 0, 1)',
      },
    },
  },
  plugins: [],
};
