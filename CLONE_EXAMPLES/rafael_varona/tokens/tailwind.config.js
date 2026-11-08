/** @type {import('tailwindcss').Config} */
module.exports = {
  theme: {
    extend: {
      colors: {
        brand: {
          primary: '#2b5672',
          secondary: '#116dff',
          muted: '#414141',
          surface: '#fff',
          foreground: '#000',
        },
      },
      fontFamily: {
        sans: ['open-sans-v2'],
      },
      borderRadius: {
        'custom-sm': '0',
        'custom-md': '0px',
        'custom-lg': '7px',
        'custom-xl': 'undefinedpx',
      },
      boxShadow: {
        'custom-card': 'none',
        'custom-elevated': 'var(--shd,0 1px 4px #0009)',
        'custom-hover': 'inset 0 0 1px 3px #116dff',
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
        'slide-horizontal-new': {
          '0%': {"transform": "translate(100%)"},
        },
        'slide-horizontal-old': {
          '80%': {"opacity": "1"},
          'to': {"opacity": "0", "transform": "translate(-100%)"},
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
        'slide-horizontal-new': 'slide-horizontal-new 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards',
        'slide-horizontal-old': 'slide-horizontal-old 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards',
      },
      transitionTimingFunction: {
        'spring': 'cubic-bezier(0.16, 1, 0.3, 1)',
        'bounce-soft': 'cubic-bezier(0.34, 1.56, 0.64, 1)',
        'smooth-out': 'cubic-bezier(0, 0, 0.2, 1)',
        'smooth-in-out': 'cubic-bezier(0.4, 0, 0.2, 1)',
        'accelerate': 'cubic-bezier(0.4, 0, 1, 1)',
        'custom-ease-1': 'cubic-bezier(0.3, 0.13, 0.12, 1)',
      },
    },
  },
  plugins: [],
};
