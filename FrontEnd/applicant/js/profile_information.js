let avatar = document.getElementById("avatar");
let name = document.getElementById("name");
let birthdate = document.getElementById("birthdate");
let male = document.getElementById("male");
let phone = document.getElementById("phone");
let address = document.getElementById("address");
let email = document.getElementById("email");
let facebook = document.getElementById("facebook");
let github = document.getElementById("github");
let self_introduction = document.getElementById("self_introduction");
let education_school_name = document.getElementById("education_school_name");
let education_major = document.getElementById("education_major");
let education_school_start_date = document.getElementById("education_school_start_date");
let education_school_end_date = document.getElementById("education_school_end_date");
let internship_enterprise_name = document.getElementById("internship_enterprise_name");
let internship_position = document.getElementById("internship_position");
let internship_start_date = document.getElementById("internship_start_date");
let internship_end_date = document.getElementById("internship_end_date");

function fill_profile_information() {
    avatar.src = "data:image/jpeg;base64," + applicant["avatar"];
    if (applicant["avatar"] === null || applicant["avatar"] === "") {
        avatar.src = applicant["gender"] ? "images/man.png" : "images/woman.png";
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
function update_profile_information() {
    let data = {
        name: name.value,
        birthdate: birthdate.value,
        gender: male.checked,
        phone: phone.value,
        address: address.value,
        facebook: facebook.value,
        github: github.value,
        self_introduction: self_introduction.value,
        education_school_name: education_school_name.value,
        education_major: education_major.value,
        education_school_start_date: education_school_start_date.value,
        education_school_end_date: education_school_end_date.value,
        internship_enterprise_name: internship_enterprise_name.value,
        internship_position: internship_position.value,
        internship_start_date: internship_start_date.value,
        internship_end_date: internship_end_date.value
    }
    axios.put("http://127.0.0.1:5000/applicant/update_profile", data, {
        headers: {
            "Authorization": `Bearer ${access_token}`
        }
    })
        .then((response) => {
            console.log(response.data)
            alert("Cập nhật hồ sơ thành công!");
        })
        .catch((error) => {
            console.error(`Error: ${error}`);
            alert("Cập nhật hồ sơ thất bại!");
        });
}

function update_avatar() {
    let file = document.getElementById("fileInput").files[0];
    let reader = new FileReader();
    reader.onload = function (e) {
        document.getElementById("avatar").src = e.target.result;
    };
    reader.readAsDataURL(file);
    // upload to backend
    let formData = new FormData();
    formData.append("avatar", file);
    axios.put("http://127.0.0.1:5000/applicant/update_avatar", formData, {
        headers: {
            "Authorization": `Bearer ${access_token}`,
            "Content-Type": "multipart/form-data"
        }
    })
        .then(function (response) {
            console.log(response.data);
        })
        .catch(function (error) {
            console.log(error);
        });
}

avatar.onclick = () => {
    document.getElementById('fileInput').click();
}

axios.get("http://127.0.0.1:5000/applicant/profile", {
    headers: {
        "Authorization": `Bearer ${access_token}`
    }
}).then(function (response) {
    console.log(response.data);
    applicant = response.data["applicant"];
    fill_profile_information();
}).catch((error) => {
    console.log(`Error: ${error}`);
});