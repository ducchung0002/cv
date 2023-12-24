/*
 * GLOBALS
 */

/*
 * trigger
 */
async function trigger_file_input(applicant_certificate_id) {
    document.getElementById(`image_select_${applicant_certificate_id}`).click();
}

/*
 * CRUD applicant certificate
 */
async function insert_applicant_certificate() {
    let formData = new FormData();
    formData.append("command", "insert_certificate");

    axios.post("http://127.0.0.1:5000/applicant/certificate", formData, {
        headers: {
            "Authorization": `Bearer ${access_token}`,
            "Content-Type": "multipart/form-data"
        }
    }).then(async function (response) {
        if (response.data["success"]) {
            let certificate_container = document.getElementById("certificate_container");
            let applicant_certificate_id = response.data["applicant_certificate_id"];
            let row = await create_certificate_row(applicant_certificate_id, "", null, []);
            certificate_container.appendChild(row);
        } else {
            console.log(response.data);
        }
    }).catch(function (error) {
        console.log(`Insert applicant certificate image error: ${error}`);
    });
}

async function update_applicant_certificate(applicant_certificate_id) {
    let certificate_name = document.getElementById(`certificate_name_${applicant_certificate_id}`).value;
    let received_date = document.getElementById(`received_date_${applicant_certificate_id}`).value;
    let formData = new FormData();
    formData.append("applicant_certificate_id", applicant_certificate_id);
    formData.append("certificate_name", certificate_name);
    formData.append("received_date", received_date);
    formData.append("command", "update_applicant_certificate");
    axios.put("http://127.0.0.1:5000/applicant/certificate", formData, {
        headers: {
            "Authorization": `Bearer ${access_token}`,
            "Content-Type": "multipart/form-data"
        }
    }).then((response) => {
        if (response.data["success"]) {
            alert("Cập nhật chứng chỉ thành công");
        }
    }).catch((error) => {
        console.log("Update applicant certificate error: ", error);
        alert("Cập nhật chứng chỉ thất bại!");
    });
}

async function delete_applicant_certificate(applicant_certificate_id) {
    let formData = new FormData();
    formData.append("applicant_certificate_id", applicant_certificate_id);
    formData.append("command", "delete_applicant_certificate");

    axios.delete("http://127.0.0.1:5000/applicant/certificate", {
        data: formData,
        headers: {
            "Authorization": `Bearer ${access_token}`
        }
    }).then((response) => {
        if (response.data["success"]) {
            let container = document.getElementById(`applicant_certificate_${applicant_certificate_id}`);
            console.log("Delete: ", container);
            container.remove();
        }
    }).catch((error) => {
        console.log("Update applicant certificate error: ", error);
        alert("Xoá chứng chỉ thất bại!");
    });
}

/*
 * CRUD certificate image
 */
async function insert_certificate_image(applicant_certificate_id) {
    let file = document.getElementById(`image_select_${applicant_certificate_id}`).files[0];
    let formData = new FormData();
    formData.append("command", "insert_certificate_image");
    formData.append("image", file);
    formData.append("applicant_certificate_id", applicant_certificate_id);

    axios.post("http://127.0.0.1:5000/applicant/certificate", formData, {
        headers: {
            "Authorization": `Bearer ${access_token}`,
            "Content-Type": "multipart/form-data"
        }
    }).then(async function (response) {
        if (response.data["success"]) {
            let applicant_certificate_image_id = response.data["applicant_certificate_image_id"];
            let image_path = response.data["image_path"]
            let image_container = document.getElementById(`certificate_image_container_${applicant_certificate_id}`);
            let image_col = await create_certificate_image_col_element(applicant_certificate_image_id, image_path);
            image_container.appendChild(image_col);
        } else {
            console.log(response.data);
        }
    }).catch(function (error) {
        console.log(`Insert applicant certificate image error: ${error}`);
    });
}

async function delete_certificate_image(applicant_certificate_image_id) {
    let formData = new FormData();
    formData.append("applicant_certificate_image_id", applicant_certificate_image_id);
    formData.append("command", "delete_applicant_certificate_image");
    axios.delete("http://127.0.0.1:5000/applicant/certificate", {
        data: formData,
        headers: {
            "Authorization": `Bearer ${access_token}`,
            "Content-Type": "multipart/form-data"
        }
    }).then((response) => {
        if (response.data["success"]) {
            let col = document.getElementById(`certificate_image_col_${applicant_certificate_image_id}`);
            col.remove();
        }
    }).catch((error) => {
        console.log("Delete certificate image error: ", error);
    });
}

// Input: applicant_certificate_image_id, image_path
// Output: Image element, get image from flask server by image_path
async function create_certificate_image_element(applicant_certificate_image_id, image_path) {
    let img = document.createElement("img");
    img.classList.add("img-fluid");

    await axios.get("http://127.0.0.1:5000/applicant/certificate", {
        headers: {
            "Authorization": `Bearer ${access_token}`,
            "Content-Type": "multipart/form-data"
        }, params: {
            "command": "get_certificate_image",
            "image_path": image_path
        }, responseType: "blob"
    }).then(function (response) {
        let blob = new Blob([response.data], {type: "image"});
        img.src = URL.createObjectURL(blob);
    }).catch((error) => {
        alert(`Get applicant certificate image error: ${error}`);
    });
    return img;
}
/**
 * [Create a certificate image column for specific certificate]
 */
