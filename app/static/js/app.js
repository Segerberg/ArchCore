

        // Check for the stored mode on page load
    document.addEventListener('DOMContentLoaded', function () {
      const savedMode = localStorage.getItem('mode');
      if (savedMode) {
        document.body.classList.add(savedMode);
      }
    });

    function toggleMode() {
      const body = document.body;

      body.classList.toggle('dark-mode');

      // Save the current mode to localStorage
      const currentMode = body.classList.contains('dark-mode') ? 'dark-mode' : '';
      localStorage.setItem('mode', currentMode);
    }