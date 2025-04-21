;(function () {
    function applyTheme(theme) {
      if (theme === "dark") {
        document.documentElement.classList.add("dark")
      } else {
        document.documentElement.classList.remove("dark")
      }
    }
  
    function getInitialTheme() {
      let theme
      try {
        theme = localStorage.getItem("theme")
  
        if (!theme || theme === "system") {
          theme = window.matchMedia("(prefers-color-scheme: dark)").matches
            ? "dark"
            : "light"
        }
      } catch (e) {
        console.warn(
          "Could not access localStorage or matchMedia. Defaulting to light theme.",
          e,
        )
        theme = "light"
      }
      return theme === "dark" ? "dark" : "light"
    }
  
    const initialTheme = getInitialTheme()
    applyTheme(initialTheme)
  
    try {
      window
        .matchMedia("(prefers-color-scheme: dark)")
        .addEventListener("change", (event) => {
          const storedTheme = localStorage.getItem("theme")
          if (storedTheme === "system" || !storedTheme) {
            applyTheme(event.matches ? "dark" : "light")
          }
        })
    } catch (e) {
      console.warn("Could not add matchMedia listener in theme-init.js", e)
    }
  })()
  