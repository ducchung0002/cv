let email = document.getElementById("email");
let password = document.getElementById("password");
email.value = localStorage.getItem("email");
password.value = localStorage.getItem("password");

function login() {
    let data = {
        email: email.value,
        password: password.value
    }

    axios.post("http://127.0.0.1:5000/enterprise/login", data)
        .then((response) => {
            if (response.data["success"] === true) {
                localStorage.setItem("email", email.value);
                localStorage.setItem("password", password.value);
                localStorage.setItem("access_token", response.data["access_token"]);
                if(response.data["role"] === 0)
                    window.location.replace("index.html");
                else 
                    window.location.replace("admin.html");
            } else {
                alert("Tài khoản không tồn tại!");
            }
        })
        .catch((error) => {
            console.error(`Error: ${error}`);
        });
}