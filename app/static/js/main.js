// Kết nối đến server Socket.IO
var old = 0;
var current = 1;
// Generate time labels for a full day (every hour)
let satisfactionCtx 
let satisfactionChart 
let global_data = {fan: 0, light: 0, air: 0, all: 0};

const socket = io('http://localhost:5002'); // Thay đổi địa chỉ nếu server của bạn chạy trên cổng khác
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
        const modifiedJsonString = `[${data.trim().slice(0, -1)}]`;
    
        // Chuyển đổi chuỗi JSON thành một mảng đối tượng JSON
        const jsonArray = JSON.parse(modifiedJsonString);
    
        // Giới hạn số lượng cột không quá 30
        const limitedData = jsonArray.slice(-30); // Lấy 30 mục cuối
    
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


function createEventListenerButton() {
    /* -----------------------all on off------------------------ */
    document.getElementById('all-switch').addEventListener('change', function () {
        if (global_data.air == 0) {
            this.checked = false;
            sendPostRequest("all on"); // Gọi hàm gửi yêu cầu POST với tham số cmd
        } else {
            this.checked = true;
            sendPostRequest("all off"); // Gọi hàm gửi yêu cầu POST với tham số cmd
        }
    });
    /* -----------------------all on off------------------------ */

    /* -----------------------fan on off------------------------ */
    document.getElementById('fan-switch').addEventListener('change', function () {
        if (global_data.fan == 0)
        {
            this.checked = false;
            sendPostRequest("fan on"); // Gọi hàm gửi yêu cầu POST với tham số cmd
        }
        else if (global_data.fan == 1)
        {
            this.checked = true;
            sendPostRequest("fan off"); // Gọi hàm gửi yêu cầu POST với tham số cmd
        }
    });
    /* -----------------------fan on off------------------------ */

    /* -----------------------light on off------------------------ */
    // Lắng nghe sự kiện thay đổi của công tắc bóng đèn
    document.getElementById('light-switch').addEventListener('change', function () {
        if (global_data.light == 0) {
            this.checked = false;
            sendPostRequest("light on"); // Gọi hàm gửi yêu cầu POST với tham số cmd
        } else {
            this.checked = true;
            sendPostRequest("light off"); // Gọi hàm gửi yêu cầu POST với tham số cmd
        }
    });
    /* -----------------------light on off------------------------ */


    /* -----------------------air on off-------------------------- */
    document.getElementById('air-condition-switch').addEventListener('change', function () {
        if (global_data.air == 0) {
            this.checked = false;
            sendPostRequest("air on"); // Gọi hàm gửi yêu cầu POST với tham số cmd
        } else {
            this.checked = true;
            sendPostRequest("air off"); // Gọi hàm gửi yêu cầu POST với tham số cmd
        }
    });
    /* -----------------------air on off-------------------------- */
}

function loadAllPages() {
    const pages = ['home', 'data_sensor', 'action_history', 'profile']; // Danh sách các trang cần tải

    pages.forEach(page => {
        // Tạo đường dẫn đến file HTML
        // Fetch file HTML và nạp nội dung vào thẻ div tương ứng
        fetch(page)
            .then(response => {
                if (response.ok) {
                    return response.text();
                } else {
                    throw new Error(`Page not found: ${page}`);
                }
            })
            .then(data => {
                // Tìm phần tử tương ứng với class của page
                const targetElement = document.getElementById(`${page}-content`);
                if (targetElement) {
                    // Chèn nội dung HTML vào thẻ div tương ứng
                    targetElement.innerHTML = data;
                    if (page === 'home') {
                        createChart()
                        loadChart()
                    }
                } else {
                    console.error(`Element with class ${page} not found.`);
                }
            })
            .catch(error => console.error('Error loading page:', error));
    });
}


function calculateColor(baseColor, value, maxValue) {
    // Tính toán độ đậm màu dựa trên giá trị
    const intensity = Math.min(value / maxValue, 1); // Đảm bảo giá trị không vượt quá 1
    return `rgba(${baseColor}, ${intensity})`;
}


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



// Hàm cập nhật màu nền của các ô dữ liệu
function updateBoxColors(light, humidity, temperature) {
    const lightValue = light;
    const humidityValue = humidity;
    const temperatureValue = temperature;
    // console.log(lightValue);
    // console.log(humidityValue);
    // console.log(temperatureValue);


    // Cập nhật màu nền dựa trên giá trị của từng ô
    document.getElementById('light-box').style.backgroundColor = calculateColor('176, 197, 164', lightValue, 300);
    document.getElementById('humidity-box').style.backgroundColor = calculateColor('211, 118, 118', humidityValue, 100);
    document.getElementById('temperature-box').style.backgroundColor = calculateColor('241, 239, 153', temperatureValue, 45);
}

