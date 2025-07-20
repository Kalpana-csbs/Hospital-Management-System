function editAppointment(id) {
    const row = document.querySelector(`tr[data-id="${id}"]`);
    const cells = row.querySelectorAll('td');
    
    const patientSelect = document.createElement('select');
    // Clone the patient select from the form
    patientSelect.innerHTML = document.querySelector('select[name="patient"]').innerHTML;
    patientSelect.value = cells[0].getAttribute('data-id');
    
    const doctorSelect = document.createElement('select');
    // Clone the doctor select from the form
    doctorSelect.innerHTML = document.querySelector('select[name="doctor"]').innerHTML;
    doctorSelect.value = cells[1].getAttribute('data-id');
    
    const dateInput = document.createElement('input');
    dateInput.type = 'datetime-local';
    dateInput.value = cells[2].getAttribute('data-date');
    
    const notesInput = document.createElement('input');
    notesInput.type = 'text';
    notesInput.value = cells[3].textContent;
    
    cells[0].innerHTML = '';
    cells[0].appendChild(patientSelect);
    cells[1].innerHTML = '';
    cells[1].appendChild(doctorSelect);
    cells[2].innerHTML = '';
    cells[2].appendChild(dateInput);
    cells[3].innerHTML = '';
    cells[3].appendChild(notesInput);
    
    const saveBtn = document.createElement('button');
    saveBtn.textContent = 'Save';
    saveBtn.className = 'save-btn';
    saveBtn.onclick = () => saveAppointment(id, patientSelect, doctorSelect, dateInput, notesInput);
    
    const cancelBtn = document.createElement('button');
    cancelBtn.textContent = 'Cancel';
    cancelBtn.className = 'cancel-btn';
    cancelBtn.onclick = () => location.reload();
    
    cells[4].innerHTML = '';
    cells[4].appendChild(saveBtn);
    cells[4].appendChild(cancelBtn);
}

function saveAppointment(id, patientSelect, doctorSelect, dateInput, notesInput) {
    const formData = new FormData();
    formData.append('patient_id', patientSelect.value);
    formData.append('doctor_id', doctorSelect.value);
    formData.append('date', dateInput.value);
    formData.append('notes', notesInput.value);
    
    fetch(`/edit_appointment/${id}`, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            location.reload();
        }
    });
}

function deleteAppointment(id) {
    if (confirm('Are you sure you want to delete this appointment?')) {
        fetch(`/delete_appointment/${id}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const row = document.querySelector(`tr[data-id="${id}"]`);
                row.classList.add('fade-out');
                setTimeout(() => row.remove(), 500);
            }
        });
    }
}
