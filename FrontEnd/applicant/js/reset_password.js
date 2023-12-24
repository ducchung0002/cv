async function reset_password() {
    const email = document.getElementById("applicant_email");
    if (email.checkValidity() === false) {
        alert("Email không hợp lệ!");
        return;
    }

    deactivate_reset_password_button(60).then(ignored => {});

    axios.get("http://127.0.0.1:5000/applicant/reset_password", {
        params: {
            email: email.value
        }
    }).then(response => {
        if (response.data["success"] === true) {
            document.getElementById("submit_recovery_code_container").classList.toggle("visually-hidden");
        } else {
            alert("Email không tồn tại!");
        }
    }).catch((error) => {
        console.log("Request reset password failed!: ", error);
    })
}

async function deactivate_reset_password_button(seconds) {
    let reset_password_button = $("#reset_password_button");
    let textContent = reset_password_button.textContent;
    // Disable the button
    reset_password_button.prop("disabled", true);

    let countdown = setInterval(function() {
        reset_password_button.text(`Thử lại sau ${seconds} giây`);
        seconds--;

        // When the countdown is over
        if (seconds <= 0) {
            clearInterval(countdown);

            // Enable the button
            reset_password_button.prop("disabled", false);
            reset_password_button.text(textContent);
        }
    }, 1000);
}

async function submit_recovery_code() {
    const recovery_code = document.getElementById("recovery_code").value;
    const email = document.getElementById("applicant_email").value;

    let formData = new FormData();
    formData.append("email", email);
    formData.append("recovery_code", recovery_code)

    axios.post("http://127.0.0.1:5000/applicant/reset_password", formData)
        .then(response => {
            console.log(response);
        if (response.data["success"] === true) {
            alert("Mật khẩu của bạn đã được đặt lại. Vui lòng kiểm tra hộp thư đến trong email.");
            $('#page_content').load('/../FrontEnd/applicant/login.html');
        } else {
            alert("Mã khôi phục bị sai hoặc đã hết hạn!");
        }
    }).catch(error => {
        console.log("Request reset password failed!");
    })
}