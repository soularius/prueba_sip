function updateAttendanceStatus(attendanceId, newStatus) {
    fetch(`/SIP/attendances/api_update_attendance/${attendanceId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ status: newStatus })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        showMessage('Attendance updated successfully API', 'success');        
    })
    .catch((error) => {
        console.error('Error:', error);
        showMessage('Error updated attendance API', 'error');
    });
}

function showMessage(message, isError = false) {
    const flashContainer = document.querySelector('.w2p_flash');
    if (flashContainer) {
        flashContainer.innerHTML = message + `<span id="closeflash"> × </span>`; // Establecer el mensaje
        flashContainer.style.display = 'block'; // Mostrar la alerta
        if (isError) {
            flashContainer.classList.add('alert-danger');
        } else {
            flashContainer.classList.add('alert-success');
        }
    }
    setTimeout(() => {
        flashContainer.style.display = 'none';
    }, 5000);
}