async function create_certificate_image_col_element(applicant_certificate_image_id, image_path) {
    let certificate_image_col = document.createElement("div");
    certificate_image_col.id = `certificate_image_col_${applicant_certificate_image_id}`;
    certificate_image_col.classList.add("position-relative", "col-2", "m-1", "certificate-image-col");
    let img = await create_certificate_image_element(applicant_certificate_image_id, image_path);
    img.classList.add("certificate-image");
    certificate_image_col.innerHTML = `
            ${img.outerHTML}
            <button class="btn btn-primary p-1" style="position: absolute; top: 5px; left: 5px;" onclick="showImage('${img.src}')"><i class="bi bi-zoom-in"></i></button>
            <button class="btn btn-danger p-1" style="position: absolute; top: 5px; right: 5px;" onclick="delete_certificate_image(${applicant_certificate_image_id})"><i class="bi bi-x-square"></i></button>
            `;
    return certificate_image_col;
}
/*
 * End CRUD certificate image
 */

async function create_certificate_row(applicant_certificate_id, certificate_name, received_date, images) {
    let row = document.createElement("div");
    row.classList.add("row", "mb-2");
    row.id = `${applicant_certificate_id}`;
    let innerHTML = `
<div id="applicant_certificate_${applicant_certificate_id}" class="border rounded p-3">
<div class="row">
    <div class="form-floating mb-2 col-3">
        <input type="text" class="form-control form-control-lg" id="certificate_name_${applicant_certificate_id}" value="${certificate_name}" placeholder="Tên chứng chỉ">
        <label for="certificate_name_${applicant_certificate_id}" class="form-label" style="padding-left: 1.5rem">Tên chứng chỉ</label>
    </div>
    <div class="form-floating mb-2 col-3">
        <input type="date" class="form-control form-control-lg" id="received_date_${applicant_certificate_id}" value="${convert_python_date_format(received_date)}" placeholder="Ngày nhận">
        <label for="received_date_${applicant_certificate_id}" class="form-label" style="padding-left: 1.5rem">Ngày nhận</label>
    </div>
    <div class="form-floating mb-2 col-1">
        <button class="btn btn-outline-primary" onclick="update_applicant_certificate(${applicant_certificate_id})"><i class="bi bi-pencil-square"></i></button>
    </div>
    <div class="form-floating mb-2 col-1">
        <button class="btn btn-outline-primary" onclick="delete_applicant_certificate(${applicant_certificate_id})"><i class="bi bi-trash-fill"></i></button>
    </div>
</div>
<div class="row">
    <p class="display-6">Hình ảnh</p>
    <button class="col-1 btn btn-outline-primary p-1 mb-2" onclick="trigger_file_input(${applicant_certificate_id})"><i class="bi bi-plus-square"></i></button>
    <input type="file" id="image_select_${applicant_certificate_id}" style="display:none;" onchange="insert_certificate_image(${applicant_certificate_id})"/>
</div>
<div class="row" id="certificate_image_container_${applicant_certificate_id}">`;

    Promise.all(images.map(async (image) => {
        // let img = await create_certificate_image_element(image["id"], image["image_path"]);
        // innerHTML += `<div id="certificate_image_${image["id"]}" class="position-relative col-2 m-1" style="width: 150px;">`;
        // innerHTML += img.outerHTML;
        // innerHTML += `<button class="btn btn-outline-danger p-1" style="position: absolute; top: 5px; right: 5px;" onclick="delete_certificate_image(${image["id"]})"><i class="bi bi-x-square p-3"></i></button>
        //             </div>`;
        let image_col = await create_certificate_image_col_element(image["id"], image["image_path"]);
        innerHTML += image_col.outerHTML;
    })).then(ignored => {
        innerHTML += "</div></div>";
        row.innerHTML = innerHTML;
    });

    return row;
}

/*
 * main
 */
axios.get("http://127.0.0.1:5000/applicant/certificate", {
    headers: {
        "Authorization": `Bearer ${access_token}`,
    }, params: {
        "command": "get_certificate"
    }
}).then(function (response) {
    let applicant_certificate;
    if (response.data["success"]) {
        applicant_certificate = response.data["applicant_certificate"];
        let certificate_container = document.getElementById("certificate_container");

        Promise.all(applicant_certificate.map(async cer => {
            let row = await create_certificate_row(cer["id"], cer["name"], cer["received_date"], cer["images"]);
            certificate_container.appendChild(row);
        })).then(ignored => {
        });
    }
}).catch((error) => {
    alert(`Get applicant profile error: ${error}`);
    window.location.href = "login.html";
});