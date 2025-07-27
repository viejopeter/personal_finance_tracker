document.addEventListener('DOMContentLoaded', function () {
    setTimeout(function () {
        const message = document.querySelectorAll('.message');
        message.forEach(function (message) {
            message.classList.remove('show'); // Triggers Bootstrap fade
            message.classList.add('fade');    // Ensure fade effect is applied
            setTimeout(function () {
                message.remove(); // Remove from DOM
            }, 500); // Matches Bootstrap's fade transition duration
        });
    }, 3000); // 3 seconds delay
});
