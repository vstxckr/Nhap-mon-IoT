// Gọi hàm loadPage khi DOM đã sẵn sàng
document.addEventListener("DOMContentLoaded", function () {

    if (typeof satisfactionChart !== 'undefined') {
        loadChart()
    }
    if (typeof sastifactionChart2 !== 'undefined') {
        createChart2()
    }
    fetch('/api/v1/sensor/pulldata')
    .then(response => response.text()) // Đọc file như một chuỗi text
    .then(data => {
        // Thêm [ vào đầu và ] vào cuối chuỗi JSON
        // const modifiedJsonString = `[${data.trim().slice(0, -1)}]`;
        // Chuyển đổi chuỗi JSON thành một mảng đối tượng JSON
        // console.log(modifiedJsonString);
        const jsonArray = JSON.parse(data);
                // Kiểm tra xem jsonArray có phần tử nào không
        if (jsonArray.length > 0) {
            // Lấy timestamp của phần tử cuối cùng
            const lastTimestamp = jsonArray[jsonArray.length - 1].timestamp;
            old = lastTimestamp; // Gán timestamp vào biến current
        } else {
            console.log("Mảng JSON trống, không có timestamp để lấy.");
        }
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


function createEventListenerButton() {
    if (isEventListenerAttached) return;  // Nếu sự kiện đã gắn, không chạy lại hàm này
    /* -----------------------all on off------------------------ */
    const intervalId1 = setInterval(() => {
        const allSwitch = document.getElementById('all-switch');
        
        if (allSwitch) {
            allSwitch.addEventListener('change', function () {
                if (global_data.all == 0) {
                    this.checked = false;
                    sendPostRequest("all on"); // Gọi hàm gửi yêu cầu POST với tham số cmd
                } else {
                    this.checked = true;
                    sendPostRequest("all off"); // Gọi hàm gửi yêu cầu POST với tham số cmd
                }
            });

            // Khi đã tìm thấy và gắn sự kiện, dừng interval
            clearInterval(intervalId1);
            console.log("Đã tìm thấy 'all-switch' và gắn sự kiện thành công.");
        }
    }, 1000); // Kiểm tra mỗi 100ms
    /* -----------------------all on off------------------------ */

    /* -----------------------fan on off------------------------ */

    const intervalId2 = setInterval(() => {
        const fanSwitch = document.getElementById('fan-switch');
        
        if (fanSwitch) {
            fanSwitch.addEventListener('change', function () {
                if (global_data.fan == 0) {
                    this.checked = false;
                    sendPostRequest("fan on"); // Gọi hàm gửi yêu cầu POST với tham số cmd
                } else {
                    this.checked = true;
                    sendPostRequest("fan off"); // Gọi hàm gửi yêu cầu POST với tham số cmd
                }
            });

            // Khi đã tìm thấy và gắn sự kiện, dừng interval
            clearInterval(intervalId2);
            console.log("Đã tìm thấy 'fan-switch' và gắn sự kiện thành công.");
        }
    }, 1000); // Kiểm tra mỗi 100ms
    /* -----------------------fan on off------------------------ */

    /* -----------------------air on off------------------------ */
    // Lắng nghe sự kiện thay đổi của công tắc bóng đèn
    const intervalId3 = setInterval(() => {
        const airSwitch = document.getElementById('air-condition-switch');
        
        if (airSwitch) {
            airSwitch.addEventListener('change', function () {
                if (global_data.air == 0) {
                    this.checked = false;
                    sendPostRequest("air on"); // Gọi hàm gửi yêu cầu POST với tham số cmd
                } else {
                    this.checked = true;
                    sendPostRequest("air off"); // Gọi hàm gửi yêu cầu POST với tham số cmd
                }
            });

            // Khi đã tìm thấy và gắn sự kiện, dừng interval
            clearInterval(intervalId3);
            console.log("Đã tìm thấy 'air-condition-switch' và gắn sự kiện thành công.");
        }
    }, 1000); // Kiểm tra mỗi 100ms
    /* -----------------------air on off------------------------ */


    /* -----------------------light on off-------------------------- */
    const intervalId4 = setInterval(() => {
        const lightSwitch = document.getElementById('light-switch');
        
        if (lightSwitch) {
            lightSwitch.addEventListener('change', function () {
                if (global_data.light == 0) {
                    this.checked = false;
                    sendPostRequest("light on"); // Gọi hàm gửi yêu cầu POST với tham số cmd
                } else {
                    this.checked = true;
                    sendPostRequest("light off"); // Gọi hàm gửi yêu cầu POST với tham số cmd
                }
            });

            // Khi đã tìm thấy và gắn sự kiện, dừng interval
            clearInterval(intervalId4);
            console.log("Đã tìm thấy 'light-switch' và gắn sự kiện thành công.");
        }
    }, 1000); // Kiểm tra mỗi 100ms
    /* -----------------------light on off-------------------------- */

    isEventListenerAttached = true;  // Đặt cờ thành true để ngăn gọi lại

}