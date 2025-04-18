(() => {
    const htmlElement = document.getElementById('htmlRoot');
    const themeSystemBtn = document.getElementById('theme-system');
    const themeLightBtn = document.getElementById('theme-light');
    const themeDarkBtn = document.getElementById('theme-dark');
    const buttons = [themeSystemBtn, themeLightBtn, themeDarkBtn];

    const getStoredTheme = () => localStorage.getItem('theme');
    const setStoredTheme = (theme) => localStorage.setItem('theme', theme);

    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)');

    const applyTheme = (theme) => {
        let themeToApply = theme;
        if (theme === 'system') {
            themeToApply = prefersDark.matches ? 'dark' : 'light';
        }

        if (themeToApply === 'dark') {
            htmlElement.classList.add('dark');
        } else {
            htmlElement.classList.remove('dark');
        }

        updateButtonStates(theme);
    };

    const updateButtonStates = (activeTheme) => {
        buttons.forEach(button => {
            if (button) {
                button.classList.remove('active');
                if (button.id === `theme-${activeTheme}`) {
                    button.classList.add('active');
                }
            }
        });
    };

    const initTheme = () => {
        const storedTheme = getStoredTheme() || 'system';
        applyTheme(storedTheme);
    };

    themeSystemBtn?.addEventListener('click', () => {
        setStoredTheme('system');
        applyTheme('system');
    });

    themeLightBtn?.addEventListener('click', () => {
        setStoredTheme('light');
        applyTheme('light');
    });

    themeDarkBtn?.addEventListener('click', () => {
        setStoredTheme('dark');
        applyTheme('dark');
    });

    prefersDark.addEventListener('change', () => {
        if (getStoredTheme() === 'system') {
            applyTheme('system');
        }
    });

    document.addEventListener('DOMContentLoaded', initTheme);
})();
