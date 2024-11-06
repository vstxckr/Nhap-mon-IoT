let sensorLogs = [];  // Sensor log data
let currentSensorLogPage = 1;  // Current page for sensor logs
let sensorLogsPerPage = 10;  // Default logs per page for sensor logs
let sensorSortField = 'id';  // Default sort field for sensor logs
let sensorSortOrder = 'desc';  // Default sort order for sensor logs
let querySensorSortOrder = 'latest'; // Default sort order

// Toggle between "latest" and "oldest" sorting
function toggleSensorSortOrder() {
    const sortToggleButton = document.getElementById("sortToggle");
    querySensorSortOrder = querySensorSortOrder === 'latest' ? 'oldest' : 'latest';
    sortToggleButton.textContent = querySensorSortOrder.charAt(0).toUpperCase() + querySensorSortOrder.slice(1);
}



// Fetch sensor logs from the API
function fetchSensorLogs() {
    fetch('/api/v1/sensor/pulldata?realtime=1&reverse=1')
        .then(response => response.json())
        .then(data => {
            sensorLogs = data;
            console.log(data)
            sensorLogs = sortSensorLogs(sensorLogs);  // Sort the sensor logs based on the selected field and order
            applyAllFilters(sensorLogs)
        })
        .catch(error => console.error('Error fetching data:', error));
}


// Sort sensor logs by a specified field and order
function sortSensorLogs(data) {
    return data.sort((a, b) => {
        let comparison = 0;
        if (a[sensorSortField] > b[sensorSortField]) {
            comparison = 1;
        } else if (a[sensorSortField] < b[sensorSortField]) {
            comparison = -1;
        }
        return sensorSortOrder === 'asc' ? comparison : -comparison;
    });
}

// Sort the sensor logs table when clicking on a header
function sortSensorLogTable(field) {
    if (sensorSortField === field) {
        sensorSortOrder = sensorSortOrder === 'asc' ? 'desc' : 'asc';
    } else {
        sensorSortField = field;
        sensorSortOrder = 'asc';
    }
    sensorLogs = sortSensorLogs(sensorLogs);  // Sort the sensor logs based on the selected field and order
    renderFilteredSensorLogTable(sensorLogs);  // Re-render the table with sorted logs
    renderFilteredSensorPagination(sensorLogs);  // Update pagination after sorting
}

function changedLogPerPage() {
    currentSensorLogPage = 1
    applyAllFilters()
}

// Apply all filters to the sensor logs
function applyAllFilters() {
    let filteredLogs = sensorLogs;

    // Retrieve filter values from each visible filter box
    const idFilter = document.getElementById('sensor-filter-id').value.toLowerCase();
    const timestampFilter = document.getElementById('sensor-filter-timestamp').value.toLowerCase();
    const lightLevelFilter = document.getElementById('sensor-filter-light-level').value.toLowerCase();
    const humidityFilter = document.getElementById('sensor-filter-humidity').value.toLowerCase();
    const temperatureFilter = document.getElementById('sensor-filter-temperature').value.toLowerCase();
    // const startDate = document.getElementById('sensorStartDate').value;
    // const endDate = document.getElementById('sensorEndDate').value;

    // Apply each active filter
    if (idFilter) {
        filteredLogs = filteredLogs.filter(log => log.id && log.id.toString().toLowerCase().includes(idFilter));
    }
    if (timestampFilter) {
        filteredLogs = filteredLogs.filter(log => log.timestamp && log.timestamp.toLowerCase().includes(timestampFilter));
    }
    if (lightLevelFilter) {
        filteredLogs = filteredLogs.filter(log => log.light_level && log.light_level.toString().toLowerCase().includes(lightLevelFilter));
    }
    if (humidityFilter) {
        filteredLogs = filteredLogs.filter(log => log.humidity && log.humidity.toString().toLowerCase().includes(humidityFilter));
    }
    if (temperatureFilter) {
        filteredLogs = filteredLogs.filter(log => log.temperature && log.temperature.toString().toLowerCase().includes(temperatureFilter));
    }

    // Render the filtered logs table and pagination
    renderFilteredSensorLogTable(filteredLogs);
    renderFilteredSensorPagination(filteredLogs);
}

