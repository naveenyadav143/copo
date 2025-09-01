// Sidebar toggle functionality
document.addEventListener('DOMContentLoaded', function() {
    const sidebar = document.querySelector('.sidebar');
    const sidebarToggle = document.querySelector('.sidebar-toggle');
    const sidebarOverlay = document.querySelector('.sidebar-overlay');
    const mainContent = document.querySelector('.main-content');

    // Function to toggle sidebar
    function toggleSidebar() {
        sidebar.classList.toggle('show');
        sidebarOverlay.classList.toggle('show');
        document.body.classList.toggle('sidebar-open');
    }

    // Toggle sidebar when button is clicked
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', function(e) {
            e.preventDefault();
            toggleSidebar();
        });
    }

    // Close sidebar when overlay is clicked
    if (sidebarOverlay) {
        sidebarOverlay.addEventListener('click', function() {
            toggleSidebar();
        });
    }

    // Close sidebar when clicking outside on mobile
    if (mainContent) {
        mainContent.addEventListener('click', function(e) {
            if (window.innerWidth <= 992 && sidebar.classList.contains('show')) {
                if (!e.target.closest('.sidebar')) {
                    toggleSidebar();
                }
            }
        });
    }

    // Handle window resize to ensure proper sidebar behavior
    window.addEventListener('resize', function() {
        if (window.innerWidth > 992) {
            sidebar.classList.remove('show');
            sidebarOverlay.classList.remove('show');
            document.body.classList.remove('sidebar-open');
        }
    });

    // Add keyboard accessibility
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && sidebar.classList.contains('show')) {
            toggleSidebar();
        }
    });

    // Add touch events for mobile devices
    let startX = 0;
    let currentX = 0;

    if (sidebar) {
        sidebar.addEventListener('touchstart', function(e) {
            startX = e.touches[0].clientX;
        }, { passive: true });

        sidebar.addEventListener('touchmove', function(e) {
            currentX = e.touches[0].clientX;
        }, { passive: true });

        sidebar.addEventListener('touchend', function() {
            const diff = startX - currentX;
            if (diff > 50 && sidebar.classList.contains('show')) {
                toggleSidebar();
            }
        }, { passive: true });
    }
});

// Add smooth scrolling for sidebar navigation
document.addEventListener('DOMContentLoaded', function() {
    const navLinks = document.querySelectorAll('.sidebar .nav-link');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            // Close sidebar on mobile after clicking a link
            if (window.innerWidth <= 992) {
                const sidebar = document.querySelector('.sidebar');
                const sidebarOverlay = document.querySelector('.sidebar-overlay');
                if (sidebar && sidebar.classList.contains('show')) {
                    sidebar.classList.remove('show');
                    sidebarOverlay.classList.remove('show');
                    document.body.classList.remove('sidebar-open');
                }
            }
        });
    });
});

// Scroll toggle functionality
document.addEventListener('DOMContentLoaded', function() {
    const scrollToggle = document.querySelector('.scroll-toggle');
    const body = document.body;
    
    // Check if scroll toggle button exists
    if (scrollToggle) {
        // Function to toggle scroll
        function toggleScroll() {
            body.classList.toggle('scroll-disabled');
            scrollToggle.classList.toggle('scroll-disabled');
            
            // Update button text based on state
            if (body.classList.contains('scroll-disabled')) {
                scrollToggle.innerHTML = '<i class="fas fa-lock"></i>';
                scrollToggle.setAttribute('title', 'Enable Scrolling');
            } else {
                scrollToggle.innerHTML = '<i class="fas fa-unlock"></i>';
                scrollToggle.setAttribute('title', 'Disable Scrolling');
            }
        }
        
        // Add click event to toggle button
        scrollToggle.addEventListener('click', function(e) {
            e.preventDefault();
            toggleScroll();
        });
        
        // Initialize button state
        scrollToggle.innerHTML = '<i class="fas fa-unlock"></i>';
        scrollToggle.setAttribute('title', 'Disable Scrolling');
        
        // Add keyboard shortcut (Ctrl+Shift+S)
        document.addEventListener('keydown', function(e) {
            if (e.ctrlKey && e.shiftKey && e.key === 'S') {
                e.preventDefault();
                toggleScroll();
            }
        });
    }
    
    // Create scroll toggle button if it doesn't exist
    if (!scrollToggle) {
        const button = document.createElement('button');
        button.className = 'scroll-toggle';
        button.innerHTML = '<i class="fas fa-unlock"></i>';
        button.setAttribute('title', 'Disable Scrolling');
        document.body.appendChild(button);
        
        button.addEventListener('click', function(e) {
            e.preventDefault();
            body.classList.toggle('scroll-disabled');
            button.classList.toggle('scroll-disabled');
            
            if (body.classList.contains('scroll-disabled')) {
                button.innerHTML = '<i class="fas fa-lock"></i>';
                button.setAttribute('title', 'Enable Scrolling');
            } else {
                button.innerHTML = '<i class="fas fa-unlock"></i>';
                button.setAttribute('title', 'Disable Scrolling');
            }
        });
        
        // Add keyboard shortcut (Ctrl+Shift+S)
        document.addEventListener('keydown', function(e) {
            if (e.ctrlKey && e.shiftKey && e.key === 'S') {
                e.preventDefault();
                body.classList.toggle('scroll-disabled');
                button.classList.toggle('scroll-disabled');
                
                if (body.classList.contains('scroll-disabled')) {
                    button.innerHTML = '<i class="fas fa-lock"></i>';
                    button.setAttribute('title', 'Enable Scrolling');
                } else {
                    button.innerHTML = '<i class="fas fa-unlock"></i>';
                    button.setAttribute('title', 'Disable Scrolling');
                }
            }
        });
    }
});
