class ThemeManager {
    constructor() {
        this.htmlElement = document.getElementById('htmlRoot');
        this.themeSystemBtn = document.getElementById('theme-system');
        this.themeLightBtn = document.getElementById('theme-light');
        this.themeDarkBtn = document.getElementById('theme-dark');
        this.buttons = [this.themeSystemBtn, this.themeLightBtn, this.themeDarkBtn];

        this.prefersDark = window.matchMedia('(prefers-color-scheme: dark)');

        this.init();
    }

    getStoredTheme() {
        return localStorage.getItem('theme');
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

        this.updateButtonStates(theme);

        document.dispatchEvent(new CustomEvent('themeChanged', {
            detail: { theme: themeToApply }
        }));
    }

    updateButtonStates(activeTheme) {
        this.buttons.forEach(button => {
            if (button) {
                button.classList.remove('active');
                if (button.id === `theme-${activeTheme}`) {
                    button.classList.add('active');
                }
            }
        });
    }

    init() {
        const storedTheme = this.getStoredTheme() || 'system';
        this.applyTheme(storedTheme);

        this.themeSystemBtn?.addEventListener('click', () => {
            this.setStoredTheme('system');
            this.applyTheme('system');
        });

        this.themeLightBtn?.addEventListener('click', () => {
            this.setStoredTheme('light');
            this.applyTheme('light');
        });

        this.themeDarkBtn?.addEventListener('click', () => {
            this.setStoredTheme('dark');
            this.applyTheme('dark');
        });

        this.prefersDark.addEventListener('change', () => {
            if (this.getStoredTheme() === 'system') {
                this.applyTheme('system');
            }
        });
    }

    getCurrentTheme() {
        const storedTheme = this.getStoredTheme() || 'system';
        return storedTheme === 'system' ?
            (this.prefersDark.matches ? 'dark' : 'light') :
            storedTheme;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    window.themeManager = new ThemeManager();
});