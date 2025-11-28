/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./src/**/*.{astro,html,js,jsx,ts,tsx,vue}"
  ],
  theme: {
    extend: {
      colors: {
        primary: { DEFAULT: '#3b82f6', dark: '#2563eb', light: '#60a5fa' },
        accent: '#8b5cf6'
      },
      backgroundImage: {
        'brand-gradient': 'linear-gradient(135deg,#f0f9ff 0%,#e0f2fe 100%)',
        'text-gradient': 'linear-gradient(135deg,#3b82f6 0%,#8b5cf6 100%)'
      }
    }
  },
  plugins: []
}
