let all_skill_type;
let all_skill;
let all_experience;
let applicant_skill;
let skill_type_dict;

/*
 * Reload skill dropdown when skill type onchange
 */

function reload_skill_dropdown(applicant_skill_id, def) {
    let skill_type_dropdown = document.getElementById(`skill_type_dd_${applicant_skill_id}`);
    let skill_dropdown = document.getElementById(`skill_dd_${applicant_skill_id}`);
    // remove all option before
    while (skill_dropdown.firstChild) {
        skill_dropdown.removeChild(skill_dropdown.firstChild);
    }
    // Get all skills for specific skill type
    let skill_of_type = skill_type_dict[skill_type_dropdown.value]["skill"];
    skill_of_type.forEach((sk) => {
        let option = document.createElement("option");
        option.classList.add();
        option.value = sk["id"];
        option.textContent = sk["name"];
        option.selected = sk["id"] === def;
        skill_dropdown.appendChild(option);
    });
}

/*
 * Load skill type dropdown, skill dropdown, experience dropdown
 */
function load_skill_type_dropdown(applicant_skill_id, def) {
    let skill_type_dropdown = document.getElementById(`skill_type_dd_${applicant_skill_id}`);
    all_skill_type.forEach((sk_tp) => {
        let option = document.createElement("option");
        option.classList.add();
        option.value = sk_tp["id"];
        option.textContent = sk_tp["name"];
        option.selected = sk_tp["id"] === def;
        skill_type_dropdown.appendChild(option);
    });
}

function load_skill_dropdown(applicant_skill_id, def) {
    let skill_type_dropdown = document.getElementById(`skill_type_dd_${applicant_skill_id}`);
    let skill_dropdown = document.getElementById(`skill_dd_${applicant_skill_id}`);
    let selected_skill_type_id = skill_type_dropdown.value;
    skill_type_dict[selected_skill_type_id]["skill"].forEach((sk) => {
        let option = document.createElement("option");
        option.classList.add();
        option.value = sk["id"];
        option.textContent = sk["name"];
        option.selected = sk["id"] === def;
        skill_dropdown.appendChild(option);
    });
}

function load_experience_dropdown(applicant_skill_id, def) {
    let experience_dropdown = document.getElementById(`experience_dd_${applicant_skill_id}`);
    all_experience.forEach((exp) => {
        let option = document.createElement("option");
        option.classList.add();
        option.value = exp["id"];
        option.textContent = exp["name"];
        option.selected = exp["id"] === def;
        experience_dropdown.appendChild(option);
    });
}

/*
 * Update + Delete applicant skill button click
 */
function update_applicant_skill(applicant_skill_id) {
    let skill_dropdown = document.getElementById(`skill_dd_${applicant_skill_id}`);
    let experience_dropdown = document.getElementById(`experience_dd_${applicant_skill_id}`);

    axios.put("http://127.0.0.1:5000/applicant/skill", {
        "id" : applicant_skill_id,
        "skill_id": skill_dropdown.value,
        "experience_id": experience_dropdown.value
    },{
        headers: {
            "Authorization": `Bearer ${access_token}`
        }
    }).then(function (response) {
        let update_btn = document.getElementById(`update_skill_button_${applicant_skill_id}`);
        update_btn.classList.add("d-none");
    }).catch(function (error) {
        console.log(`Delete applicant skill error: ${error}`);
    });
}
function delete_applicant_skill(applicant_skill_id) {
    axios.delete("http://127.0.0.1:5000/applicant/skill", {
        headers: {
            "Authorization": `Bearer ${access_token}`,
            "Content-Type": "application/json"
        },
        data: {
            "id": applicant_skill_id
        }
    }).then(function (response) {
        console.log("Delete applicant skill response data: ", response.data);
        if (response.data["success"]) {
            let row = document.getElementById(`applicant_skill_row_${applicant_skill_id}`);
            row.remove();
        }
    }).catch(function (error) {
        console.log(`Delete applicant skill error: ${error}`);
    });
}
function trigger_update_button(applicant_skill_id) {
    let update_btn = document.getElementById(`update_skill_button_${applicant_skill_id}`);
    update_btn.classList.remove("d-none");
}
/*
 * Insert applicant skill
 */
