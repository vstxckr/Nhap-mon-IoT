// Action log data and configurations
let actionLogs = [];  // Array to hold fetched action log data
let currentActionLogPage = 1;  // Current page for action logs
let actionLogsPerPage = 10;  // Default logs per page
let actionSortField = 'id';  // Default sort field for action logs
let actionSortOrder = 'desc';  // Default sort order for action logs
let queryActionSortOrder = 'lastest'

// Toggle between "latest" and "oldest" sorting for action logs
function toggleActionSortOrder() {
    const sortToggleButton = document.getElementById("actionSortToggle");
    queryActionSortOrder = queryActionSortOrder === 'lastest' ? 'oldest' : 'lastest';
    sortToggleButton.textContent = queryActionSortOrder.charAt(0).toUpperCase() + queryActionSortOrder.slice(1);
}


// Fetch action logs from the API
function fetchActionLogs() {
    fetch('/api/v1/device/status')
        .then(response => response.json())
        .then(data => {
            actionLogs = data;
            actionLogs = sortActionLogs(actionLogs);  // Sort fetched data
            applyAllActionFilters(actionLogs)
        })
        .catch(error => console.error('Error fetching action data:', error));
}

// Sort action logs by specified field and order
function sortActionLogs(data) {
    return data.sort((a, b) => {
        let comparison = 0;
        if (a[actionSortField] > b[actionSortField]) comparison = 1;
        else if (a[actionSortField] < b[actionSortField]) comparison = -1;
        return actionSortOrder === 'asc' ? comparison : -comparison;
    });
}

// Sort the action logs table when clicking on a header
function sortActionLogTable(field) {
    actionSortField = field;
    actionSortOrder = actionSortOrder === 'asc' ? 'desc' : 'asc';
    actionLogs = sortActionLogs(actionLogs);  // Sort the logs based on new settings
    renderFilteredActionLogTable(actionLogs);  // Update table display
    renderFilteredActionPagination(actionLogs);  // Update pagination
}

// Apply all filters to action logs
function applyAllActionFilters() {
    let filteredLogs = actionLogs;

    // Retrieve filter values
    const idFilter = document.getElementById('action-filter-id').value.toLowerCase();
    const timestampFilter = document.getElementById('action-filter-timestamp').value.toLowerCase();
    const topicFilter = document.getElementById('action-filter-topic').value.toLowerCase();
    const commandFilter = document.getElementById('action-filter-command').value.toLowerCase();
    const statusFilter = document.getElementById('action-filter-status').value.toLowerCase();

    // Apply each filter
    if (idFilter) filteredLogs = filteredLogs.filter(log => log.id && log.id.toString().toLowerCase().includes(idFilter));
    if (timestampFilter) filteredLogs = filteredLogs.filter(log => log.timestamp && log.timestamp.toLowerCase().includes(timestampFilter));
    if (topicFilter) filteredLogs = filteredLogs.filter(log => log.topic && log.topic.toLowerCase().includes(topicFilter));
    if (commandFilter) filteredLogs = filteredLogs.filter(log => log.command && log.command.toLowerCase().includes(commandFilter));
    if (statusFilter) filteredLogs = filteredLogs.filter(log => log.status && log.status.toLowerCase().includes(statusFilter));

    // Render filtered logs
    renderFilteredActionLogTable(filteredLogs);
    renderFilteredActionPagination(filteredLogs);
}

// Render filtered action logs with pagination
function renderFilteredActionLogTable(filteredLogs) {
    const tableBody = document.getElementById('actionLogTableBody');
    tableBody.innerHTML = '';  // Clear existing rows

    const start = (currentActionLogPage - 1) * actionLogsPerPage;
    const end = start + actionLogsPerPage;
    const paginatedLogs = filteredLogs.slice(start, end);
    /* new */
    paginatedLogs.forEach(log => {
        // Determine classes based on topic, command, and status values
        const topicClass = log.topic ? `topic-${log.topic.toLowerCase()}` : '';
        const commandClass = log.command ? `command-${log.command.toLowerCase()}` : '';
        const statusClass = log.status ? `status-${log.status.toLowerCase()}` : '';

        // Construct row with dynamic classes
        const row = `<tr>
            <td>${log.id}</td>
            <td>${log.timestamp || "N/A"}</td>
            <td class="${topicClass}">${log.topic || "N/A"}</td>
            <td class="${commandClass}">${log.command || "N/A"}</td>
            <td class="${statusClass}">${log.status || "N/A"}</td>
        </tr>`;
        tableBody.innerHTML += row;
    });
    /* new */

    // paginatedLogs.forEach(log => {
    //     const row = `<tr>
    //         <td>${log.id}</td>
    //         <td>${log.timestamp || "N/A"}</td>
    //         <td>${log.topic || "N/A"}</td>
    //         <td>${log.command || "N/A"}</td>
    //         <td>${log.status || "N/A"}</td>
    //     </tr>`;
    //     tableBody.innerHTML += row;
    // });
}

