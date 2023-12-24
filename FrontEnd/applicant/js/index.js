let applicant;

async function main() {
    let formData = new FormData();
    formData.append("command", "get_applicant");

    axios.post("http://127.0.0.1:5000/applicant/profile", formData, {
        headers: {
            "Authorization": `Bearer ${access_token}`,
            "Content-Type": "multipart/form-data"
        }
    }).then(function (response) {
        applicant = response.data["applicant"];
        document.getElementById("navbar_hidden_options").textContent = applicant["name"];
    }).catch((ignored) => {
        window.location.replace("/../FrontEnd/applicant/index.html");
    });
}

main().then(ignored => {});