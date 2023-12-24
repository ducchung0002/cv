async function change_password() {
    const old_password = document.getElementById("old_password").value;
    const new_password = document.getElementById("new_password").value;
    const retype_new_password = document.getElementById("retype_new_password").value;

    if (new_password !== retype_new_password) {
        alert("Mật khẩu nhập lại không đúng!");
        return;
    }

    let formData = new FormData();
    formData.append("old_password", old_password);
    formData.append("new_password", new_password);
    formData.append("command", "change_password");

    axios.post("http://localhost:5000/applicant/profile", formData, {
        headers: {
            "Authorization": `Bearer ${access_token}`,
            "Content-Type": "multipart/form-data"
        }
    })
        .then(response => {
            console.log(response.data);
            if (response.data["success"] === true) {
                alert("Đổi mật khẩu thành công!");
            } else {
                alert("Đổi mật khẩu thất bại!");
            }
        })
        .catch(error => {
            console.error("Change password error: ", error);
        });
}