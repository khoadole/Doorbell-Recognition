function showNotification(type, message) {
    const overlay = document.querySelector('.notification-overlay');
    const iconContainer = document.getElementById('notificationIcon');
    const messageElement = document.getElementById('notificationMessage');

    messageElement.innerText = message;
    iconContainer.innerHTML = '';

    const icon = document.createElement('img');
    icon.style.width = '80px';
    icon.style.height = '80px';
    icon.src = type.includes('success') ? '/static/images/check.svg' : '/static/images/cross.svg';
    icon.alt = type.includes('success') ? 'Success' : 'Error';
    iconContainer.appendChild(icon);

    overlay.style.display = 'flex';
    setTimeout(() => closeNotification(), 3000);
}

function closeNotification() {
    document.querySelector('.notification-overlay').style.display = 'none';
}
