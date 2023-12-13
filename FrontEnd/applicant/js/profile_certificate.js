/*
 * GLOBALS
 */
let applicant_certificate;

/*
 * trigger
 */
function trigger_file_input(applicant_certificate_id) {
    document.getElementById(`image_select_${applicant_certificate_id}`).click();
}
/*
 * CRUD applicant certificate
 */

function add_certificate_image(applicant_certificate_id) {
    applicant_certificate["images"].forEach();
}

function insert_applicant_certificate() {

}


function load_certificate_image(applicant_certificate_id) {

}

/*
 * End CRUD
 */

function create_certificate_row(applicant_certificate_id, certificate_name, received_date, images) {
    let row = document.createElement("div");
    row.classList.add("row", "mb-2");
    row.id = `applicant_certificate_row_${applicant_certificate_id}`;
    row.innerHTML = `
<div class="row">
<div class="form-floating mb-2 col-3">
    <input type="text" class="form-control form-control-lg" id="certificate_name_${applicant_certificate_id}" value="${certificate_name}" placeholder="Tên chứng chỉ">
    <label for="certificate_name_${applicant_certificate_id}" class="form-label" style="padding-left: 1.5rem">Tên chứng chỉ</label>
</div>
<div class="form-floating mb-2 col-3">
    <input type="date" class="form-control form-control-lg" id="received_date_${applicant_certificate_id}" value="${convert_python_date_format(received_date)}" placeholder="Ngày nhận">
    <label for="received_date_${applicant_certificate_id}" class="form-label" style="padding-left: 1.5rem">Ngày nhận</label>
</div>
</div>
<div class="row">
    <p class="display-6">Hình ảnh</p>
    <button class="col-1 btn btn-outline-primary p-2" onclick="trigger_file_input(${applicant_certificate_id})"><i class="bi bi-plus-square"></i></button>
    <input type="file" id="image_select_${applicant_certificate_id}" style="display:none;" onchange="add_certificate_image(${applicant_certificate_id})"/>
</div>
<div class="row" id="image_container_${applicant_certificate_id}">
</div>
    `;
    let load_image_script = document.createElement("script");
    load_image_script.innerHTML = `load_certificate_image(${applicant_certificate_id})`;
    row.appendChild(load_image_script);
    return row;
}

/*
 * main
 */
axios.get("http://127.0.0.1:5000/applicant/certificate", {
    headers: {
        "Authorization": `Bearer ${access_token}`
    }
}).then(function (response) {
    console.log(response.data);
    if (response.data["success"]) {
        applicant_certificate = response.data["applicant_certificate"];
        let certificate_container = document.getElementById("certificate_container");

        applicant_certificate.forEach((cer) => {
            let row = create_certificate_row(cer["id"], cer["name"], cer["received_date"], cer["images"]);
            certificate_container.appendChild(row);
        });
    }
}).catch((error) => {
    alert(`Get applicant profile error: ${error}`);
    window.location.href = "login.html";
});