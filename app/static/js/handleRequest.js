// Hàm gửi yêu cầu POST với tham số 'cmd'
function sendPostRequest(command) {
    fetch('/api/v1/device/control', { // Thay thế URL bằng URL server của bạn
        method: 'POST',
        headers: {
            'Content-Type': 'application/json' // Định dạng dữ liệu là JSON
        },
        body: JSON.stringify({ 'cmd': command }) // Chuyển tham số 'cmd' thành JSON
    })
    .then(response => response.json())
    .then(data => {
        console.log('Response:', data); // In ra phản hồi từ server
    })
    .catch((error) => {
        console.error('Error:', error); // Bắt lỗi nếu có lỗi xảy ra
    });
}