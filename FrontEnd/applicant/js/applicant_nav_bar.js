async function switch_view_logout() {
    localStorage.setItem("email", "");
    localStorage.setItem("password", "");
    localStorage.setItem("access_token", "");
    window.location.replace("/../FrontEnd/job/index.html");
}

async function switch_view_change_password() {
    $("#page_content").load("/../FrontEnd/applicant/change_password.html");
}

async function switch_view_homepage() {
    $("#page_content").load("/../FrontEnd/job/main.html");
}

async function switch_view_profile() {
    $("#page_content").load("/../FrontEnd/applicant/profile.html");
}

async function switch_view_application() {
    $("#page_content").load("/../FrontEnd/applicant/application.html");
}