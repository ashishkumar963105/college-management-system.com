// Faculty Page JavaScript
document.addEventListener('DOMContentLoaded', function() {
    const deptButtons = document.querySelectorAll('.dept-btn');
    const facultyCards = document.querySelectorAll('.faculty-card');

    // Department filter functionality
    deptButtons.forEach(button => {
        button.addEventListener('click', function() {
            const selectedDept = this.getAttribute('data-dept');

            // Remove active class from all buttons
            deptButtons.forEach(btn => btn.classList.remove('active'));
            
            // Add active class to clicked button
            this.classList.add('active');

            // Filter faculty cards
            facultyCards.forEach(card => {
                const cardDept = card.getAttribute('data-department');
                
                if (selectedDept === 'all' || cardDept === selectedDept) {
                    card.style.display = 'block';
                    card.style.animation = 'fadeIn 0.5s';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });
});
