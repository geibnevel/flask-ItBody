const themeSwitcher = document.getElementById('themeSwitcher');
themeSwitcher.addEventListener('click', () => {
    document.body.classList.toggle('dark');
    const currentTheme = document.body.classList.contains('dark') ? '🌞' : '🌙';
    themeSwitcher.textContent = currentTheme;
});