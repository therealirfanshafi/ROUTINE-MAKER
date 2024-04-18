const subjectList = [];  // array to keep track of the subjects which have been selected in the html document
const subjectTrackerElm = document.getElementById('subject-tracker');  // a hidden input field whose value is continuosly set to subjectList if any change is made to it. This input field is used to send back the subjectList array back to django in a GET request as JSON data


// event listner for subject adding button
function addSubject(subjectName, qualification) {

    // unhides the selected subjects list 
    document.querySelector('#selected-subject-list-container').style.display = "flex";
    document.querySelector('#submit').style.display = "block";

    const subjectListElm = document.getElementById('selected-subject-list');

    if (subjectName.includes('(')) {  // checks if the subject contains an extension

        const baseName = subjectName.slice(0, subjectName.indexOf('('));  // gets the name of the subject without the extension

        for (let i = 0; i < subjectList.length; i++) {  // loops over the subjectList array
            if (subjectList[i].slice(0, subjectName.indexOf('(')) === baseName) {  // and removes any subject which is an alternative option of the selected subject

                const removedElm = subjectList.splice(i, 1);
                document.getElementById(removedElm).remove();

            }
        }

    }

    if (!(subjectList.includes(subjectName))) {  // checks if the subject + extension is already within the array

        subjectList.push(subjectName);  // and ads it if already not

        //creates a button element to show the users that the subject is selected
        const buttonElm = document.createElement('button');
        buttonElm.textContent = subjectName;

        buttonElm.setAttribute('id', subjectName);

        // event listner for the created button
        buttonElm.addEventListener('click', () => {

            try {  // which removes a selected subject if clicked

                const i = subjectList.indexOf(buttonElm.textContent);
                subjectList.splice(i, 1);
                document.getElementById(buttonElm.textContent).remove();
                subjectTrackerElm.value = JSON.stringify([...subjectList, {qualification: qualification}]);

            }
        
            catch (e) { // in case the subject doesnt exist for some reason

                console.log(e);
                console.log(subjectList)
                console.log('Error')

            }

            finally {  
                if (subjectList.length === 0) { // checks if there is no subject in the list

                    // and if so, the selected subject list in the HTML is hidden again
                    document.querySelector('#selected-subject-list-container').style.display = "none";
                    document.querySelector('#submit').style.display = "none";

                }
            }
        });

        subjectListElm.appendChild(buttonElm); // adds the button to the appropriate div
        subjectTrackerElm.value = JSON.stringify([...subjectList, {qualification: qualification}]);  // converts the list to JSON and stores in the hidden input field. The last object added is used in the server to determine which qualification level the subjects fall under
        
    }
}

