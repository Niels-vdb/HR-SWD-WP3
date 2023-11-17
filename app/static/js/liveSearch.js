function liveSearch(value) {
    value = value.trim();
    fetch(`/student-filter/${value}`)
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        let listOfStudents = document.getElementById("list_of_students");
        listOfStudents.replaceChildren();
        data.forEach((student) => {
          const markup = `
            <li class="list-group-item student-list-item">
              <input class="form-check-input me-1" 
                      type="checkbox" 
                      value="${student.student_id}" 
                      id="student-${student.student_id}"
                      name="student-in-meeting"
                      onclick="checkClickStudent(${student.student_id})"    
                  >
              <label class="form-check-label" 
                      for="student-${student.student_id}"
                      >${student.student_id} - ${student.name}</label>
            </li>
            `;
          listOfStudents.insertAdjacentHTML("beforeend", markup);
        });
      });
  }

  const listOfStudents = document.getElementById("list_of_students");

  student_list = liveSearch();

  result = "";
  for (let student of student_list) {
    result += `<li class="list-group-item student-list-item">
                <input class="form-check-input me-1" 
                        type="checkbox" 
                        value="" 
                        id="firstCheckbox">
                <label class="form-check-label" 
                        for="firstCheckbox">
                          ${student.studentId} - ${student.name}
                        </label>
              </li>`;
  }

  listOfStudents.innerHTML(result);