
// join general whatsapp group modal
const modals = document.querySelectorAll('.static-modal');

modals.forEach(modal => {
    // Show the modal after 5 seconds
    const showModalTimeout = setTimeout(() => {
        modal.classList.remove('hidden');
    }, 5000);

    // Add event listeners to close the modal
    const closeButtons = modal.querySelectorAll('.close-modal-btn');
    closeButtons.forEach(button => {
        button.addEventListener('click', () => {
            clearTimeout(showModalTimeout);
            modal.classList.add('hidden');
        });
    });

    const cancelButton = modal.querySelector('.cancel-btn');
    cancelButton.addEventListener('click', () => {
        clearTimeout(showModalTimeout);
        modal.classList.add('hidden');
    });
});

//script for both inspo and image details
function sendWhatsAppMessage(imageUrl) {
    var phoneNumber = "+2348139425458"; // Replace with your phone number
    var defaultText = "Thank you for contacting Jume Mega wears & Accessories. For all your unisex wears we have got you covered. --Quality is our Watch World--\n"; // Include newline character directly in the string
    var message = defaultText + imageUrl;
    window.location.href = "https://wa.me/" + phoneNumber + "/?text=" + encodeURIComponent(message);
}

//for messages
document.addEventListener('DOMContentLoaded', (event) => {
    const toasts = document.querySelectorAll('[id^="toast-"]');
    toasts.forEach((toast) => {
        setTimeout(() => {
            toast.remove();
        }, 5000); // Dismiss after 5 seconds
    });
});


//next
