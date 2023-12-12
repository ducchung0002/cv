let all_skill_type;
let all_skill;
let all_experience;
let applicant_skill;
let skill_type_dict;

/*
 * Reload skill dropdown when skill type onchange
 */

function reload_skill_dropdown(applicant_skill_id, def) {
    alert("onchange trigger");
    let skill_type_dropdown = document.getElementById(`skill_type_dd_${applicant_skill_id}`);
    let skill_dropdown = document.getElementById(`skill_dd_${applicant_skill_id}`);
    // remove all option before
    while (skill_dropdown?.firstChild) {
        skill_dropdown.removeChild(skill_dropdown.firstChild);
    }
    // Get all skills for specific skill type
    let skill_of_type = skill_type_dict[skill_type_dropdown.value]["skill"];
    skill_of_type.forEach((sk) => {
        let option = document.createElement("option");
        option.classList.add();
        option.value = sk["id"];
        option.textContent = sk["name"];
        option.selected = sk["name"] === def;
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
    let skill_dropdown = document.getElementById(`skill_dd_${applicant_skill_id}`);
    all_skill.forEach((sk) => {
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
 * Delete applicant skill button click
 */
function delete_applicant_skill(app_sk_id) {
    console.log("Delete applicant skill id: ", app_sk_id);
}

/*
 * Fill skill information
 */
function fill_skill_information() {
    let skill_div = document.getElementById("skill_container");

    applicant_skill.forEach((app_sk) => {
        let app_sk_id = app_sk["id"];
        let row = document.createElement("div");
        row.classList.add("row", "mb-2");
        row.innerHTML = `
<div class="col-3">
    <select class="form-control form-select" id="skill_type_dd_${app_sk_id}" onchange="reload_skill_dropdown(${this.value}, ${app_sk["skill_id"]})"></select>
</div>
<div class="col-4">
    <select class="form-control form-select" id="skill_dd_${app_sk_id}"></select>
</div>
<div class="col-3">
    <select class="form-control form-select" id="experience_dd_${app_sk_id}"></select>
</div>
<div class="col-1">
    <button class="btn" onclick="delete_applicant_skill(${app_sk_id})"><i class="bi bi-trash-fill"></i></button>
</div>
        `;
        let load_skill_type_script = document.createElement("script");
        load_skill_type_script.textContent = `load_skill_type_dropdown(${app_sk_id}, ${app_sk["skill_type_id"]});`;
        let load_skill_script = document.createElement("script");
        load_skill_script.textContent = `load_skill_dropdown(${app_sk_id}, ${app_sk["skill_id"]});`;
        let load_experience_script = document.createElement("script");
        load_experience_script.textContent = `load_experience_dropdown(${app_sk_id}, ${app_sk["experience_id"]});`;
        row.appendChild(load_skill_type_script);
        row.appendChild(load_skill_script);
        row.appendChild(load_experience_script);
        skill_div.appendChild(row);
    });
}

/*
 * Main
 */

async function main() {
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

    await axios.get("http://127.0.0.1:5000/applicant/skill", {
        headers: {
            "Authorization": `Bearer ${access_token}`
        }
    }).then(function (response) {
        applicant_skill = response.data["applicant_skill"];
    }).catch(function (error) {
        console.log(`Error: ${error}`);
    });
}
main();
fill_skill_information();
