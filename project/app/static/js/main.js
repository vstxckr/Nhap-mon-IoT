// Kết nối đến server Socket.IO
var old = 0;
var current = 1;
// Generate time labels for a full day (every hour)
let satisfactionCtx 
let satisfactionChart 
let satisfactionCtx2
let satisfactionChart2
let global_data = {fan: 0, light: 0, air: 0, all: 0, wind: 0};
let isEventListenerAttached = false;  // Cờ để kiểm tra xem sự kiện đã được gắn chưa


const socket = io('http://localhost:5002'); // Thay đổi địa chỉ nếu server của bạn chạy trên cổng khác


// Nhận dữ liệu từ Socket.IO và cập nhật biểu đồ
socket.on('sensor_data', function (data) {
    global_data.fan = data.fan
    global_data.light = data.light
    global_data.air = data.air
    global_data.all = data.all
    global_data.wind = data.wind_speed

    if (actionrealtime == 0) {
        fetchActionLogs()
    }
    if (sensorrealtime == 0) {
        fetchSensorLogs()
    }
    setActionRealTime()
    setSensorRealTime()

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

    /* ---------------------update bai5------------------------  */
    document.getElementById('wind-sensor').textContent = data.wind_speed;
    // Cập nhật lại biểu đồ sau khi thêm dữ liệu từ file JSON
    satisfactionChart2.data.datasets[0].data.push(global_data.wind)
    satisfactionChart2.data.labels.push(data.timestamp)
    if (satisfactionChart2.data.datasets[0].data.length > 20) {
        satisfactionChart2.data.datasets[0].data.shift()
        satisfactionChart2.data.labels.shift()
    }
    else {
    }
    satisfactionChart2.update()

    /* ---------------------update bai5------------------------  */

    // Xóa giá trị cũ nhất nếu vượt quá số lượng cần thiết (chỉ giữ 25 giá trị)
    fetch('/api/v1/sensor/pulldata')
    .then(response => response.text()) // Đọc file như một chuỗi text
    .then(data => {
        // Thêm [ vào đầu và ] vào cuối chuỗi JSON
        // const modifiedJsonString = `[${data.trim().slice(0, -1)}]`;
        // Chuyển đổi chuỗi JSON thành một mảng đối tượng JSON
        //console.log(modifiedJsonString);
        // console.log(data)
        const jsonArray = JSON.parse(data);

        current = jsonArray[jsonArray.length - 1].timestamp;
        // console.log('current is '+current +' and old is :' + old)
        if (current != old) {
            old = current
            const lastElement = jsonArray[jsonArray.length - 1];

            // console.log(lastElement);
            satisfactionChart.data.labels.push(lastElement.timestamp)
            satisfactionChart.data.datasets[0].data.push(lastElement.light_level);
            satisfactionChart.data.datasets[1].data.push(lastElement.humidity);
            satisfactionChart.data.datasets[2].data.push(lastElement.temperature);

            // Cập nhật lại biểu đồ sau khi thêm dữ liệu từ file JSON
            if (satisfactionChart.data.datasets[0].data.length > 40) {
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
