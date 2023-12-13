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