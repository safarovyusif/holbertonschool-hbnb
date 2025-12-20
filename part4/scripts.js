document.addEventListener('DOMContentLoaded', () => {
    // --- ÜMUMİ DƏYİŞƏNLƏR ---
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');
    const addReviewSection = document.getElementById('add-review-section');

    // 1. Login Linkini İdarə et (Görünüb/Gizlənməsi)
    if (loginLink) {
        if (token) {
            loginLink.style.display = 'none'; // Giriş edibsə gizlət
        } else {
            loginLink.style.display = 'block';
        }
    }

    // 2. Add Review Düyməsini İdarə et (Place səhifəsi üçün)
    if (addReviewSection) {
        if (token) {
            addReviewSection.style.display = 'block'; // Giriş edibsə göstər
        } else {
            addReviewSection.style.display = 'none';
        }
    }

    // --- SƏHİFƏLƏR ÜZRƏ MƏNTİQ ---

    // A. LOGIN SƏHİFƏSİ
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
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
        });
    }

    // B. INDEX SƏHİFƏSİ (Evlərin Siyahısı)
    const placesList = document.getElementById('places-list');
    const priceFilter = document.getElementById('price-filter');
    
    if (placesList) {
        let allPlaces = [];
        fetchPlaces(token).then(data => {
            allPlaces = data;
            displayPlaces(allPlaces);
        });

        if (priceFilter) {
            priceFilter.addEventListener('change', (e) => {
                const price = e.target.value;
                if (price === 'all') {
                    displayPlaces(allPlaces);
                } else {
                    const filtered = allPlaces.filter(p => p.price_by_night <= parseInt(price));
                    displayPlaces(filtered);
                }
            });
        }
    }

    // C. PLACE DETAILS SƏHİFƏSİ (Təkdə evin detalları) - TASK 4 BURADADIR
    const placeNameElement = document.getElementById('place-name');
    if (placeNameElement) {
        // URL-dən ID-ni götürürük
        const urlParams = new URLSearchParams(window.location.search);
        const placeId = urlParams.get('id');

        if (placeId) {
            fetchPlaceDetails(token, placeId);
        } else {
            window.location.href = 'index.html'; // ID yoxdursa ana səhifəyə at
        }
    }

    // --- KÖMƏKÇİ FUNKSİYALAR ---

    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
        return null;
    }

    async function fetchPlaces(token) {
        try {
            const response = await fetch('http://127.0.0.1:5000/api/v1/places', {
                headers: token ? { 'Authorization': `Bearer ${token}` } : {}
            });
            if (response.ok) return await response.json();
        } catch (error) {
            console.error('Error loading places:', error);
        }
        return [];
    }

    function displayPlaces(places) {
        const placesList = document.getElementById('places-list');
        placesList.innerHTML = '';
        places.forEach(place => {
            const article = document.createElement('article');
            article.className = 'place-card';
            article.innerHTML = `
                <h2>${place.name}</h2>
                <div class="price">$${place.price_by_night} per night</div>
                <button class="details-button" onclick="window.location.href='place.html?id=${place.id}'">View Details</button>
            `;
            placesList.appendChild(article);
        });
    }

    // Task 4 üçün xüsusi funksiya
    async function fetchPlaceDetails(token, placeId) {
        try {
            const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`, {
                headers: token ? { 'Authorization': `Bearer ${token}` } : {}
            });

            if (response.ok) {
                const place = await response.json();
                
                // Məlumatları HTML-ə doldururuq
                document.getElementById('place-name').textContent = place.name;
                document.getElementById('place-host').innerHTML = `<b>Host:</b> ${place.user_id}`; // Sadəlik üçün ID
                document.getElementById('place-price').innerHTML = `<b>Price:</b> $${place.price_by_night}/night`;
                document.getElementById('place-description').innerHTML = place.description;

                // Amenities (İmkanlar)
                const amenitiesList = document.getElementById('place-amenities');
                amenitiesList.innerHTML = '';
                // Əgər amenities API-dən gəlirsə (hazırda boş gələ bilər)
                if (place.amenities) {
                   place.amenities.forEach(amenity => {
                       const li = document.createElement('li');
                       li.textContent = amenity.name || amenity;
                       amenitiesList.appendChild(li);
                   });
                }

                // Reviews (Rəylər)
                const reviewsList = document.getElementById('reviews-list');
                reviewsList.innerHTML = '';
                if (place.reviews) {
                    place.reviews.forEach(review => {
                        const div = document.createElement('div');
                        div.className = 'review-card';
                        div.innerHTML = `
                            <p>${review.text}</p>
                            <span><b>User:</b> ${review.user_id}</span>
                        `;
                        reviewsList.appendChild(div);
                    });
                }
            } else {
                alert('Could not load place details.');
            }
        } catch (error) {
            console.error('Error fetching details:', error);
        }
    }
});
