const locationButton = document.getElementById('location');
const locationInput = document.getElementById('location_input');
const form = document.getElementById('attendance_form');

locationButton.addEventListener('click', () => {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            position => {
                const coords = `${position.coords.latitude},${position.coords.longitude}`;
                console.log('Vị trí:', coords); // Debug
                locationInput.value = coords;
                form.submit();
                alert('Chấm công bằng vị trí thành công!');
            },
            err => {
                console.error('Lỗi vị trí:', err.message); // Debug
                alert('Lỗi lấy vị trí: ' + err.message);
            },
            { enableHighAccuracy: true, timeout: 5000, maximumAge: 0 }
        );
    } else {
        console.error('Trình duyệt không hỗ trợ geolocation');
        alert('Trình duyệt không hỗ trợ lấy vị trí!');
    }
});