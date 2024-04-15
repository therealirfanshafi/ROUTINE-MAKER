const subjectList = [];

function addSubject(subjectName) {
    document.querySelector('#selected-subject-list-container').style.display = "flex";
    document.querySelector('#submit').style.display = "block";
    const subjectListElm = document.getElementById('selected-subject-list');
    if (!(subjectList.includes(subjectName))) {
        subjectList.push(subjectName);
        const buttonElm = document.createElement('button');
        buttonElm.textContent = subjectName;
        subjectListElm.appendChild(buttonElm);
    }
}