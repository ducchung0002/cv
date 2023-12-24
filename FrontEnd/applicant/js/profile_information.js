const avatar = document.getElementById("avatar");
const name = document.getElementById("name");
const birthdate = document.getElementById("birthdate");
const male = document.getElementById("male");
const phone = document.getElementById("phone");
const address = document.getElementById("address");
const email = document.getElementById("email");
const facebook = document.getElementById("facebook");
const github = document.getElementById("github");
const self_introduction = document.getElementById("self_introduction");
const education_school_name = document.getElementById("education_school_name");
const education_major = document.getElementById("education_major");
const education_school_start_date = document.getElementById("education_school_start_date");
const education_school_end_date = document.getElementById("education_school_end_date");
const internship_enterprise_name = document.getElementById("internship_enterprise_name");
const internship_position = document.getElementById("internship_position");
const internship_start_date = document.getElementById("internship_start_date");
const internship_end_date = document.getElementById("internship_end_date");

async function fill_profile_information() {
    if (applicant["avatar"] === null || applicant["avatar"] === "") {
        avatar.src = applicant["gender"] ? "images/man.png" : "images/woman.png";
    } else {
        let formData = new FormData();
        formData.append("image_path", applicant["avatar_path"]);
        formData.append("command", "get_avatar");

        axios.post("http://localhost:5000/applicant/profile", formData, {
            headers: {
                "Authorization": `Bearer ${access_token}`,
                "Content-Type": "multipart/form-data"
            }, responseType: "blob"
        })
            .then(response => {
                let blob = new Blob([response.data], {type: "image"});
                avatar.src = URL.createObjectURL(blob);
            })
            .catch(error => {
                console.error(error);
            });
    }
    document.title = name.value = applicant["name"];
    birthdate.value = convert_python_date_format(applicant["birthdate"]);
    male.checked = applicant["gender"];
    phone.value = applicant["phone"];
    address.value = applicant["address"];
    email.value = applicant["email"];
    facebook.value = applicant["facebook"];
    github.value = applicant["github"];
    self_introduction.value = applicant["self_introduction"];
    education_school_name.value = applicant["education_school_name"];
    education_major.value = applicant["education_major"];
    education_school_start_date.value = convert_python_date_format(applicant["education_school_start_date"]);
    education_school_end_date.value = convert_python_date_format(applicant["education_school_end_date"]);
    internship_enterprise_name.value = applicant["internship_enterprise_name"];
    internship_position.value = applicant["internship_position"];
    internship_start_date.value = convert_python_date_format(applicant["internship_start_date"]);
    internship_end_date.value = convert_python_date_format(applicant["internship_end_date"]);
}

/*
 * Update trigger
 */
async function update_profile_information() {
    let formData = new FormData();
    formData.append("name", name.value);
    formData.append("birthdate", birthdate.value);
    formData.append("gender", male.checked);
    formData.append("self_introduction", self_introduction.value);
    formData.append("phone", phone.value);
    formData.append("address", address.value);
    formData.append("facebook", facebook.value);
    formData.append("github", github.value);
    formData.append("education_school_name", education_school_name.value);
    formData.append("education_major", education_major.value);
    formData.append("education_school_start_date", education_school_start_date.value);
    formData.append("education_school_end_date", education_school_end_date.value);
    formData.append("internship_enterprise_name", internship_enterprise_name.value);
    formData.append("internship_position", internship_position.value);
    formData.append("internship_start_date", internship_start_date.value);
    formData.append("internship_end_date", internship_end_date.value);
    formData.append("command", "update_profile");

    axios.put("http://127.0.0.1:5000/applicant/profile", formData, {
        headers: {
            "Authorization": `Bearer ${access_token}`,
            "Content-Type": "multipart/form-data"
        }
    }).then((response) => {
        if (response.data["success"])
            alert("Cập nhật hồ sơ thành công!");
    })
    .catch((error) => {
        console.error(`Update profile information error: ${error}`);
        alert("Cập nhật hồ sơ thất bại!");
    });
}

async function update_avatar() {
    let file = document.getElementById("fileInput").files[0];
    let formData = new FormData();
    formData.append("avatar", file);
    formData.append("command", "update_avatar");

    axios.put("http://127.0.0.1:5000/applicant/profile", formData, {
        headers: {
            "Authorization": `Bearer ${access_token}`,
            "Content-Type": "multipart/form-data"
        },
        responseType: "blob"
    }).then(function (response) {
        let blob = new Blob([response.data], {type: "image"});
        avatar.src = URL.createObjectURL(blob);
    }).catch(function (error) {
        console.log(`Update avatar error: ${error}`);
    });
}

avatar.onclick = () => {
    document.getElementById('fileInput').click();
}

let formData = new FormData();
formData.append("command", "get_applicant");

axios.post("http://127.0.0.1:5000/applicant/profile", formData, {
    headers: {
        "Authorization": `Bearer ${access_token}`,
        "Content-Type": "multipart/form-data"
    }
}).then(function (response) {
    console.log(response.data);
    applicant = response.data["applicant"];
    fill_profile_information().then((ignored) => {
    });
}).catch((ignored) => {
    window.location.href = "login.html";
});