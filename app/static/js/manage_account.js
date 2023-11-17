const student_information_wrapper = document.getElementById("student_information_wrapper")
const classes_information_wrapper = document.getElementById('classes_information_wrapper')

const search_student_field = document.getElementById("search_student_field")
const students_list = document.getElementById("students_list")
const added_students_list = document.getElementById("added_students_list")
search_student_field.addEventListener("input", search_student);


let added_students = []

function all_studies_select_html_generator(comparator, onchange_function){
    const all_studies = make_api_call("/get_all_studies", 'GET',{}, false)

    let html_code =
        `<select name="studies" class="form-select" onchange="${onchange_function}">
        <option>Kies een studie...</option>`

    for (let y = 0; y < all_studies.length; y++) {
        if(all_studies[y]['studyId'] === comparator) {
            html_code = html_code + `<option selected value="${all_studies[y]['studyId']}">${all_studies[y]['name']}</option>`
        }
        else {
            html_code = html_code + `<option value="${all_studies[y]['studyId']}">${all_studies[y]['name']}</option>`
        }
    }
    html_code = html_code + '</select>'

    return html_code
}

function all_classes_of_study_select_html_generator(study, comparator, onchange_function){
    const all_classes_of_study = make_api_call("/get_all_classes_of_study", 'GET',{"studyId": study}, false)
    let html_code = `
        <select name="${"study-" + study}" class="form-select" onchange="${onchange_function}">
        <option>Kies een klas...</option>`

    for (let y = 0; y < all_classes_of_study.length; y++) {
        if(all_classes_of_study[y]['name'] === comparator) {
            html_code = html_code + `<option selected value="${all_classes_of_study[y]['classId']}">${all_classes_of_study[y]['name']}</option>`
        }
        else {
            html_code = html_code + `<option value="${all_classes_of_study[y]['classId']}">${all_classes_of_study[y]['name']}</option>`
        }
    }
    html_code = html_code + '</select>'

    return html_code
}

function set_ui_for_person_information() {
    let student_id = document.getElementById('student_number_field').value
    const student = make_api_call("/get_user_by_pk", 'GET',{"id": student_id}, false)
    const latest_meeting_checkin = make_api_call("/get_latest_meeting_checkin", 'GET',{"studentId": student_id}, false)['date_and_time']
    let html_code =
                `<div class="col"> 
                    <span class="badge text-bg-primary">Studentnummer</span> 
                </div> 
                <div class="col"> 
                    <span class="user-select-all">${student['studentId']}</span> 
                </div> 
                <div class="col"> 
                    <span class="badge text-bg-primary">Naam</span> 
                </div>
                <div class="col-auto"> 
                    <input id="student_name_field" class="form-control" type="text" value="${student['name']}">
                </div>
                <div class="col-auto p-0"> 
                    <button onclick="save_name()" class="btn btn-outline-success">Opslaan</button>
                </div>
                <div class="col"> 
                    <span class="badge text-bg-primary">Laatste check-in moment</span>
                </div> 
                <div class="col"> 
                    <span class="user-select-all">${latest_meeting_checkin}</span> 
                </div> 
                <div class="col"> 
                    <span class="badge text-bg-dark">Studie(s)</span><button type="button" class="ms-2 btn btn-outline-primary btn-sm" onclick="set_ui_for_add_study()"><i class="bi bi-plus-lg"></i></button> 
                </div>`

    for (let i = 0; i < student['studies'].length; i++) {
        const study_id = student['studies'][i]['study']
        html_code = html_code +
            `
            <div class="col">
                <div class="row gx-2">
                    <div class="col-auto">
                        <button onclick="remove_student_from_class(this, document.getElementById('student_number_field').value, this.parentElement.parentElement.children[2].firstElementChild.value)" class="btn btn-outline-danger"><i class="bi bi-x-lg"></i></button>
                    </div>
                    <div class="col-auto">
                        ${all_studies_select_html_generator(study_id)}
                    </div>
                    <div class="col-auto">
                        ${all_classes_of_study_select_html_generator(study_id, student['studies'][i]['class'])}
                    </div>
                </div>
            </div>
            `
    }
    student_information_wrapper.innerHTML = `${html_code}`
}

function remove_student_from_class(element, student_id, class_id) {
    // let student_id = document.getElementById('student_number_field').value
    // let class_id = element.parentElement.parentElement.children[2].firstElementChild.value
    let response = make_api_call("/remove_student_from_class", 'POST',{"studentId": student_id, "classId": class_id}, false)

    element.parentElement.parentElement.parentElement.remove()
    show_flash_message(`<i class="bi bi-info-circle-fill"></i> ${response["message"]}`, "info")
}

function set_ui_for_add_study(){
    let html_code =
        `<div class="col">
            <div class="row gx-2">
                <div class="col-auto">
                    <button onclick="this.parentElement.parentElement.parentElement.remove()" class="btn btn-danger"><i class="bi bi-x-lg"></i></button>
                </div>   
                <div class="col-auto">
                    ${all_studies_select_html_generator("", "set_ui_for_class_picker(this)")}
                </div>
            </div>
        </div>`
    student_information_wrapper.insertAdjacentHTML('beforeend', html_code)
}

function add_student_to_class(element){
    let student_id = document.getElementById('student_number_field').value
    let class_id = element.parentElement.parentElement.children[2].firstElementChild.value
    make_api_call("add_student_to_class", 'POST',{"studentId": student_id, "classId": class_id}, false)


    setAttributes(element.parentElement.parentElement.firstElementChild.firstElementChild, {"class": "btn btn-outline-danger", "onclick": "remove_student_from_class(this, document.getElementById('student_number_field').value, this.parentElement.parentElement.children[2].firstElementChild.value)"})
    element.parentElement.parentElement.lastElementChild.remove()

    show_flash_message("<i class=\"bi bi-info-circle-fill\"></i> Student is toegevoegd aan klas!", "success")
}

