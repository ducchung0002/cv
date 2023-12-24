const name = document.getElementById("name");
const birthdate = document.getElementById("birthdate");
const gender_male = document.getElementById("male");
const email = document.getElementById("email");
const password = document.getElementById("password");
const confirm_password = document.getElementById("confirm_password");

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
        birthdate: birthdate.value,
        gender: gender_male.checked ? 1 : 0,
        email: email.value,
        password: password.value
    }
    axios.post("http://127.0.0.1:5000/applicant/register", data)
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