/* -----------------------air on off-------------------------- */
// document.addEventListener('DOMContentLoaded', () => {
//     // Đọc file JSON và cập nhật dữ liệu lên biểu đồ
// });

// Gọi hàm loadPage khi DOM đã sẵn sàng
document.addEventListener("DOMContentLoaded", function () {

    if (typeof satisfactionChart !== 'undefined') {
        loadChart()
    }
    fetch('/api/v1/sensor/pulldata')
    .then(response => response.text()) // Đọc file như một chuỗi text
    .then(data => {
        // Thêm [ vào đầu và ] vào cuối chuỗi JSON
        const modifiedJsonString = `[${data.trim().slice(0, -1)}]`;
        // Chuyển đổi chuỗi JSON thành một mảng đối tượng JSON
        console.log(modifiedJsonString);
        const jsonArray = JSON.parse(modifiedJsonString);

        current = jsonArray.length
        old = current
    });
    // Gắn sự kiện click cho tất cả các menu item
    document.querySelectorAll('.menu-item').forEach(item => {
        item.addEventListener('click', function (e) {
            e.preventDefault();  // Ngăn chặn sự kiện load lại trang
            const page = this.getAttribute('data-page');  // Lấy giá trị của data-page
            loadPage(page, '.main-content');  // Nạp trang tương ứng
        });
    });

    // Load trang mặc định ban đầu
    loadPage('home', '.main-content');
    createEventListenerButton()
})


// Nhận dữ liệu từ Socket.IO và cập nhật biểu đồ
socket.on('sensor_data', function (data) {
    global_data.fan = data.fan
    global_data.light = data.light
    global_data.air = data.air
    global_data.all = data.all

    if (data.fan != 1) {
        document.getElementById('fan-switch').checked = false;
        document.getElementById('fan-image').classList.remove('spin');
    } else {
        document.getElementById('fan-switch').checked = true;
        document.getElementById('fan-image').classList.add('spin');
    }

    if (data.light != 1) {
        document.getElementById('light-switch').checked = false;
        document.getElementById('lightbulb-image').src = "..\\static\\assets\\light_off.png"
    } else {
        document.getElementById('light-switch').checked = true;
        document.getElementById('lightbulb-image').src = "..\\static\\assets\\light_on.png"
    }

    if (data.air != 1) {
        document.getElementById('air-condition-switch').checked = false;
        document.getElementById('airconditioner-image').src = "..\\static\\assets\\air-conditioner_off.png"
    } else {
        document.getElementById('air-condition-switch').checked = true;
        document.getElementById('airconditioner-image').src = "..\\static\\assets\\air-conditioner_on.png"
    }

    if (data.all != 1) {
        document.getElementById('all-switch').checked = false;
        document.getElementById('all-image').src = "..\\static\\assets\\all_off.png"
    } else {
        document.getElementById('all-switch').checked = true;
        document.getElementById('all-image').src = "..\\static\\assets\\all_on.png"
    }

    //console.log('Received sensor data:', data);

    document.getElementById('light_level').textContent = data.light_level;
    document.getElementById('humidity').textContent = data.humidity;
    document.getElementById('temperature').textContent = data.temperature;

    updateBoxColors(data.light_level, data.humidity, data.temperature);

    

    // Xóa giá trị cũ nhất nếu vượt quá số lượng cần thiết (chỉ giữ 25 giá trị)
    fetch('/api/v1/sensor/pulldata')
    .then(response => response.text()) // Đọc file như một chuỗi text
    .then(data => {
        // Thêm [ vào đầu và ] vào cuối chuỗi JSON
        const modifiedJsonString = `[${data.trim().slice(0, -1)}]`;
        // Chuyển đổi chuỗi JSON thành một mảng đối tượng JSON
        //console.log(modifiedJsonString);
        const jsonArray = JSON.parse(modifiedJsonString);

        current = jsonArray.length
        if (current != old) {
            old = current
            const lastElement = jsonArray[current - 1];

            console.log(lastElement);
            satisfactionChart.data.labels.push(lastElement.timestamp)
            satisfactionChart.data.datasets[0].data.push(lastElement.light_level);
            satisfactionChart.data.datasets[1].data.push(lastElement.humidity);
            satisfactionChart.data.datasets[2].data.push(lastElement.temperature);

            // Cập nhật lại biểu đồ sau khi thêm dữ liệu từ file JSON
            if (satisfactionChart.data.datasets[0].data.length > 30) {
                satisfactionChart.data.labels.shift(lastElement.timestamp)
                satisfactionChart.data.datasets[0].data.shift();
                satisfactionChart.data.datasets[1].data.shift();
                satisfactionChart.data.datasets[2].data.shift();
            }
            console.log('updated')
            satisfactionChart.update();
        }

    })
    // Cập nhật lại biểu đồ
    satisfactionChart.update();
});

