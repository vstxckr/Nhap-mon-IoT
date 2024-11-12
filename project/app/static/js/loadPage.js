function loadPage(page, className) {
    // Ẩn tất cả các phần nội dung trướcmenu
    page += '-content'
    document.querySelectorAll('.content-section').forEach(section => {
        section.style.display = 'none';
    });

    // Hiển thị phần tương ứng với trang yêu cầu
    const targetElement = document.getElementById(page);
    if (targetElement) {
        targetElement.style.display = 'block';
    } else {
        console.error('Page not found:', page);
    }
}


function loadAllPages() {
    const pages = ['home', 'data_sensor', 'action_history', 'profile', 'bai5']; // Danh sách các trang cần tải

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
                    if (page === 'bai5') {
                        createChart2()
                        loadChart2()
                    }
                } else {
                    console.error(`Element with class ${page} not found.`);
                }
            })
            .catch(error => console.error('Error loading page:', error));
    });
}