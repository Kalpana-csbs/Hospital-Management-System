function editDoctor(id) {
    const row = document.querySelector(`tr[data-id="${id}"]`);
    const cells = row.getElementsByTagName('td');
    
    // Create edit form
    const form = document.createElement('form');
    form.innerHTML = `
        <td><input type="text" name="name" value="${cells[0].textContent}"></td>
        <td><input type="text" name="specialization" value="${cells[1].textContent}"></td>
        <td><input type="tel" name="phone" value="${cells[2].textContent}"></td>
        <td>
            <select name="availability">
                <option value="true" ${cells[3].textContent === 'Available' ? 'selected' : ''}>Available</option>
                <option value="false" ${cells[3].textContent === 'Not Available' ? 'selected' : ''}>Not Available</option>
            </select>
        </td>
        <td>
            <button type="submit" class="save-btn">Save</button>
            <button type="button" class="cancel-btn" onclick="cancelEdit(${id})">Cancel</button>
        </td>
    `;

    form.addEventListener('submit', (e) => {
        e.preventDefault();
        const formData = new FormData(form);
        fetch(`/edit_doctor/${id}`, {
            method: 'POST',
            body: formData
        }).then(() => {
            window.location.reload();
        });
    });

    row.innerHTML = '';
    row.appendChild(form);
}

function cancelEdit(id) {
    window.location.reload();
}

function deleteDoctor(id) {
    if (confirm('Are you sure you want to delete this doctor?')) {
        fetch(`/delete_doctor/${id}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(response => response.json())
        .then(data => {
            if (data.success) {
                const row = document.querySelector(`tr[data-id="${id}"]`);
                row.classList.add('fade-out');
                setTimeout(() => row.remove(), 500);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to delete doctor');
        });
    }
}

// Add animation to form submission
document.querySelector('.animate-form').addEventListener('submit', function(e) {
    e.preventDefault();
    this.classList.add('submitted');
    setTimeout(() => this.submit(), 300);
});
