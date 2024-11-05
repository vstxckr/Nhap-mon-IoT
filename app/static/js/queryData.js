let actionrealtime = 0
let sensorrealtime = 0

function toggleActionRealTime() {
    if (actionrealtime == 1) {
        actionrealtime = 0
        // document.getElementById('actionStartDate').value = '';
        // document.getElementById('actionEndDate').value = '';

        // Clear individual field filters
        document.getElementById('action-id-query-db-box').value = '';
        document.getElementById('action-timestamp-query-db-box').value = '';
        document.getElementById('action-topic-query-db-box').value = '';
        document.getElementById('action-command-query-db-box').value = '';
        document.getElementById('action-status-query-db-box').value = '';
        currentActionLogPage=1
    } else {
        actionrealtime = 1
        currentActionLogPage=1
    }
    setActionRealTime()
}

function setActionRealTime() {
    // Toggle the value of actionrealtime between 0 and 1
    // Update the button color based on the value of actionrealtime
    const actionRTButton = document.getElementById('actionRT');
    if (actionrealtime === 0) {
        actionRTButton.style.backgroundColor = 'red';
        actionRTButton.textContent = 'Real-Time: ON';  // Optional: Change button text
    } else {
        actionRTButton.style.backgroundColor = 'green';
        actionRTButton.textContent = 'Real-Time: OFF';  // Optional: Change button text
    }
}

function toggleSensorRealTime() {
    if (sensorrealtime == 1) {
        sensorrealtime = 0
        // Clear date filters
        // document.getElementById('sensorStartDate').value = '';
        // document.getElementById('sensorEndDate').value = '';

        // Clear individual field filters
        document.getElementById('id-query-db-box').value = '';
        document.getElementById('timestamp-query-db-box').value = '';
        document.getElementById('light-level-query-db-box').value = '';
        document.getElementById('humidity-query-db-box').value = '';
        document.getElementById('temperature-query-db-box').value = '';
        // document.getElementById('sensorTopicName').value = '';
        currentSensorLogPage=1
    } else {
        sensorrealtime = 1
        currentSensorLogPage=1
    }
    setSensorRealTime()
}

function setSensorRealTime() {
    // Toggle the value of actionrealtime between 0 and 1
    // Update the button color based on the value of actionrealtime
    const sensorRTButton = document.getElementById('sensorRT');
    if (sensorrealtime === 0) {
        sensorRTButton.style.backgroundColor = 'red';
        sensorRTButton.textContent = 'Real-Time: ON';  // Optional: Change button text
    } else {
        sensorRTButton.style.backgroundColor = 'green';
        sensorRTButton.textContent = 'Real-Time: OFF';  // Optional: Change button text
    }
}