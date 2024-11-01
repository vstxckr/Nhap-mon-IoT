function calculateColor(baseColor, value, maxValue) {
    // Tính toán độ đậm màu dựa trên giá trị
    const intensity = Math.min(value / maxValue, 1); // Đảm bảo giá trị không vượt quá 1
    return `rgba(${baseColor}, ${intensity})`;
}

// Hàm cập nhật màu nền của các ô dữ liệu
function updateBoxColors(light, humidity, temperature) {
    const lightValue = light;
    const humidityValue = humidity;
    const temperatureValue = temperature;


    // Cập nhật màu nền dựa trên giá trị của từng ô
    document.getElementById('light-box').style.backgroundColor = calculateColor('176, 197, 164', lightValue, 300);
    document.getElementById('humidity-box').style.backgroundColor = calculateColor('211, 118, 118', humidityValue, 100);
    document.getElementById('temperature-box').style.backgroundColor = calculateColor('241, 239, 153', temperatureValue, 45);
}