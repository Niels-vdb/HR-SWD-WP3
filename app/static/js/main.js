console.log("main.js is executing this line :)!");
const flash_message_wrapper = document.getElementById("flash_message_wrapper");

function show_flash_message(message, category, short=false) {
  if (short) {
    console.log('bye')
    flash_message_wrapper.innerHTML = `      
      <div class="alert alert-${category} alert-dismissible fade show bs-alert-short" role="alert">
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
      </div>
      `;
  } else
  flash_message_wrapper.innerHTML = `      
      <div class="alert alert-${category} alert-dismissible fade show bs-alert" role="alert">
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
      </div>
      `;
}

function setAttributes(el, attrs) {
  for (let key in attrs) {
    el.setAttribute(key, attrs[key]);
  }
}

function make_api_call(url, method, parameters, async) {
  url = url + "?";
  for (let param in parameters) {
    url = url + param + "=" + parameters[param] + "&";
  }
  const myRequest = new XMLHttpRequest();
  myRequest.open(method, url, async);
  myRequest.send();

  return JSON.parse(myRequest.responseText);
}

function invinsilbleNav() {
  for (i = 0; i < 5; i++) {
    document.getElementsByClassName("navbar-nav")[i].style.display = "none";
  }
}

// $(function (){

//     var $student = $('#student');
//     $.ajax({
//         type: 'GET',
//         url: 'templates/lookupscreen'
//         success: function(data) {
//             $.each(student, function (i, student) {
//                 $student.append('<li>Student: '+ student.name +', '+student.id+');
//             }
//             console.log('succes', data);
//         }
//     });
// });
