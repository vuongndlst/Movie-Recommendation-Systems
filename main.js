function loadMovies() {
    fetch('http://localhost:5000/movies')
    .then(response => response.json())
    .then(data => {
        const select = document.getElementById('movieDropdown');
        data.forEach(movie => {
            const option = document.createElement('option');
            option.value = option.text = movie;
            select.add(option);
        });
    })
    .catch(error => console.error('Lỗi tải danh sách phim:', error));
}

function getRecommendations() {
    const movieTitle = document.getElementById('movieDropdown').value;
    fetch('http://localhost:5000/recommend', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({title: movieTitle})
    })
    .then(response => response.json())
    .then(data => {
        let recommendationsHtml = '<ul>';
        data.movies.forEach((movie, index) => {
            recommendationsHtml += `<li><input type="checkbox" id="movie${index}" name="movie${index}" value="${movie}">
                                     <label for="movie${index}">${movie} - ${data.reasons[index]}</label></li>`;
        });
        recommendationsHtml += '</ul>';
        document.getElementById('recommendations').innerHTML = recommendationsHtml;
    })
    .catch(error => console.error('Lỗi:', error));
}

function submitFeedback() {
    const checkboxes = document.querySelectorAll('input[type="checkbox"]:checked');
    let liked_movies = [];
    checkboxes.forEach(checkbox => {
        liked_movies.push(checkbox.value);
    });
    fetch('http://localhost:5000/feedback', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({liked_movies: liked_movies})
    })
    .then(response => response.json())
    .then(data => console.log('Phản hồi đã gửi:', data))
    .catch(error => console.error('Lỗi gửi phản hồi:', error));
}

window.onload = loadMovies;
