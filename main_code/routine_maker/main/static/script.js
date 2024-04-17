const subjectList = [];

function addSubject(subjectName) {

    document.querySelector('#selected-subject-list-container').style.display = "flex";
    document.querySelector('#submit').style.display = "block";

    const subjectListElm = document.getElementById('selected-subject-list');


    if (subjectName.includes('(')) {
        const baseName = subjectName.slice(0, subjectName.indexOf('('));

        for (let i = 0; i < subjectList.length; i++) {
            if (subjectList[i].includes(baseName)) {
                const removedElm = subjectList.splice(i, 1);
                document.getElementById(removedElm).remove();
            }
        }

    }

    if (!(subjectList.includes(subjectName))) {

        subjectList.push(subjectName);
        const buttonElm = document.createElement('button');
        buttonElm.textContent = subjectName;

        buttonElm.setAttribute('id', subjectName);

        buttonElm.addEventListener('click', () => {

            try {
                const i = subjectList.indexOf(buttonElm.textContent);
                subjectList.splice(i, 1);
                console.log(buttonElm.textContent);
                document.getElementById(buttonElm.textContent).remove();
            }
        
            catch (e) {
                console.log(e);
                console.log(subjectList)
                console.log('Error')
            }

            finally {
                if (subjectList.length === 0) {
                    document.querySelector('#selected-subject-list-container').style.display = "none";
                    document.querySelector('#submit').style.display = "none";
                }
            }
        });

        subjectListElm.appendChild(buttonElm);

    }
}
