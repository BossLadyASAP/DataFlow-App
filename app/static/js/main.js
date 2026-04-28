/**
 * INF232 EC2 - Main JavaScript
 * Handles language switching and dark mode functionality
 */

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    initializeDarkMode();
    initializeLanguage();
});

/**
 * Initialize Dark Mode
 */
function initializeDarkMode() {
    const darkModeToggle = document.getElementById('dark-mode-toggle');
    const app = document.getElementById('app');
    
    // Check for saved dark mode preference or system preference
    const isDarkMode = localStorage.getItem('darkMode') === 'true' ||
                      (!localStorage.getItem('darkMode') && 
                       window.matchMedia('(prefers-color-scheme: dark)').matches);
    
    if (isDarkMode) {
        app.classList.add('dark-mode');
        app.classList.remove('light-mode');
        updateDarkModeIcon(true);
    } else {
        app.classList.add('light-mode');
        app.classList.remove('dark-mode');
        updateDarkModeIcon(false);
    }
    
    // Listen for system theme changes
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
        if (!localStorage.getItem('darkMode')) {
            if (e.matches) {
                app.classList.add('dark-mode');
                app.classList.remove('light-mode');
                updateDarkModeIcon(true);
            } else {
                app.classList.add('light-mode');
                app.classList.remove('dark-mode');
                updateDarkModeIcon(false);
            }
        }
    });
}

/**
 * Toggle Dark Mode
 */
function toggleDarkMode() {
    const app = document.getElementById('app');
    const isDarkMode = app.classList.contains('dark-mode');
    
    if (isDarkMode) {
        app.classList.remove('dark-mode');
        app.classList.add('light-mode');
        localStorage.setItem('darkMode', 'false');
        updateDarkModeIcon(false);
    } else {
        app.classList.add('dark-mode');
        app.classList.remove('light-mode');
        localStorage.setItem('darkMode', 'true');
        updateDarkModeIcon(true);
    }
}

/**
 * Update Dark Mode Icon
 */
function updateDarkModeIcon(isDarkMode) {
    const darkModeToggle = document.getElementById('dark-mode-toggle');
    if (darkModeToggle) {
        const icon = darkModeToggle.querySelector('i');
        if (isDarkMode) {
            icon.classList.remove('fa-moon');
            icon.classList.add('fa-sun');
        } else {
            icon.classList.remove('fa-sun');
            icon.classList.add('fa-moon');
        }
    }
}

/**
 * Initialize Language
 */
function initializeLanguage() {
    const languageSelect = document.getElementById('language-select');
    if (languageSelect) {
        // Set the select to the current language
        const currentLang = document.documentElement.lang || 'en';
        languageSelect.value = currentLang;
    }
}

/**
 * Change Language
 */
function changeLanguage() {
    const languageSelect = document.getElementById('language-select');
    const selectedLang = languageSelect.value;
    
    // Send request to change language
    fetch(`/api/language/${selectedLang}`)
        .then(response => {
            if (response.ok) {
                // Reload the page to apply the new language
                location.reload();
            }
        })
        .catch(error => {
            console.error('Error changing language:', error);
        });
}

/**
 * Format date for display
 */
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
}

/**
 * Show notification
 */
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.classList.add('show');
    }, 10);
    
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 3000);
}

/**
 * Debounce function for performance
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Throttle function for performance
 */
function throttle(func, limit) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Export functions for use in other scripts
window.toggleDarkMode = toggleDarkMode;
window.changeLanguage = changeLanguage;
window.formatDate = formatDate;
window.showNotification = showNotification;
window.debounce = debounce;
window.throttle = throttle;
