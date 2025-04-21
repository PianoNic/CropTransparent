document.addEventListener("DOMContentLoaded", () => {
    const currentYearElement = document.getElementById("currentYear")
    if (currentYearElement) {
      currentYearElement.textContent = new Date().getFullYear()
    } else {
      console.warn('Footer element with ID "currentYear" not found.')
    }
  
    async function loadAppInfo() {
      try {
        const response = await fetch("/api/app-info")
        if (response.ok) {
          const info = await response.json()
          const versionElement = document.getElementById("version")
          const environmentElement = document.getElementById("environment")
  
          if (versionElement) {
            versionElement.textContent = info.version || "N/A"
            if (info.version) {
              versionElement.href = `https://github.com/Pianonic/CropTransparent/releases/tag/${info.version}`
            } else {
              versionElement.removeAttribute("href")
              versionElement.style.pointerEvents = "none"
            }
          } else {
            console.warn('Footer element with ID "version" not found.')
          }
  
          if (environmentElement) {
            environmentElement.textContent = info.environment || "N/A"
          } else {
            console.warn('Footer element with ID "environment" not found.')
          }
        } else {
          console.error(
            `Failed to load app info: ${response.status} ${response.statusText}`,
          )
          const versionElement = document.getElementById("version")
          const environmentElement = document.getElementById("environment")
          if (versionElement) versionElement.textContent = "Error"
          if (environmentElement) environmentElement.textContent = "Error"
        }
      } catch (error) {
        console.error("Failed to load app info:", error)
        const versionElement = document.getElementById("version")
        const environmentElement = document.getElementById("environment")
        if (versionElement) versionElement.textContent = "Error"
        if (environmentElement) environmentElement.textContent = "Error"
      }
    }
  
    loadAppInfo()
  })
  