class ThemeManager {
    constructor() {
        this.htmlElement = document.getElementById('htmlRoot');
        this.themeToggleBtn = document.getElementById('theme-toggle');
        this.themeIcon = document.getElementById('theme-icon');
        this.themes = ['system', 'light', 'dark'];
        this.themeTitles = {
            system: 'Switch to Light Theme',
            light: 'Switch to Dark Theme',
            dark: 'Switch to System Theme',
        };
        this.themeIcons = {
            system: 'fa-desktop',
            light: 'fa-sun',
            dark: 'fa-moon',
        };

        this.prefersDark = window.matchMedia('(prefers-color-scheme: dark)');

        this.init();
    }

    getStoredTheme() {
        return localStorage.getItem('theme') || 'system';
    }

    setStoredTheme(theme) {
        localStorage.setItem('theme', theme);
    }

    applyTheme(theme) {
        let themeToApply = theme;
        if (theme === 'system') {
            themeToApply = this.prefersDark.matches ? 'dark' : 'light';
        }

        if (themeToApply === 'dark') {
            this.htmlElement.classList.add('dark');
        } else {
            this.htmlElement.classList.remove('dark');
        }

        this.updateButtonState(theme);

        document.dispatchEvent(
            new CustomEvent('themeChanged', {
                detail: { theme: themeToApply },
            }),
        );
    }

    updateButtonState(currentTheme) {
        if (this.themeToggleBtn && this.themeIcon) {
            const currentIcon = this.themeIcons[currentTheme];
            const nextThemeIndex =
                (this.themes.indexOf(currentTheme) + 1) % this.themes.length;
            const nextTheme = this.themes[nextThemeIndex];

            this.themeIcon.className = `fas ${currentIcon}`;
            this.themeToggleBtn.title = this.themeTitles[currentTheme];
        }
    }

    cycleTheme() {
        const currentTheme = this.getStoredTheme();
        const nextThemeIndex =
            (this.themes.indexOf(currentTheme) + 1) % this.themes.length;
        const nextTheme = this.themes[nextThemeIndex];
        this.setStoredTheme(nextTheme);
        this.applyTheme(nextTheme);
    }

    init() {
        const storedTheme = this.getStoredTheme();
        this.applyTheme(storedTheme);

        this.themeToggleBtn?.addEventListener('click', () => {
            this.cycleTheme();
        });

        this.prefersDark.addEventListener('change', () => {
            if (this.getStoredTheme() === 'system') {
                this.applyTheme('system');
            }
        });
    }

    getCurrentTheme() {
        const storedTheme = this.getStoredTheme();
        return storedTheme === 'system'
            ? this.prefersDark.matches
                ? 'dark'
                : 'light'
            : storedTheme;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    window.themeManager = new ThemeManager();
});
