function createChart() {
    satisfactionCtx = document.getElementById('satisfaction-chart').getContext('2d');
    satisfactionChart = new Chart(satisfactionCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [
                {
                    label: 'Light Intensity',
                    data: [],
                    borderColor: '#B0C5A4',
                    fill: true,
                    backgroundColor: 'rgba(176, 197, 164, 0.1)'
                },
                {
                    label: 'Moisture',
                    data: [],
                    borderColor: '#D37676',
                    fill: true,
                    backgroundColor: 'rgba(211, 118, 118, 0.1)'
                },
                {
                    label: 'Temperature',
                    data: [],
                    borderColor: '#F1EF99',
                    fill: true,
                    backgroundColor: 'rgba(241, 239, 153, 0.1)'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

function loadChart() {
    fetch('/api/v1/sensor/pulldata')
    .then(response => response.text()) // Đọc file như một chuỗi text
    .then(data => {
        // Thêm [ vào đầu và ] vào cuối chuỗi JSON
        // const modifiedJsonString = `[${data.trim().slice(0, -1)}]`;
    
        // Chuyển đổi chuỗi JSON thành một mảng đối tượng JSON
        const jsonArray = JSON.parse(data);
    
        // Giới hạn số lượng cột không quá 30
        const limitedData = jsonArray.slice(-40); // Lấy 30 mục cuối
    
        // Sử dụng limitedData để cập nhật biểu đồ
        limitedData.forEach(item => {
            // Thêm timestamp vào nhãn của biểu đồ
            satisfactionChart.data.labels.push(item.timestamp);
        
            // Thêm dữ liệu vào từng dataset
            satisfactionChart.data.datasets[0].data.push(item.light_level);
            satisfactionChart.data.datasets[1].data.push(item.humidity);
            satisfactionChart.data.datasets[2].data.push(item.temperature);
        });
    
        // Cập nhật lại biểu đồ sau khi thêm dữ liệu từ file JSON
        satisfactionChart.update();
    })
    .catch(error => console.error('Error reading JSON file:', error));
}