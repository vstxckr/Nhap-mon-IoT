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
