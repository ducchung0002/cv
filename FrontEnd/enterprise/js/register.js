let name = document.getElementById("name")
let email = document.getElementById("email")
let role = document.getElementById("role")
let password = document.getElementById("password")
let confirm_password = document.getElementById("confirm_password")

function submit() {
    if (name.checkValidity() === false || name.value.trim().length === 0) {
        alert("Tên trống/khoảng trắng");
        return;
    }
    if (email.checkValidity() === false) {
        alert("Email không hợp lệ!");
        return;
    }
    if (password.checkValidity() === false) {
        alert("Mật khẩu không được trống!");
        return;
    }
    if (password.value !== confirm_password.value) {
        alert("Mật khẩu nhập lại không đúng!");
        return;
    }
    let data = {
        name: name.value,
        email: email.value,
        role: role.value,
        password: password.value
    }
    axios.post("http://127.0.0.1:5000/enterprise/register", data)
        .then((response) => {
            if (response.data["success"] === true) {
                alert("Tạo tài khoản thành công!")
                localStorage.setItem("email", email.value);
                localStorage.setItem("password", password.value);
                window.location.replace("login.html")
            } else {
                alert(`Email ${email.value} đã được sử dụng!`)
            }
        })
        .catch((error) => {
            console.error(`Error: ${error}`);
        });
}