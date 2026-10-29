export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        canvas: "#0A0E17",
        surface: "#111827",
        elevated: "#1F2937",
        border: "#1F2A3A",
        accent: "#00E5A0",
        danger: "#FF4757",
        indigo: "#6366F1",
        muted: "#9CA3AF",
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
        mono: ["JetBrains Mono", "monospace"],
      },
      boxShadow: {
        glow: "0 0 20px rgba(0,229,160,0.15)",
        danger: "0 0 20px rgba(255,71,87,0.15)",
      },
      keyframes: {
        pulseDot: {
          "0%,100%": { opacity: 1, transform: "scale(1)" },
          "50%": { opacity: 0.4, transform: "scale(0.85)" },
        },
        flashUp: {
          "0%": { backgroundColor: "rgba(0,229,160,0.3)" },
          "100%": { backgroundColor: "transparent" },
        },
        flashDown: {
          "0%": { backgroundColor: "rgba(255,71,87,0.3)" },
          "100%": { backgroundColor: "transparent" },
        },
        shimmer: {
          "0%": { backgroundPosition: "-1000px 0" },
          "100%": { backgroundPosition: "1000px 0" },
        },
      },
      animation: {
        pulseDot: "pulseDot 2s ease-in-out infinite",
        flashUp: "flashUp 0.6s ease-out",
        flashDown: "flashDown 0.6s ease-out",
        shimmer: "shimmer 2s linear infinite",
      },
    },
  },
  plugins: [],
};