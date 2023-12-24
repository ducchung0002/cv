async function login() {
    const email = document.getElementById("email");
    const password = document.getElementById("password");

    let data = {
        email: email.value,
        password: password.value
    }

    axios.post("http://127.0.0.1:5000/applicant/login", data)
        .then(response => {
            if (response.data["success"] === true) {
                localStorage.setItem("email", email.value);
                localStorage.setItem("password", password.value);
                localStorage.setItem("access_token", response.data["access_token"]);
                window.location.replace("/../FrontEnd/applicant/index.html");
            } else {
                alert("Tài khoản không tồn tại!: " + password.value);

            }
        })
        .catch((error) => {
            console.error(`Error: ${error}`);
        });
}