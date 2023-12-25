let enterpriseTable = document.getElementById('enterpriseTable');
function redirectToDetailPage(id) {
     // Redirect to another page passing the enterprise ID
     window.location.href = `detail.html?id=${id}`;
 }
 
 document.addEventListener('DOMContentLoaded', function() {
     // Get all elements with class 'enterpriseName'
     let enterpriseNames = document.querySelectorAll('.enterpriseName');
 
     // Add click event listener to each element
     enterpriseNames.forEach(name => {
         name.addEventListener('click', function(event) {
             let enterpriseId = event.target.getAttribute('data-id');
             redirectToDetailPage(enterpriseId);
         });
     });
 });
function fill_profile_name(enterprises) {
     enterprises.forEach(enterprise => {
         const row = document.createElement('tr');
         
         // Tạo cell cho tên enterprise và thêm thuộc tính data-id
         const nameCell = document.createElement('td');
         const nameLink = document.createElement('a');
         nameLink.textContent = enterprise.name;
         nameLink.setAttribute('data-id', enterprise.id); // Lưu trữ id trong thuộc tính data-id
         nameLink.classList.add('enterpriseName'); // Thêm class để xác định cho việc thêm sự kiện click
         nameCell.appendChild(nameLink);
         row.appendChild(nameCell);
 
         // Thêm hàng vào bảng
         enterpriseTable.appendChild(row);
     });
 
     // Gán sự kiện click cho các phần tử có class 'enterpriseName'
     let enterpriseNames = document.querySelectorAll('.enterpriseName');
     enterpriseNames.forEach(name => {
         name.addEventListener('click', function(event) {
             let enterpriseId = event.target.getAttribute('data-id');
             redirectToDetailPage(enterpriseId);
         });
     });
 }
 
 
 
axios.get("http://127.0.0.1:5000/enterprise/admin", {
     headers: {
         "Authorization": `Bearer ${access_token}`
     }
 }).then(function (response) {
     // console.log(response.data);
     enterprises = response.data["enterprises"];
     enterprises = JSON.parse(enterprises);
     fill_profile_name(enterprises);
 }).catch((error) => {
     console.log(`Error: ${error}`);
 });
