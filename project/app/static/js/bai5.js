let threshold = 80
let nChartItems = 20
function createChart2() {
    satisfactionCtx2 = document.getElementById('satisfaction-chart2').getContext('2d');
    satisfactionChart2 = new Chart(satisfactionCtx2, {
        type: 'line',
        data: {
            labels: [],
            datasets: [
                {
                    label: 'Light Intensity',
                    data: [],
                    borderColor: '#1f93db',
                    fill: true,
                    backgroundColor: 'rgba(170, 219, 250, 0.5)'
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

function triggerAlert(message) {
    const alertBox = document.getElementById("alert-box");
    const alertContent = document.getElementById("alert-content");
    document.getElementById("wind-sensor").classList.add("text-red")
    // Hiển thị thông báo
    fetch("/api/v1/log/query", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({type: 'statistic', thres: threshold})
    })
    .then(response => response.json())
    .then(data => {
        if (data)
            alertContent.innerHTML = `<h1>${message}</h1><h1>Count: ${data}</h1>`;
        else 
            alertContent.innerHTML = `<h1>${message}</h1><h1>Count: N/A</h1>`;
    })
    .catch(error => console.error("Error querying sensor data:", error));

    // Thêm class nhấp nháy đỏ để tạo hiệu ứng
    alertBox.classList.add("flash-red");
}


// Ví dụ: Kiểm tra điều kiện và gọi hàm cảnh báo
function checkCondition() {
    const windspeed = parseInt(document.getElementById("wind-sensor").textContent) || 0;
    if (windspeed > threshold) { // Điều kiện ví dụ
        triggerAlert("Wind speed is high!");
    } else {
        let message = "Wind speed is normal"
        const alertBox = document.getElementById("alert-box");
        const alertContent = document.getElementById("alert-content");
        alertContent.innerHTML = `<h1>${message}</h1>`
        alertBox.classList.remove("flash-red")
        document.getElementById("wind-sensor").classList.remove("text-red")
    }
}

// Kiểm tra điều kiện mỗi 3 giây
setInterval(checkCondition, 50);

function loadChart2() {
    fetch('/api/v1/sensor/pulldata?wind_speed=1&thres='+nChartItems)
    .then(response => response.text()) // Đọc file như một chuỗi text
    .then(data => {
        // Thêm [ vào đầu và ] vào cuối chuỗi JSON
        // const modifiedJsonString = `[${data.trim().slice(0, -1)}]`;
    
        // Chuyển đổi chuỗi JSON thành một mảng đối tượng JSON
        const jsonArray = JSON.parse(data);
    
        // Giới hạn số lượng cột không quá 30
        const limitedData = jsonArray.slice(-nChartItems); // Lấy 30 mục cuối
    
        // Sử dụng limitedData để cập nhật biểu đồ
        limitedData.forEach(item => {
            // Thêm timestamp vào nhãn của biểu đồ
            satisfactionChart2.data.labels.push(item.timestamp);
        
            // Thêm dữ liệu vào từng dataset
            satisfactionChart2.data.datasets[0].data.push(item.wind_speed);
        });
    
        // Cập nhật lại biểu đồ sau khi thêm dữ liệu từ file JSON
        satisfactionChart2.update();
    })
    .catch(error => console.error('Error reading JSON file:', error));
}