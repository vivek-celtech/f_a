$(document).ready(function () {
    // Function to get CSRF token from cookies
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Event listener for capture button click
    $('#capture-btn').click(function () {
        // Capture photo and send it via AJAX
        capturePhoto();
    });

    // Event listener for reload button click
    $('#reload-btn').click(function () {
        // Reload the page
        location.reload();
    });

    // Function to capture photo and send it via AJAX
    function capturePhoto() {
        const video = document.getElementById('video-element');
        const image = document.getElementById('img-element');

        navigator.mediaDevices.getUserMedia({ video: true })
            .then(function (stream) {
                video.srcObject = stream;

                const track = stream.getVideoTracks()[0];
                const imageCapture = new ImageCapture(track);

                imageCapture.takePhoto()
                    .then(function (blob) {
                        const img = new Image();
                        img.src = URL.createObjectURL(blob);
                        image.innerHTML = ''; // Clear previous images
                        image.appendChild(img);

                        const formData = new FormData();
                        formData.append('csrfmiddlewaretoken', getCookie('csrftoken'));
                        formData.append('photo', blob);

                        // Send AJAX request to classify the face
                        $.ajax({
                            type: 'POST',
                            url: '/login/', // Ensure this URL is correct
                            data: formData,
                            processData: false,
                            contentType: false,
                            success: function (response) {
                                console.log(response);
                                // Redirect to home page on success
                                window.location.href = '/';
                            },
                            error: function (xhr, status, error) {
                                console.error('Error sending AJAX request:', error);
                                console.error('Response:', xhr.responseText);
                            }
                        });
                    })
                    .catch(function (error) {
                        console.error('Error capturing photo:', error);
                    });
            })
            .catch(function (error) {
                console.error('Error accessing camera:', error);
            });
    }
});
