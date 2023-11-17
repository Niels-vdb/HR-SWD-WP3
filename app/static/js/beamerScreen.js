invinsilbleNav();

// Functionality for list toggles
const presentList = document.getElementById("beamer-present-list");
const absentList = document.getElementById("beamer-absent-list");
const calledOffList = document.getElementById("beamer-called-off-list");
const messageList = document.getElementById("beamer-messages-list");
const beamerScreen = document.getElementById("beamer-screen");
beamerScreen.addEventListener("load", beamerScreenInit(), true);

function beamerScreenInit() {
  absentList.style.display = "none";
  calledOffList.style.display = "none";
  messageList.style.display = "none";
}

function presentToggle() {
  presentList.style.display = "";
  absentList.style.display = "none";
  calledOffList.style.display = "none";
  messageList.style.display = "none";
}
function absentToggle() {
  presentList.style.display = "none";
  absentList.style.display = "";
  calledOffList.style.display = "none";
  messageList.style.display = "none";
}
function calledOffToggle() {
  presentList.style.display = "none";
  absentList.style.display = "none";
  calledOffList.style.display = "";
  messageList.style.display = "none";
}
function messageListToggle() {
  presentList.style.display = "none";
  absentList.style.display = "none";
  calledOffList.style.display = "none";
  messageList.style.display = "";
}

// Functionality for putting students absent
function studentAbsent(studentId, meetingId) {
  fetch(`/beamer-student-absent/${studentId}/${meetingId}`, {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
  });
}

function studentCalledOf(studentId, meetingId) {
  fetch(`/beamer-student-call-off/${studentId}/${meetingId}`, {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
  });
}

function endMeeting(meetingId) {
  fetch(`/end-meeting/${meetingId}`, {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
  });
}