function set_ui_for_class_picker(element){
    const study_id = element.value

    let html_code =
        `<div class="col-auto">
            ${all_classes_of_study_select_html_generator(study_id)}
        </div>
        <div class="col-auto">
            <button type="button" class="btn btn-success" onclick="add_student_to_class(this)"><i class="bi bi-plus-lg"></i></button>
        </div>`

    element.parentElement.insertAdjacentHTML('afterend', html_code)
}

function generate_table_of_chosen_class(element){
    const class_id = element.parentElement.parentElement.children[1].firstElementChild.value
    const student_id_field = document.getElementById('student_number_field')
    const students = make_api_call("/get_all_students_of_class", 'GET',{"classId": class_id}, false)


    let html_code = `
        <div class="col-12">
            <table class="table table-striped table-hover">
                <thead>
                    <tr>
                        <th scope="col">Studentnummer</th>
                        <th scope="col">Naam</th>
                        <th scope="col">Meer info</th>
                        <th scope="col">Verwijder uit klas</th>
                    </tr>
                </thead>
                <tbody>
        `

    for (let y = 0; y < students.length; y++) {
        html_code = html_code + `
            <tr>
                <td>${students[y]['studentId']}</td>
                <td>${students[y]['name']}</td>
                <td><button onclick="document.getElementById('student_number_field').value=${students[y]['studentId']}; set_ui_for_person_information(); document.getElementById('home-tab').click();" class="btn btn-primary"><i class="bi bi-search"></i></button></td>
                <td><button onclick="show_flash_message('Gebruiker is verwijderd uit de klas', 'info');this.parentElement.parentElement.remove(); remove_student_from_class('', ${students[y]['studentId']}, ${class_id});" class="btn btn-danger"><i class="bi bi-box-arrow-right"></i></button></td>
            </tr>
        `
    }

    html_code = html_code + '</tbody></table></div><div class="wh-100"></div>'
    classes_information_wrapper.insertAdjacentHTML('beforeend', html_code)
}

function save_name(){
    let student_name = document.getElementById("student_name_field").value
    const student_id = document.getElementById('student_number_field').value
    let response = make_api_call('/edit_database_row', 'POST', {"table_name": "Student", "column": "name", "value": student_name, "condition_column": "studentId", "condition_value": student_id}, false)

    show_flash_message(`<i class="bi bi-info-circle-fill"></i> ${response["message"]}`, "info")
}

function create_student(element){
    const student_id = document.getElementById("new_student_studentnumber").value
    const name = document.getElementById("new_student_name").value
    const password = document.getElementById("new_student_password").value
    const class_id = document.getElementById('new_student_studies_wrapper').parentElement.lastElementChild.firstElementChild.value


    let response = make_api_call("/add_student_account", "POST", {"studentId": student_id, "name": name, "password": password, "classId": class_id}, false)

    show_flash_message(`<i class="bi bi-info-circle-fill"></i> ${response["message"]}`, "info")
}

function add_to_class(element){
    element.remove()
    if (added_students.includes(element.value)){
        show_flash_message(`<i class="bi bi-exclamation-triangle-fill"></i> ${element.innerText} has been added already!`, "danger")
    }
    added_students.push(element.value)
    let html_code = `<li onclick="remove_from_class(this)" class="list-group-item temp-remove-item" value="${element.value}">${element.innerText}</li>`
    added_students_list.insertAdjacentHTML('beforeend', html_code)
}

function search_student(input) {
    if (input.target.value.length > 2){
        let students = make_api_call(`/student-filter/${input.target.value}`, 'GET', {}, false)

        students_list.innerHTML = ''
        for (let y = 0; y < students.length; y++) {
            const html_code = `<li onclick="add_to_class(this)" class="list-group-item temp-list-item" value="${students[y]['student_id']}">${students[y]['name']}</li>`
            students_list.insertAdjacentHTML('beforeend', html_code)
        }
    }
}

function remove_from_class(element){
    element.remove()
    console.log(added_students)
    const index = added_students.indexOf(element.value)
    added_students.splice(index, 1)
    console.log(added_students)
}

function create_class(){
    const new_class_study = document.getElementById("new_class_study")
    const class_title_field = document.getElementById("class_title_field")
    const students_list = document.getElementById("students_list")

    if (new_class_study.value === "Kies een studie..."){
        new_class_study.setAttribute("class", "form-select border border-danger")
        show_flash_message("Selecteer een studie!", "danger")
    }
    else {
        const response = make_api_call("/create_class", "POST", {"name": class_title_field.value, "studyId": new_class_study.value}, false)
        show_flash_message(response['message'], response['status_category'])
        const class_id = response['class_id']

        if (added_students.length > 0) {
            for (let y = 0; y < added_students.length; y++) {
                make_api_call("add_student_to_class", 'POST',{"studentId": added_students[y], "classId": class_id}, false)
                console.log(added_students[y])
            }
        }
        else{
            students_list.setAttribute("class", "list-group overflow-scroll border border-danger")
            show_flash_message("Voeg eerst minimaal 1 student toe!", "danger")
        }
    }
}


function create_teacher(){
    const teacher_email = document.getElementById("new_teacher_email").value
    const teacher_name = document.getElementById("new_teacher_name").value
    const teacher_password = document.getElementById("new_teacher_password").value
    const teacher_admin = document.getElementById("new_teacher_admin").checked

    const parameters = {
        "email": teacher_email,
        "name": teacher_name,
        "password": teacher_password,
        "admin": teacher_admin
    }

    const response = make_api_call("/create_teacher", 'POST', parameters, false)

    show_flash_message(response['message'], 'success')
}