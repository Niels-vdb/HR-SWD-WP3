document.getElementById('navbar-nav-2').classList.add('nav-item-invisible');

let studentsChecked = [];
// Needs to keep selected students selected
function checkClickStudent(studentId) {
  let student = document.getElementById(`student-${studentId}`);
  if (student.checked == true) {
    studentsChecked.push(student.id.split("-")[1]);
  } else {
    index = studentsChecked.indexOf(student.id.split("-")[1]);
    studentsChecked.splice(index, 1);
  }

  fetch("/students")
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      let markup = ``;
      const studentsInMeeting = document.getElementById(
        "students-in-planning"
      );
      for (student_info of studentsChecked) {
        data.forEach((student) => {
          if (student_info == student.student_id) {
            markup += `
                    <div class="schedule-block">
                      <div class="schedule-block-header">
                        <i class="bi bi-check-circle"></i>
                        <p class="student-name" data-student="${student.student_id}">${student.student_id} - ${student.name}</p>
                      </div>
                    </div>
              `;
          }
        });
      }
      studentsInMeeting.replaceChildren();
      studentsInMeeting.insertAdjacentHTML("beforeend", markup);
    });
  return studentsChecked;
}

var classesChecked = [];
function checkClickClass(classId) {
  let clas = document.getElementById(`class-${classId}`);
  if (clas.checked == true) {
    classesChecked.push(clas.id.split("-")[1]);
  } else {
    index = classesChecked.indexOf(classId);
    classesChecked.splice(index, 1);
  }

  fetch("/classes")
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      let markup = ``;
      const classInMeeting = document.getElementById("classes-in-planning");
      for (class_info of classesChecked) {
        data.forEach((clas) => {
          if (class_info == clas.class_id) {
            markup += `
              <div class="schedule-block">
                <div class="schedule-block-header">
                  <i class="bi bi-check-circle"></i>
                  <p class="student-name">${clas.study}, ${clas.class_name}</p>
                </div>
              </div>
                  `;
          }
        });
      }
      classInMeeting.replaceChildren();
      classInMeeting.insertAdjacentHTML("beforeend", markup);
    });
  return classesChecked;
}

const formEl = document.getElementById("create-meeting-form");

formEl.addEventListener("submit", (event) => {
  event.preventDefault();
  
  if (studentsChecked.length == 0 && classesChecked.length == 0) {
    show_flash_message(
      "Er zijn geen studenten toegevoegd aan de bijeenkomst.",
      "danger", true
    );
    return;
  }

  const formData = new FormData(formEl);
  let dataEntries = [...formData.entries()];

  let meetingInfo = {
    teacher: teacherId,
    course: dataEntries[0][1],
    dateAndTime: `${dataEntries[1][1]} ${dataEntries[2][1]}`,
    question: dataEntries[3][1],
    classes: classesChecked,
    students: studentsChecked,
  };

  fetch("/create-meeting", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(meetingInfo),
  })
    .then((response) => response.json())
    .then((data) => console.log(data))
    .then(() => {
      show_flash_message("Bijeenkomst is aangemaakt", "success", true)
      window.location.reload()
    })
    .catch((error) => {
      show_flash_message(
        "Er is iets fout gegdaan bij de invoer van de informatie.",
        "danger",
        true
      );
    });
});