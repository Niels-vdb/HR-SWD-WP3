invinsilbleNav();

function teacherCallOff(meetingId) {
  const myRequest = new XMLHttpRequest();
  myRequest.open("POST", `/teacher-call-off-meeting/${meetingId}`, true);
  myRequest.send();
}
function teacherDeleteMeeting(meetingId) {
  fetch(`/meetings/${meetingId}`, {
    method: "DELETE",
  });
}

console.log(teacherId);
const fetch_teacher_meetings = () => {
  fetch(`/teachers/${teacherId}`)
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      let teacherSchedule = document.getElementById("teacher-schedule");
      teacherSchedule.replaceChildren();
      console.log(data.meetings.length);
      if (data.meetings.length == 0) {
        teacherSchedule.insertAdjacentHTML(
          "beforeend",
          "<p>Geen bijeenkomsten ingepland</p>"
        );
      }
      data.meetings.forEach((meeting) => {
        classString = "";
        for (clas of meeting.classes) {
          classString += `${clas} `;
        }
        let date = new Date(Date.parse(meeting.date));
        const monthNames = [
          "januari",
          "februari",
          "maart",
          "april",
          "mei",
          "juni",
          "juli",
          "augustus",
          "september",
          "oktober",
          "november",
          "december",
        ];
        let time = meeting.time;
        let hour = time.split(":")[0];
        let minute = time.split(":")[1];
        let timeFormated = `${hour}:${minute}`;

        const markup = `
              <div class="schedule-block teacher-schedule-block">
                
                <a href="${beamerScreen}/${meeting.meeting_id}" 
                    class="teacher-begin-meeting">
                  <div class="teacher-begin-meeting">
                    <div class="schedule-block-header schedule-block-header-techer-menu">
                      <i class="bi bi-calendar-check"></i>
                      <p class="meeting-name">${meeting.course}</p>
                    </div>
              
                    <div class="schedule-block-info-teacher">
                      <p class="classes-and-students">Klas(sen): ${classString}</p>
                      <p>Datum: ${date.getDate()} ${
          monthNames[date.getMonth()]
        } ${date.getFullYear()}</p>
                      <p>Tijd: ${timeFormated}</p>
                    </div>
                  </div>
                </a>

                <div class="teacher-meeting-btns">
                  <form action="/teacher-delete-meeting" 
                        method="post" 
                        class="teacher-delete-meeting"
                        onclick="teacherDeleteMeeting('${meeting.meeting_id}')">
                    <i class="bi bi-trash3"></i>
                    <p>Verwijder</p>
                  </form>
                  
                  <form action="/teacher-cancel-meeting" 
                        method="post" 
                        class="teacher-cancel-meeting"
                        onclick="teacherCallOff('${meeting.meeting_id}')">
                    <i class="bi bi-calendar-x"></i>
                    <p>Annuleer</p>
                  </form>
                </div>
              </div>
          `;
        teacherSchedule.insertAdjacentHTML("beforeend", markup);
      });
    });
};

let refresh = setInterval(fetch_teacher_meetings, 1000);
