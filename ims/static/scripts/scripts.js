// Password toggle function
function togglePassword() {
    const passwordField = document.getElementById("id_password");
    const toggleIcon = document.getElementById("toggleIcon");
    
    if (passwordField.type === "password") {
        passwordField.type = "text";
        toggleIcon.classList.remove("fa-eye");
        toggleIcon.classList.add("fa-eye-slash");
    } else {
        passwordField.type = "password";
        toggleIcon.classList.remove("fa-eye-slash");
        toggleIcon.classList.add("fa-eye");
    }
}

// Chart script - Only run if the chart element exists
document.addEventListener('DOMContentLoaded', function() {
    const chartElement = document.getElementById('salesChart');
    
    if (chartElement) {
        const ctx = chartElement.getContext('2d');
        const salesChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                datasets: [{
                    label: 'Sales (₦)',
                    data: [12000, 19000, 8000, 15000, 20000, 25000],
                    borderColor: 'rgb(75, 192, 192)',
                    backgroundColor: 'rgba(75, 192, 192, 0.1)',
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                    }
                }
            }
        });
    }

    // login page with ajax
    
    const loginLink = document.querySelector('#user-login');
    
    if (loginLink) {
        loginLink.addEventListener('click', function(e) {
            e.preventDefault();
            
            fetch('/login-form/')
            .then(response => {
                if(!response.ok) {
                    throw new Error('Network response was not okay');
                }
                return response.text();
            })
            .then(html => {
                const mainContent = document.querySelector('.main-content');
                if (mainContent) {
                    mainContent.innerHTML = html;
                } else {
                    console.error('Page not found!');
                }
            })
            .catch(error => {
                console.error('ajax failed:', error);
            });
        });
    }
});