// Theme Management
class ThemeManager {
    constructor() {
        this.theme = localStorage.getItem('theme') || 'light';
        this.toggleButton = document.getElementById('themeToggle');
        this.init();
    }
    
    init() {
        // Apply saved theme on load
        this.applyTheme(this.theme);
        
        // Add event listener for theme toggle
        if (this.toggleButton) {
            this.toggleButton.addEventListener('click', () => this.toggleTheme());
        }
    }
    
    applyTheme(theme) {
        const body = document.body;
        const darkIcon = document.querySelector('.dark-icon');
        const lightIcon = document.querySelector('.light-icon');
        
        if (theme === 'dark') {
            body.classList.add('dark-mode');
            if (darkIcon) darkIcon.style.display = 'none';
            if (lightIcon) lightIcon.style.display = 'inline';
        } else {
            body.classList.remove('dark-mode');
            if (darkIcon) darkIcon.style.display = 'inline';
            if (lightIcon) lightIcon.style.display = 'none';
        }
        
        this.theme = theme;
        localStorage.setItem('theme', theme);
    }
    
    toggleTheme() {
        const newTheme = this.theme === 'light' ? 'dark' : 'light';
        this.applyTheme(newTheme);
    }
}

// Dashboard common functionality
document.addEventListener('DOMContentLoaded', function() {
    // Initialize theme manager after DOM is loaded
    const themeManager = new ThemeManager();
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        if (alert.classList.contains('alert-success') || alert.classList.contains('alert-info')) {
            setTimeout(() => {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }, 5000);
        }
    });
    
    // Add loading states to forms
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn && !submitBtn.disabled) {
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status"></span> ' + submitBtn.textContent;
                submitBtn.disabled = true;
            }
        });
    });
    
    // Tooltip initialization
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Add smooth transitions to cards
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.style.transition = 'transform 0.3s ease, box-shadow 0.3s ease';
    });
    
    // Profile photo preview
    const profilePhotoInput = document.querySelector('input[name="profile_photo"]');
    if (profilePhotoInput) {
        profilePhotoInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    const currentPhoto = document.querySelector('.current-avatar');
                    if (currentPhoto) {
                        currentPhoto.src = e.target.result;
                    }
                };
                reader.readAsDataURL(file);
            }
        });
    }
    
    // Confirm delete actions
    const deleteLinks = document.querySelectorAll('a[href*="delete"]');
    deleteLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            if (!confirm('Êtes-vous sûr de vouloir supprimer cet élément ?')) {
                e.preventDefault();
            }
        });
    });
    
    // Add animation to statistics cards
    const statsCards = document.querySelectorAll('.stats-card');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animation = 'fadeInUp 0.6s ease forwards';
            }
        });
    });
    
    statsCards.forEach(card => {
        observer.observe(card);
    });
    
    // Add keyboard navigation for sidebar
    document.addEventListener('keydown', function(e) {
        if (e.altKey) {
            const sidebarLinks = document.querySelectorAll('.sidebar-nav .nav-link');
            let currentIndex = -1;
            
            sidebarLinks.forEach((link, index) => {
                if (link.classList.contains('active')) {
                    currentIndex = index;
                }
            });
            
            if (e.key === 'ArrowUp' && currentIndex > 0) {
                e.preventDefault();
                sidebarLinks[currentIndex - 1].click();
            } else if (e.key === 'ArrowDown' && currentIndex < sidebarLinks.length - 1) {
                e.preventDefault();
                sidebarLinks[currentIndex + 1].click();
            }
        }
    });
});

// Add CSS animation keyframes
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .fade-in-up {
        animation: fadeInUp 0.6s ease forwards;
    }
`;
document.head.appendChild(style);
