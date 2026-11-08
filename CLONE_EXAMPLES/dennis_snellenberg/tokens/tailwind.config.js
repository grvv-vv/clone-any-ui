/** @type {import('tailwindcss').Config} */
module.exports = {
  theme: {
    extend: {
      colors: {
        brand: {
          primary: '#3b82f6',
          secondary: '#6366f1',
          muted: '#f1f1f1',
          surface: '#ffffff',
          foreground: '#101010',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      borderRadius: {
      },
      boxShadow: {
        'custom-card': 'rgb(0, 0, 0) 0px 0px 0px 0px',
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
      },
      transitionTimingFunction: {
        'spring': 'cubic-bezier(0.16, 1, 0.3, 1)',
        'bounce-soft': 'cubic-bezier(0.34, 1.56, 0.64, 1)',
        'smooth-out': 'cubic-bezier(0, 0, 0.2, 1)',
        'smooth-in-out': 'cubic-bezier(0.4, 0, 0.2, 1)',
        'accelerate': 'cubic-bezier(0.4, 0, 1, 1)',
      },
    },
  },
  plugins: [],
};
