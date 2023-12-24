function convert_python_date_format(py_date) {
    if (py_date !== null) {
        let date = new Date(py_date);
        let year = date.getUTCFullYear();
        let month = ("0" + (date.getUTCMonth() + 1)).slice(-2); // Months are 0-indexed in JavaScript
        let day = ("0" + date.getUTCDate()).slice(-2);
        return `${year}-${month}-${day}`;
    }
    return "";
}

async function showImage(image_source) {
    let largeImageDiv = document.getElementById('largeImageDiv');
    let largeImage = document.getElementById('largeImage');

    // Set the source of the large image to be the same as the small image
    largeImage.src = image_source;

    largeImageDiv.style.display = 'block';
}

async function hide_large_image_show() {
    let largeImageDiv = document.getElementById('largeImageDiv');
    largeImageDiv.style.display = 'none';
}