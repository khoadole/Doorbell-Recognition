document.getElementById('dateSearch').valueAsDate = new Date();

document.querySelectorAll('.table tbody tr:not(.empty-row)').forEach(row => {
  row.addEventListener('click', function () {
    // Remove active class from all rows
    document.querySelectorAll('.table tbody tr').forEach(r => r.classList.remove('active'));
    // Add active class to clicked row
    this.classList.add('active');
  });
});

document.querySelectorAll('.image-placeholder').forEach(img => {
  img.addEventListener('mouseenter', function () {
    this.style.transform = 'scale(1.2) rotate(5deg)';
  });

  img.addEventListener('mouseleave', function () {
    this.style.transform = 'scale(1) rotate(0deg)';
  });
});

document.querySelectorAll('.pagination-btn').forEach(btn => {
  btn.addEventListener('click', function () {
    if (!this.textContent.includes('Previous') && !this.textContent.includes('Next')) {
      document.querySelectorAll('.pagination-btn').forEach(b => b.classList.remove('active'));
      this.classList.add('active');
    }
  });
});