// Render filtered sensor logs with pagination
function renderFilteredSensorLogTable(filteredLogs) {
    sensorLogsPerPage = parseInt(document.getElementById('sensorLogsPerPageSelect').value);
    const tableBody = document.getElementById('sensorLogTableBody');
    tableBody.innerHTML = '';  // Clear existing table rows

    const start = (currentSensorLogPage - 1) * sensorLogsPerPage;
    const end = start + sensorLogsPerPage;
    const paginatedLogs = filteredLogs.slice(start, end);

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

function renderFilteredSensorPagination(filteredLogs) {
    const pagination = document.getElementById('sensorPagination');
    pagination.innerHTML = '';  // Clear previous pagination controls

    const totalPages = Math.ceil(filteredLogs.length / sensorLogsPerPage);
    const maxPagesToShow = 10;
    const startPage = Math.max(1, currentSensorLogPage - Math.floor(maxPagesToShow / 2));
    const endPage = Math.min(totalPages, startPage + maxPagesToShow - 1);

    // Previous button
    const prevButton = document.createElement('button');
    prevButton.classList.add('page-link');
    prevButton.textContent = 'Previous';
    prevButton.disabled = currentSensorLogPage === 1;
    prevButton.addEventListener('click', function () {
        if (currentSensorLogPage > 1) {
            currentSensorLogPage--;
            renderFilteredSensorLogTable(filteredLogs);
            renderFilteredSensorPagination(filteredLogs);
        }
    });
    pagination.appendChild(prevButton);

    // Ellipsis before current range if needed
    if (startPage > 1) {
        const ellipsis = document.createElement('span');
        ellipsis.textContent = '...';
        pagination.appendChild(ellipsis);
    }

    // Page numbers
    for (let i = startPage; i <= endPage; i++) {
        const pageLink = document.createElement('button');
        pageLink.classList.add('page-link');
        pageLink.textContent = i;

        if (i === currentSensorLogPage) {
            pageLink.classList.add('active');
        }

        pageLink.addEventListener('click', function () {
            currentSensorLogPage = i;
            renderFilteredSensorLogTable(filteredLogs);
            renderFilteredSensorPagination(filteredLogs);  // Update pagination to show active page
        });

        pagination.appendChild(pageLink);
    }

    // Ellipsis after current range if needed
    if (endPage < totalPages) {
        const ellipsis = document.createElement('span');
        ellipsis.textContent = '...';
        pagination.appendChild(ellipsis);
    }

    // Next button
    const nextButton = document.createElement('button');
    nextButton.classList.add('page-link');
    nextButton.textContent = 'Next';
    nextButton.disabled = currentSensorLogPage === totalPages;
    nextButton.addEventListener('click', function () {
        if (currentSensorLogPage < totalPages) {
            currentSensorLogPage++;
            renderFilteredSensorLogTable(filteredLogs);
            renderFilteredSensorPagination(filteredLogs);
        }
    });
    pagination.appendChild(nextButton);
}


function querySensorFromDB() {
    // Get values from date range inputs
    currentSensorLogPage = 1
    const startDate = document.getElementById("sensorStartDate").value;
    const endDate = document.getElementById("sensorEndDate").value;

    // Get values from filter inputs
    const idFilter = document.getElementById("id-query-db-box").value.trim();
    const timestampFilter = document.getElementById("timestamp-query-db-box").value.trim();
    const lightLevelFilter = document.getElementById("light-level-query-db-box").value.trim();
    const humidityFilter = document.getElementById("humidity-query-db-box").value.trim();
    const temperatureFilter = document.getElementById("temperature-query-db-box").value.trim();

    // Get other options from UI elements
    const sortOrder = document.getElementById("sortToggle").textContent === "Latest" ? "latest" : "oldest";
    const numberOfRecords = parseInt(document.getElementById("sensorTopicName").value) || 100;  // Number of records to retrieve
    sensorrealtime = 1
    setSensorRealTime()

    // const recordsPerPage = parseInt(document.getElementById("sensorLogsPerPageSelect").value) || 10;

    // Prepare filter data
    const filters = {
        id: idFilter,
        timestamp: timestampFilter,
        light_level: lightLevelFilter,
        humidity: humidityFilter,
        temperature: temperatureFilter
    };

    // API request payload
    const payload = {
        type: "sensorLog", // Assuming type "sensor" for sensor logs
        startDate: startDate || null,
        endDate: endDate || null,
        sort: sortOrder,
        numberOfRecords: numberOfRecords,
        filters: filters
    };
    console.log(payload)

    // Send POST request to the API
    fetch("/api/v1/log/query", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(data => {
        sensorLogs=data
        console.log(data)
        renderFilteredSensorLogTable(data);
        renderFilteredSensorPagination(data);
    })
    .catch(error => console.error("Error querying sensor data:", error));
}

function clearSensorFilter() {
    document.getElementById('sensor-filter-id').value = '';
    document.getElementById('sensor-filter-timestamp').value = '';
    document.getElementById('sensor-filter-light-level').value = '';
    document.getElementById('sensor-filter-humidity').value = '';
    document.getElementById('sensor-filter-temperature').value = '';
    sensorLogs = sortSensorLogs(sensorLogs);  // Sort the sensor logs based on the selected field and order
    applyAllFilters(sensorLogs)
}