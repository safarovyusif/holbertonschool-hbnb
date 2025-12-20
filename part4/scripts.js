document.addEventListener('DOMContentLoaded', () => {
    // Dəyişənlər
    const loginLink = document.getElementById('login-link');
    const placesList = document.getElementById('places-list');
    const priceFilter = document.getElementById('price-filter');
    let allPlaces = []; // Bütün evləri burada yadda saxlayacağıq

    // 1. Tokeni yoxla (Login linkini göstər/gizlət)
    checkAuthentication();

    // 2. Evləri gətir
    fetchPlaces();

    // 3. Login forması varsa (login.html səhifəsi üçün)
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }

    // 4. Filtr dəyişəndə işə düşən funksiya
    if (priceFilter) {
        priceFilter.addEventListener('change', (event) => {
            const selectedPrice = event.target.value;
            filterPlaces(selectedPrice);
        });
    }

    // --- FUNKSİYALAR ---

    function checkAuthentication() {
        const token = getCookie('token');
        if (loginLink) {
            if (token) {
                loginLink.style.display = 'none'; // Token varsa, Login düyməsini gizlət
            } else {
                loginLink.style.display = 'block'; // Token yoxdursa, göstər
            }
        }
    }

    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
        return null;
    }

    async function handleLogin(event) {
        event.preventDefault();
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        try {
            const response = await fetch('http://127.0.0.1:5000/api/v1/auth_session/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            });

            if (response.ok) {
                const data = await response.json();
                document.cookie = `token=${data.token}; path=/`;
                window.location.href = 'index.html';
            } else {
                alert('Login failed');
            }
        } catch (error) {
            console.error('Error:', error);
        }
    }

    async function fetchPlaces() {
        if (!placesList) return; // Əgər index səhifəsində deyiliksə, dayan

        const token = getCookie('token');
        
        try {
            const response = await fetch('http://127.0.0.1:5000/api/v1/places', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    // Bəzi API-lər token tələb edir, əlavə edirik
                    ...(token && { 'Authorization': `Bearer ${token}` })
                }
            });

            if (response.ok) {
                allPlaces = await response.json(); // Məlumatı yaddaşa yazırıq
                displayPlaces(allPlaces); // Ekrana çıxarırıq
            }
        } catch (error) {
            console.error('Error fetching places:', error);
            placesList.innerHTML = '<p>Error loading places.</p>';
        }
    }

    function displayPlaces(places) {
        placesList.innerHTML = ''; // Siyahını təmizlə

        places.forEach(place => {
            const article = document.createElement('article');
            article.className = 'place-card';
            
            // Kartın HTML strukturu
            article.innerHTML = `
                <h2>${place.name}</h2>
                <div class="price">$${place.price_by_night} per night</div>
                <button class="details-button" onclick="window.location.href='place.html?id=${place.id}'">View Details</button>
            `;
            
            placesList.appendChild(article);
        });
    }

    function filterPlaces(price) {
        if (price === 'all') {
            displayPlaces(allPlaces); // Hamısını göstər
        } else {
            // Seçilən qiymətdən ucuz olanları süzgəcdən keçir
            const filtered = allPlaces.filter(place => place.price_by_night <= parseInt(price));
            displayPlaces(filtered);
        }
    }
});
