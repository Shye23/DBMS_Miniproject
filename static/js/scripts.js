document.addEventListener('DOMContentLoaded', () => {
    fetch('/data')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            const tableBody = document.querySelector('#data-table tbody');
            tableBody.innerHTML = ''; // Clear existing data

            // Loop through the data and create table rows
            data.forEach(row => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${row.title}</td>
                    <td>${row.ingredients}</td>
                    <td>${row.instructions}</td>
                    <td>${row.cooking_time}</td>
                    <td>${row.servings}</td>
                `;
                tableBody.appendChild(tr);
            });
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
});