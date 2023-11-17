let url = window.location.href;
let meetingId = url.split("/").pop();

const fetch_students = () => {
  fetch(`/meetings/${meetingId}`)
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      let presentList = document.getElementById("present-students");
      presentList.replaceChildren();
      let studentsPresentCounter = document.getElementById('students-present-counter');
      studentsPresentCounter.replaceChildren();

      data.students_present.forEach((studentsPresent) => {
        const markup = `
                <div class="schedule-block schedule-block-beamer schedule-block-beamer-present id="schedule-block-beamer-present">
                  <div class="schedule-block-student-name">
                    <i class="bi bi-check-circle toggle-icon"></i>
                    <p class="student-name">${studentsPresent.name}</p>
                  </div>
                  <div class="schedule-block-toggles">
                    <i class="bi bi-hourglass-split toggle-icon toggle-icon-present-absent" 
                        onclick="studentAbsent(${studentsPresent.student_id}, ${data.meeting_id})">
                    </i>
                  </div>
                </div>
                `;
        presentList.insertAdjacentHTML("beforeend", markup);
        
      });
      presentCounter = ` <strong>${presentList.children.length}</strong>`
      studentsPresentCounter.insertAdjacentHTML("beforeend", presentCounter);

      let absentList = document.getElementById("absent-students");
      absentList.replaceChildren();
      let studentsAbsentCounter = document.getElementById('students-absent-counter');
      studentsAbsentCounter.replaceChildren();
      data.students_absent.forEach((studentAbsent) => {
        const markup = `
                <div class="schedule-block schedule-block-beamer" id="schedule-block-beamer-absent">
                  <div class="schedule-block-student-name">
                    <i class="bi bi-hourglass-split toggle-icon"></i>
                    <p class="student-name">${studentAbsent.name}</p>
                  </div>
                  <div class="schedule-block-toggles">
                    <i class="bi bi-x-circle toggle-icon toggle-icon-present-called-off" 
                        onclick="studentCalledOf(${studentAbsent.student_id}, ${data.meeting_id})">
                    </i>
                  </div>
                </div>
                `;
        absentList.insertAdjacentHTML("beforeend", markup);
      });
      absentCounter = ` <strong>${absentList.children.length}</strong>`
      studentsAbsentCounter.insertAdjacentHTML("beforeend", absentCounter);

      let calledOffList = document.getElementById("called-off-students");
      calledOffList.replaceChildren();
      let studentsCalledOffCounter = document.getElementById('students-called-off-counter');
      studentsCalledOffCounter.replaceChildren();

      data.students_called_off.forEach((studentCalledOff) => {
        const markup = `
                <div class="schedule-block schedule-block-beamer" id="schedule-block-beamer-called-off">
                  <i class="bi bi-x-circle toggle-icon"></i>
                  <p class="student-name">${studentCalledOff.name}</p>
                </div>
                `;
        calledOffList.insertAdjacentHTML("beforeend", markup);
        
      });
      let calledOffCounter = ` <strong>${calledOffList.children.length}</strong>`
      studentsCalledOffCounter.insertAdjacentHTML("beforeend", calledOffCounter)

      let studentReplies = document.getElementById("student-replies");
      studentReplies.replaceChildren();
      data.student_replies.forEach((reply) => {
        const markup = `
                <div
                  class="schedule-block schedule-block-beamer schedule-block-beamer-replies"
                >
                  <div class="schedule-block-header">
                    <p class=student-reply>
                      ${reply.reply}
                    </p>
                  </div>
                </div>
              `;
        studentReplies.insertAdjacentHTML("beforeend", markup);
      });
    });
};

let refresh = setInterval(fetch_students, 1000);
