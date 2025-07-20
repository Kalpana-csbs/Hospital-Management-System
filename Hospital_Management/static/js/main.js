document.addEventListener('DOMContentLoaded', function() {
    // Add form animations
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            this.classList.add('form-submitted');
            setTimeout(() => {
                this.submit();
            }, 500);
        });
    });

    // Add button click animations
    const buttons = document.querySelectorAll('button');
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            this.classList.add('button-clicked');
            setTimeout(() => {
                this.classList.remove('button-clicked');
            }, 200);
        });
    });

    // Edit row animation
    window.editRow = function(id) {
        const row = document.querySelector(`tr[data-id="${id}"]`);
        row.classList.add('row-editing');
        setTimeout(() => {
            row.classList.remove('row-editing');
        }, 500);
    };

    // Delete row animation
    window.deleteRow = function(id, url) {
        const row = document.querySelector(`tr[data-id="${id}"]`);
        if (confirm('Are you sure you want to delete this record?')) {
            row.classList.add('row-deleting');
            setTimeout(() => {
                fetch(url, { method: 'DELETE' })
                    .then(() => {
                        row.classList.add('row-deleted');
                        setTimeout(() => {
                            row.remove();
                        }, 300);
                    });
            }, 300);
        }
    };
});
