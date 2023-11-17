document.addEventListener('DOMContentLoaded', function () {
    const studentId = student_id;
    const latest_meeting_checkin = make_api_call("/get_latest_meeting_checkin", 'GET', {"studentId": studentId}, false)['date_and_time'];
});