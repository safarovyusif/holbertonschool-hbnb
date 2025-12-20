document.addEventListener('DOMContentLoaded', () => {
    // 1. Login formunu tapırıq
    const loginForm = document.getElementById('login-form');

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            // Səhifənin yenilənməsinin qarşısını alırıq
            event.preventDefault();

            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            try {
                // 2. API-yə sorğu göndəririk (AJAX Fetch)
                const response = await fetch('http://127.0.0.1:5000/api/v1/auth_session/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ email: email, password: password })
                });

                // 3. Cavabı yoxlayırıq
                if (response.ok) {
                    const data = await response.json();
                    // Tokeni cookie-də yadda saxlayırıq
                    document.cookie = `token=${data.token}; path=/`;
                    // Uğurlu girişdən sonra index səhifəsinə yönləndiririk
                    window.location.href = 'index.html';
                } else {
                    alert('Login failed. Please check your email and password.');
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Network error. Please try again later.');
            }
        });
    }
});