// Render pagination controls for action logs
function renderFilteredActionPagination(filteredLogs) {
    const pagination = document.getElementById('actionPagination');
    pagination.innerHTML = '';  // Clear previous controls

    const totalPages = Math.ceil(filteredLogs.length / actionLogsPerPage);
    const maxPagesToShow = 10;
    const startPage = Math.max(1, currentActionLogPage - Math.floor(maxPagesToShow / 2));
    const endPage = Math.min(totalPages, startPage + maxPagesToShow - 1);

    // Previous button
    const prevButton = document.createElement('button');
    prevButton.classList.add('page-link');
    prevButton.textContent = 'Previous';
    prevButton.disabled = currentActionLogPage === 1;
    prevButton.addEventListener('click', function () {
        if (currentActionLogPage > 1) {
            currentActionLogPage--;
            renderFilteredActionLogTable(filteredLogs);
            renderFilteredActionPagination(filteredLogs);
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
        if (i === currentActionLogPage) pageLink.classList.add('active');
        pageLink.addEventListener('click', function () {
            currentActionLogPage = i;
            renderFilteredActionLogTable(filteredLogs);
            renderFilteredActionPagination(filteredLogs);
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
    nextButton.disabled = currentActionLogPage === totalPages;
    nextButton.addEventListener('click', function () {
        if (currentActionLogPage < totalPages) {
            currentActionLogPage++;
            renderFilteredActionLogTable(filteredLogs);
            renderFilteredActionPagination(filteredLogs);
        }
    });
    pagination.appendChild(nextButton);
}

// Update logs per page based on dropdown selection
function changedActionLogPerPage() {
    const logsPerPageSelect = document.getElementById('actionLogsPerPageSelect');
    actionLogsPerPage = parseInt(logsPerPageSelect.value);
    currentActionLogPage = 1;  // Reset to first page
    renderFilteredActionLogTable(actionLogs);
    renderFilteredActionPagination(actionLogs);
}

// Fetch action logs from the API with the updated type parameter
function queryActionFromDB() {
    // Set the current page to 1 for a new query
    currentActionLogPage = 1;

    // Get values from date range inputs
    const startDate = document.getElementById("actionStartDate").value;
    const endDate = document.getElementById("actionEndDate").value;

    // Get values from filter inputs
    const idFilter = document.getElementById("action-id-query-db-box").value.trim();
    const timestampFilter = document.getElementById("action-timestamp-query-db-box").value.trim();
    const topicFilter = document.getElementById("action-topic-query-db-box").value.trim();
    const commandFilter = document.getElementById("action-command-query-db-box").value.trim();
    const statusFilter = document.getElementById("action-status-query-db-box").value.trim();

    // Get other options from UI elements
    const sortOrder = document.getElementById("actionSortToggle").textContent === "Lastest" ? "latest" : "oldest";
    console.log(document.getElementById("actionSortToggle"))
    console.log(sortOrder)
    const numberOfRecords = parseInt(document.getElementById("actionTopicName").value) || 100;  // Number of records to retrieve
    actionrealtime = 1; // Turn on real-time mode
    setActionRealTime();

    // Prepare filter data
    const filters = {
        id: idFilter,
        timestamp: timestampFilter,
        topic: topicFilter,
        command: commandFilter,
        status: statusFilter
    };

    // API request payload
    const payload = {
        type: "actionLog",  // Specify type as "actionLog" for action logs
        startDate: startDate || null,
        endDate: endDate || null,
        sort: sortOrder,
        numberOfRecords: numberOfRecords,
        filters: filters
    };
    console.log(payload);

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
        actionLogs = data;  // Store the fetched action logs
        console.log(data);
        renderFilteredActionLogTable(data);  // Render the table with filtered action logs
        renderFilteredActionPagination(data);  // Render pagination for the action logs
    })
    .catch(error => console.error("Error querying action data:", error));
}

function clearActionFilter() {
        document.getElementById('action-filter-id').value = '';
        document.getElementById('action-filter-timestamp').value = '';
        document.getElementById('action-filter-topic').value = '';
        document.getElementById('action-filter-command').value = '';
        document.getElementById('action-filter-status').value = '';
        
        actionLogs = sortActionLogs(actionLogs);  // Sort fetched data
        applyAllActionFilters(actionLogs)
}