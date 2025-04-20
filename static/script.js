document.addEventListener("DOMContentLoaded", function() {
    // Handle the category filter dynamically:
    const filterButton = document.getElementById('filter-button');
    filterButton.addEventListener('click', function() {
        const category = document.getElementById('category').value;
        const startDate = document.getElementById('start_date').value;
        const endDate = document.getElementById('end_date').value;

        const url = `/transactions?category=${category}&start_date=${startDate}&end_date=${endDate}`;

        window.location.href = url; // Redirect with filter parameters
    });
});
