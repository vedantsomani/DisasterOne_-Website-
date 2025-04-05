document.querySelectorAll('.progress-bar').forEach(bar => {
    let width = bar.getAttribute('aria-valuenow');
    bar.style.width = '0%';
    setTimeout(() => {
      bar.style.width = width + '%';
    }, 500);
  });
  