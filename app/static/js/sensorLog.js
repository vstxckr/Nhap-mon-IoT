let logs = [];  // Dữ liệu logs
let currentPage = 1;  // Trang hiện tại
let perPage = 10;  // Số lượng log mỗi trang, mặc định là 10
let sortField = 'id';  // Field sắp xếp mặc định
let sortOrder = 'asc';  // Thứ tự sắp xếp mặc định (asc: tăng dần, desc: giảm dần)


function fetchLogs() {
    fetch('/api/v1/sensor/pulldata?realtime=1&reverse=1')
        .then(response => response.json())
        .then(data => {
            logs = data;
            // console.log(logs)
            renderTable();
            renderPagination();
        })
        .catch(error => console.error('Error fetching data:', error));
}

// Hàm render bảng với logs phân trang
function renderTable() {
    const tableBody = document.getElementById('logTableBody');
    tableBody.innerHTML = '';

    // Lấy logs theo trang
    const start = (currentPage - 1) * perPage;
    const end = start + perPage;
    const paginatedLogs = logs.slice(start, end);

    paginatedLogs.forEach(log => {
        const row = `<tr>
            <td>${log.id}</td>
            <td>${log.timestamp || "N/A"}</td>
            <td>${log.light_level || "N/A"}</td>
            <td>${log.humidity || "N/A"}</td>
            <td>${log.temperature || "N/A"}</td>
        </tr>`;
        tableBody.innerHTML += row;
    });
}

// Hàm sắp xếp dữ liệu theo field và thứ tự
function sortLogs(data) {
    return data.sort((a, b) => {
        let comparison = 0;
        if (a[sortField] > b[sortField]) {
            comparison = 1;
        } else if (a[sortField] < b[sortField]) {
            comparison = -1;
        }
        return sortOrder === 'asc' ? comparison : -comparison;
    });
}

// Hàm sắp xếp bảng khi nhấn vào header
function sortTable(field) {
    if (sortField === field) {
        sortOrder = sortOrder === 'asc' ? 'desc' : 'asc';
    } else {
        sortField = field;
        sortOrder = 'asc';
    }
    renderTable();
}

// Hàm render phân trang
function renderPagination() {
    const pagination = document.getElementById('pagination');
    pagination.innerHTML = '';

    const totalPages = Math.ceil(logs.length / perPage);
    for (let i = 1; i <= totalPages; i++) {
        const pageLink = document.createElement('button');
        pageLink.classList.add('page-link');
        pageLink.textContent = i;

        // Gán lớp active cho trang hiện tại
        if (i === currentPage) {
            pageLink.classList.add('active');
        }

        pageLink.addEventListener('click', function () {
            currentPage = i;
            renderTable();
            renderPagination(); // Cập nhật lại phân trang sau khi thay đổi trang
        });
        pagination.appendChild(pageLink);
    }
}

// Hàm cập nhật số lượng log mỗi trang
function updatePerPage() {
    perPage = parseInt(document.getElementById('perPageSelect').value);
    currentPage = 1; // Reset về trang đầu tiên khi thay đổi số log mỗi trang
    renderTable();
    renderPagination();
}

// Hàm lọc logs theo tên thiết bị
function filterLogs() {
    const deviceName = document.getElementById('deviceName').value.toLowerCase();
    const filteredLogs = logs.filter(log => log.device && log.device.toLowerCase().includes(deviceName));
    renderFilteredTable(filteredLogs);
}

// Render bảng sau khi lọc
function renderFilteredTable(filteredLogs) {
    const tableBody = document.getElementById('logTableBody');
    tableBody.innerHTML = '';

    const start = (currentPage - 1) * perPage;
    const end = start + perPage;
    const paginatedLogs = sortLogs(filteredLogs).slice(start, end);

    paginatedLogs.forEach(log => {
        const row = `<tr>
            <td>${log.id}</td>
            <td>${log.timestamp || "N/A"}</td>
            <td>${log.light_level || "N/A"}</td>
            <td>${log.humidity || "N/A"}</td>
            <td>${log.temperature || "N/A"}</td>
        </tr>`;
        tableBody.innerHTML += row;
    });

    // Cập nhật phân trang sau khi lọc
    renderPagination();
}

function initializeDataSensor() {
    console.log("Initializing Data Sensor Page");
    fetchLogs(); // Hàm lấy dữ liệu từ API và khởi tạo bảng
}