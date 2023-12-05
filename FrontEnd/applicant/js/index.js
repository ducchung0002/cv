


axios.get('http://127.0.0.1:5000/')
    .then(response => {
        document.getElementById("test1").innerText = response.data["message"]
    })
    .catch(error => {
        console.error('Error:', error);
    });

axios.get('http://127.0.0.1:5000/applicant')
    .then(response => {
        document.getElementById("test2").innerText = response.data["message"]
    })
    .catch(error => {
        console.error('Error:', error);
    });