/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}", "./public/index.html"],
  theme: {
    screens: {
      sm: "480px",
      md: "768px",
      lg: "976px",
      xl: "1440px",
    },
    extend: {
      colors: {
        primary: "#111",
        secondary: "#7c3aed",
        background: "#fff",
        accent: "#7c3aed",
        danger: "#ef4444",
        textPrimary: "#111",
        textSecondary: "#fff",
        cta: "#F87171",
        success: "#4ade80",
        info: "#3B82F6",
      },
    },
  },
  plugins: [],
};
