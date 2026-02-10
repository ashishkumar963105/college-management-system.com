// Portal JavaScript
document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    const loginSection = document.getElementById('loginSection');
    const dashboardSection = document.getElementById('dashboardSection');
    const logoutBtn = document.getElementById('logoutBtn');
    const sidebarItems = document.querySelectorAll('.sidebar-menu li');
    const contentSections = document.querySelectorAll('.content-section');

    // Login Handler
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const studentId = document.getElementById('studentId').value;
            const password = document.getElementById('password').value;

            // Simple validation (in real app, this would be server-side)
            if (studentId && password) {
                loginSection.style.display = 'none';
                dashboardSection.style.display = 'block';
                
                // Update student name
                document.getElementById('studentName').textContent = `Welcome, ${studentId}`;
            }
        });
    }

    // Logout Handler
    if (logoutBtn) {
        logoutBtn.addEventListener('click', function() {
            dashboardSection.style.display = 'none';
            loginSection.style.display = 'flex';
            loginForm.reset();
        });
    }

    // Sidebar Navigation
    sidebarItems.forEach(item => {
        item.addEventListener('click', function() {
            // Remove active class from all items
            sidebarItems.forEach(i => i.classList.remove('active'));
            
            // Add active class to clicked item
            this.classList.add('active');
            
            // Get section to show
            const sectionId = this.getAttribute('data-section');
            
            // Hide all sections
            contentSections.forEach(section => {
                section.classList.remove('active');
            });
            
            // Show selected section
            const targetSection = document.getElementById(sectionId);
            if (targetSection) {
                targetSection.classList.add('active');
            }
        });
    });

    // Quick Action Buttons
    const actionButtons = document.querySelectorAll('.action-btn');
    actionButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const gotoSection = this.getAttribute('data-goto');
            
            // Find and click the corresponding sidebar item
            sidebarItems.forEach(item => {
                if (item.getAttribute('data-section') === gotoSection) {
                    item.click();
                }
            });
        });
    });

    // Circular Progress Animation
    const circularProgress = document.querySelector('.circular-progress');
    if (circularProgress) {
        const percentage = circularProgress.getAttribute('data-percentage');
        circularProgress.style.background = `conic-gradient(var(--primary-color) 0% ${percentage}%, var(--bg-light) ${percentage}% 100%)`;
    }
});