function insert_applicant_skill() {
    let skill_type_id;
    let skill_id;
    let experience_id;
    try {
        skill_type_id = all_skill_type[0]["id"];
        skill_id = skill_type_dict[skill_type_id]["skill"][0]["id"];
        experience_id = all_experience[0]["id"];
        console.log("skill_type_id", skill_type_id);
        console.log("skill_id", skill_id);
        console.log("experience_id", experience_id);
    } catch (error) {
        console.log("Init default applicant skill record failed!");
        return;
    }

    axios.post("http://127.0.0.1:5000/applicant/skill", {"skill_id": skill_id, "experience_id" : experience_id} ,{
        headers: {
            "Authorization": `Bearer ${access_token}`
        }
    }).then(function (response) {
        console.log("Insert applicant skill request response: ", response.data);
        if (response.data["success"] === true) {
            let applicant_skill_id = response.data["applicant_skill_id"];
            /************************/
            let skill_div = document.getElementById("skill_container");
            let row = create_skill_row(applicant_skill_id, skill_type_id, skill_id, experience_id);
            skill_div.appendChild(row);
        } else {
            alert("Thêm kỹ năng mới thất bại!");
        }
    }).catch(function (error) {
        console.log(`Error: ${error}`);
    });
}
/*
 * Load skill information
 */
function create_skill_row(applicant_skill_id, skill_type_id, skill_id, experience_id) {
    let row = document.createElement("div");
    row.classList.add("row", "mb-2");
    row.id = `applicant_skill_row_${applicant_skill_id}`;
    row.innerHTML =
     `
<div class="col-3">
    <select class="form-control form-select" id="skill_type_dd_${applicant_skill_id}" onchange="reload_skill_dropdown(${applicant_skill_id}, ${skill_id}); trigger_update_button(${applicant_skill_id})"></select>
</div>
<div class="col-4">
    <select class="form-control form-select" id="skill_dd_${applicant_skill_id}" onchange="trigger_update_button(${applicant_skill_id})"></select>
</div>
<div class="col-3">
    <select class="form-control form-select" id="experience_dd_${applicant_skill_id}" onchange="trigger_update_button(${applicant_skill_id})"></select>
</div>
<div class="col-1">
    <button class="btn" onclick="delete_applicant_skill(${applicant_skill_id})"><i class="bi bi-trash-fill"></i></button>
</div>
<div class="col-1">
    <button class="btn d-none" onclick="update_applicant_skill(${applicant_skill_id})" id="update_skill_button_${applicant_skill_id}"><i class="bi bi-pencil-square"></i></button>
</div>
        `;
    let load_skill_type_script = document.createElement("script");
    load_skill_type_script.textContent = `load_skill_type_dropdown(${applicant_skill_id}, ${skill_type_id});`;
    let load_skill_script = document.createElement("script");
    load_skill_script.textContent = `load_skill_dropdown(${applicant_skill_id}, ${skill_id});`;
    let load_experience_script = document.createElement("script");
    load_experience_script.textContent = `load_experience_dropdown(${applicant_skill_id}, ${experience_id});`;
    row.appendChild(load_skill_type_script);
    row.appendChild(load_skill_script);
    row.appendChild(load_experience_script);
    return row;
}
function load_skill_information() {
    axios.get("http://127.0.0.1:5000/applicant/skill", {
        headers: {
            "Authorization": `Bearer ${access_token}`
        }
    }).then(function (response) {
        applicant_skill = response.data["applicant_skill"];
        /************************/
        let skill_div = document.getElementById("skill_container");

        applicant_skill.forEach((app_sk) => {
            let row = create_skill_row(app_sk["id"], app_sk["skill_type_id"], app_sk["skill_id"], app_sk["experience_id"]);
            skill_div.appendChild(row);
        });

        /***********************/
    }).catch(function (error) {
        console.log(`Error: ${error}`);
    });
}

/*
 * Main
 */

async function profile_skill_init() {
    await axios.get("http://127.0.0.1:5000/database/skill_type", {
        headers: {
            "Authorization": `Bearer ${access_token}`
        }
    }).then(function (response) {
        all_skill_type = response.data["skill_type"];
        skill_type_dict = {}
        all_skill_type.forEach((skill_type) => {
            skill_type_dict[skill_type["id"]] = {"name": skill_type["name"]}
        });
    }).catch(function (error) {
        console.log(`Error: ${error}`);
    });

    await axios.get("http://127.0.0.1:5000/database/experience", {
        headers: {
            "Authorization": `Bearer ${access_token}`
        }
    }).then(function (response) {
        all_experience = response.data["experience"];
    }).catch(function (error) {
        console.log(`Error: ${error}`);
    });

    await axios.get("http://127.0.0.1:5000/database/skill", {
        headers: {
            "Authorization": `Bearer ${access_token}`
        }
    }).then(function (response) {
        all_skill = response.data["skill"];
        all_skill.forEach((sk) => {
            if (skill_type_dict[sk["skill_type_id"]]["skill"] === undefined) {
                skill_type_dict[sk["skill_type_id"]]["skill"] = []
            }
            skill_type_dict[sk["skill_type_id"]]["skill"].push({"id": sk["id"], "name": sk["name"]});
        });

    }).catch(function (error) {
        console.log(`Error: ${error}`);
    });
}
profile_skill_init().then(r => load_skill_information());

