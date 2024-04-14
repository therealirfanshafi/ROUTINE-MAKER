const subjectList = [];

function addSubject(subjectName) {
    document.querySelector('#selected-subject-list-container').style.display = "block";
    document.querySelector('#submit').style.display = "block";
    const subjectListElm = document.getElementById('selected-subject-list');
    if (!(subjectList.includes(subjectName))) {
        subjectList.push(subjectName);
        const listItemElm = document.createElement('li');
        listItemElm.textContent = subjectName;
        subjectListElm.appendChild(listItemElm);
    }
}