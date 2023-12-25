let jobName = document.getElementById("jobName");
let jobDescription = document.getElementById("jobDescription");
let position = document.getElementById("position");
let applicantRequirement = document.getElementById("applicantRequirement");
let benefit = document.getElementById("benefit");
let minSalary = document.getElementById("minSalary");
let maxSalary = document.getElementById("maxSalary");
let deadline = document.getElementById("deadline");
let postDate = document.getElementById("postDate");
let access_token = localStorage.getItem("access_token");
function fill_profile_information() {
     avatar.src = "data:image/jpeg;base64," + enterprise["avatar"]
     if(!enterprise["avatar"]) {
        avatar.src = "images/logo.jpg"
     }
     document.title = name.value = enterprise["name"];
     introduction.value = enterprise["introduction"] ?enterprise["introduction"]:"" ;
     homepage.value = enterprise["homepage"]?enterprise["homepage"]:""
}

async function add_recruitment() {
     console.log("Here");
     let formData = new FormData();
     formData.append("jobName", jobName.value);
     formData.append("jobDescription", jobDescription.value);
     formData.append("position", position.value);
     formData.append("applicantRequirement", applicantRequirement.value);
     formData.append("benefit", benefit.value);
     formData.append("minSalary", minSalary.value);
     formData.append("maxSalary", maxSalary.value);
     formData.append("postDate", postDate.value);
     formData.append("deadline", deadline.value);
     formData.append("command", "add_recruitment");
    axios.post("http://127.0.0.1:5000/enterprise/recruitment", formData, {
        headers: {
            "Authorization": `Bearer ${access_token}`,
            "Content-Type": "multipart/form-data"
        }
    }).then((response) => {
        if (response.data["success"])
          alert("Thêm tuyển dụng thành công");
        else 
          alert("Thêm tuyển dụng đéo thành công!");
})
.catch((error) => {
    console.error(`Update profile information error: ${error}`);
    alert("Thêm tuyển dụng thất bại!");
});
     console.log(formData);
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
     axios.put("http://127.0.0.1:5000/enterprise/update_avatar", formData, {
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

 
// axios.get("http://127.0.0.1:5000/enterprise/profile", {
//      headers: {
//          "Authorization": `Bearer ${access_token}`
//      }
//  }).then(function (response) {
//      console.log(response.data);
//      enterprise = response.data["enterprise"];
//      fill_profile_information();
//  }).catch((error) => {
//      console.log(`Error: ${error}`);
//  });
