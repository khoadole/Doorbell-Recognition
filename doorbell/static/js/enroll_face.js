// Global variables
let currentDeleteId = null;

// Set default date to today
document.getElementById('dateSearch').valueAsDate = new Date();

// Modal functions
function openUploadModal() {
  document.getElementById('uploadModal').style.display = 'block';
  document.body.style.overflow = 'hidden';
}

function closeUploadModal() {
  document.getElementById('uploadModal').style.display = 'none';
  document.body.style.overflow = 'auto';

  // Reset form
  document.getElementById('uploadForm').reset();
  document.getElementById('imagePreview').style.display = 'none';
  document.querySelector('.upload-placeholder').style.display = 'flex';
}

function openDeleteModal(faceId, faceName) {
  currentDeleteId = faceId;
  document.getElementById('deleteName').textContent = faceName;
  document.getElementById('deleteModal').style.display = 'block';
  document.body.style.overflow = 'hidden';
}

function closeDeleteModal() {
  document.getElementById('deleteModal').style.display = 'none';
  document.body.style.overflow = 'auto';
  currentDeleteId = null;
}

// Delete face function
function deleteFace(faceId, faceName) {
  openDeleteModal(faceId, faceName);
}

function confirmDelete() {
  if (!currentDeleteId) return;

  // Create form data for delete request
  const formData = new FormData();
  formData.append('face_id', currentDeleteId);
  formData.append('csrfmiddlewaretoken', document.querySelector('[name=csrfmiddlewaretoken]').value);

  // Send delete request
  fetch(window.location.href, {
    method: 'POST',
    body: formData,
    headers: {
      'X-Requested-With': 'XMLHttpRequest',
    }
  })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        // Remove the row from table
        const row = document.querySelector(`tr[data-id="${currentDeleteId}"]`);
        if (row) {
          row.remove();
        }

        // Check if table is empty
        const remainingRows = document.querySelectorAll('.table tbody tr:not(.empty-row)');
        if (remainingRows.length === 0) {
          const tbody = document.querySelector('.table tbody');
          tbody.innerHTML = `
                    <tr class="empty-row">
                        <td colspan="5" class="empty-message">
                            No enrolled faces found. Upload your first face to get started!
                        </td>
                    </tr>
                `;
        }

        showNotification('Face deleted successfully!', 'success');
      } else {
        showNotification(data.message || 'Error deleting face', 'error');
      }
    })
    .catch(error => {
      console.error('Error:', error);
      showNotification('Error deleting face', 'error');
    })
    .finally(() => {
      closeDeleteModal();
    });
}

// File upload handling
document.getElementById('faceImage').addEventListener('change', function (e) {
  const file = e.target.files[0];
  if (file) {
    // Check file size (5MB limit)
    if (file.size > 5 * 1024 * 1024) {
      showNotification('File size must be less than 5MB', 'error');
      return;
    }

    // Check file type
    if (!file.type.startsWith('image/')) {
      showNotification('Please select a valid image file', 'error');
      return;
    }

    const reader = new FileReader();
    reader.onload = function (e) {
      const preview = document.getElementById('imagePreview');
      preview.src = e.target.result;
      preview.style.display = 'block';
      document.querySelector('.upload-placeholder').style.display = 'none';
    };
    reader.readAsDataURL(file);
  }
});

// Form submission
document.getElementById('uploadForm').addEventListener('submit', function (e) {
  e.preventDefault();

  const formData = new FormData(this);
  const submitBtn = document.querySelector('.submit-btn');
  const originalText = submitBtn.textContent;

  // Show loading state
  submitBtn.textContent = 'Uploading...';
  submitBtn.disabled = true;

  fetch(window.location.href, {
    method: 'POST',
    body: formData,
    headers: {
      'X-Requested-With': 'XMLHttpRequest',
    }
  })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        showNotification('Face uploaded successfully!', 'success');
        closeUploadModal();

        // Reload page to show new face
        setTimeout(() => {
          window.location.reload();
        }, 1000);
      } else {
        showNotification(data.message || 'Error uploading face', 'error');
      }
    })
    .catch(error => {
      console.error('Error:', error);
      showNotification('Error uploading face', 'error');
    })
    .finally(() => {
      submitBtn.textContent = originalText;
      submitBtn.disabled = false;
    });
});

// Close modal when clicking outside
window.addEventListener('click', function (e) {
  const uploadModal = document.getElementById('uploadModal');
  const deleteModal = document.getElementById('deleteModal');

  if (e.target === uploadModal) {
    closeUploadModal();
  }
  if (e.target === deleteModal) {
    closeDeleteModal();
  }
});

// Notification function
function showNotification(message, type = 'info') {
  // Remove existing notifications
  const existingNotifications = document.querySelectorAll('.notification');
  existingNotifications.forEach(n => n.remove());

  const notification = document.createElement('div');
  notification.className = `notification notification-${type}`;
  notification.textContent = message;

  // Styles for notification
  notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        color: white;
        font-weight: 600;
        z-index: 10000;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        animation: slideIn 0.3s ease;
        max-width: 300px;
    `;

  // Set background color based on type
  switch (type) {
    case 'success':
      notification.style.background = 'linear-gradient(135deg, #10b981 0%, #059669 100%)';
      break;
    case 'error':
      notification.style.background = 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)';
      break;
    default:
      notification.style.background = 'linear-gradient(135deg, #00b7ff 0%, #00a0e6 100%)';
  }

  document.body.appendChild(notification);

  // Auto remove after 3 seconds
  setTimeout(() => {
    notification.style.animation = 'slideOut 0.3s ease';
    setTimeout(() => notification.remove(), 300);
  }, 3000);
}

// Add CSS animation for notifications
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(100%);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideOut {
        from {
            opacity: 1;
            transform: translateX(0);
        }
        to {
            opacity: 0;
            transform: translateX(100%);
        }
    }
`;
document.head.appendChild(style);

// Row hover effects
document.querySelectorAll('.table tbody tr:not(.empty-row)').forEach(row => {
  row.addEventListener('mouseenter', function () {
    this.style.transform = 'translateY(-2px)';
  });

  row.addEventListener('mouseleave', function () {
    this.style.transform = 'translateY(0)';
  });
});

// Image placeholder hover effects
document.querySelectorAll('.image-placeholder').forEach(img => {
  img.addEventListener('mouseenter', function () {
    this.style.transform = 'scale(1.2) rotate(5deg)';
  });

  img.addEventListener('mouseleave', function () {
    this.style.transform = 'scale(1) rotate(0deg)';
  });
});

// Escape key to close modals
document.addEventListener('keydown', function (e) {
  if (e.key === 'Escape') {
    closeUploadModal();
    closeDeleteModal();
  }
});