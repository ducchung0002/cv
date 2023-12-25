let avatar = document.getElementById("avatar");
let name = document.getElementById("name");
let introduction = document.getElementById("introduction");
let homepage =  document.getElementById("homepage");
let urlParams = new URLSearchParams(window.location.search);
let enterpriseId = urlParams.get('id');
console.log(enterpriseId); // In ra giá trị của enterpriseId từ URL
function fill_profile_information(enterprise) {
     avatar.src = "data:image/jpeg;base64," + enterprise["avatar"]
     if(!enterprise["avatar"]) {
        avatar.src = "images/logo.jpg"
     }
     document.title = name.value = enterprise["name"];
     introduction.value = enterprise["introduction"] ?enterprise["introduction"]:"" ;
     homepage.value = enterprise["homepage"]?enterprise["homepage"]:""
}

 
axios.get(`http://127.0.0.1:5000/enterprise/detail?id=${enterpriseId}`, {
     headers: {
          "Authorization": `Bearer ${access_token}`
      }
}).then(function (response) {
        console.log(response.data);
        let enterprise = response.data["enterprise"];
        console.log('enterprise', enterprise);
        fill_profile_information(enterprise);
    })
    .catch((error) => {
        console.log(`Error: ${error}`);
    });