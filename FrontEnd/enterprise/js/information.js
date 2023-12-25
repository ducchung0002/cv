let avatar = document.getElementById("avatar");
let name = document.getElementById("name");
let introduction = document.getElementById("introduction");
let homepage =  document.getElementById("homepage");

function fill_profile_information() {
     avatar.src = "data:image/jpeg;base64," + enterprise["avatar"]
     if(!enterprise["avatar"]) {
        avatar.src = "images/logo.jpg"
     }
     document.title = name.value = enterprise["name"];
     introduction.value = enterprise["introduction"] ?enterprise["introduction"]:"" ;
     homepage.value = enterprise["homepage"]?enterprise["homepage"]:""
}

async function update_information() {
    let formData = new FormData();
    formData.append("name", name.value);
    formData.append("introduction", introduction.value);
    formData.append("homepage", homepage.value);
    formData.append("command", "update_profile");
    console.log(name.value);
    console.log(introduction.value);
    console.log(homepage.value);
    axios.put("http://127.0.0.1:5000/enterprise/profile", formData, {
        headers: {
            "Authorization": `Bearer ${access_token}`,
            "Content-Type": "multipart/form-data"
        }
    }).then((response) => {
        if (response.data["success"])
        alert("Cập nhật hồ sơ thành công!");
        else 
        alert("Cập nhật hồ sơ đéo thành công!");
})
.catch((error) => {
    console.error(`Update profile information error: ${error}`);
    alert("Cập nhật hồ sơ thất bại!");
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
 avatar.onclick = () => {
     document.getElementById('fileInput').click();
 }

 
axios.get("http://127.0.0.1:5000/enterprise/profile", {
     headers: {
         "Authorization": `Bearer ${access_token}`
     }
 }).then(function (response) {
     console.log(response.data);
     enterprise = response.data["enterprise"];
     fill_profile_information();
 }).catch((error) => {
     console.log(`Error: ${error}`);
 });
