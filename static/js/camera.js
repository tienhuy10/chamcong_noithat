let video = document.getElementById('video');
let canvas = document.getElementById('canvas');
let preview = document.getElementById('preview');
let previewContainer = document.getElementById('preview-container');
let captureButton = document.getElementById('capture');
let confirmButton = document.getElementById('confirm');
let retakeButton = document.getElementById('retake');
let locationButton = document.getElementById('location');
let imageInput = document.getElementById('image_input');
let context = canvas.getContext('2d');

navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        video.srcObject = stream;
    })
    .catch(err => {
        console.error('Camera error:', err);
        locationButton.style.display = 'block';
    });

captureButton.addEventListener('click', () => {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    preview.src = canvas.toDataURL('image/jpeg');
    previewContainer.style.display = 'block';
    captureButton.style.display = 'none';
});

retakeButton.addEventListener('click', () => {
    previewContainer.style.display = 'none';
    captureButton.style.display = 'block';
});

confirmButton.addEventListener('click', () => {
    canvas.toBlob(blob => {
        let file = new File([blob], 'capture.jpg', { type: 'image/jpeg' });
        let dataTransfer = new DataTransfer();
        dataTransfer.items.add(file);
        imageInput.files = dataTransfer.files;
        document.getElementById('attendance_form').submit();
    }, 'image/jpeg');
});