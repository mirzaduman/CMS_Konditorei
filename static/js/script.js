let personen_anzahl = document.querySelector('#personen_anzahl')
let button_2 = document.querySelector('#tortenstockwerke-2')
let button_3 = document.querySelector('#tortenstockwerke-3')




function viewFotoInput() {
    let textinput = document.querySelector('.torten-foto')
    textinput.classList.toggle('active')
}

function exampleFotoInput() {
    let textinput = document.querySelector('.vorlage-foto')
    textinput.classList.toggle('active')
}


function viewTextInput() {
    let textinput = document.querySelector('.text-input')
    textinput.classList.toggle('active')
}

if (personen_anzahl) {
    personen_anzahl.addEventListener('change', function() {
        if (personen_anzahl.value < 40) {
            button_2.disabled = true
            button_3.disabled = true
        }
        else if (60 > personen_anzahl.value && personen_anzahl.value >= 40) {
            button_2.disabled = false
            button_3.disabled = true
        } else if (personen_anzahl.value >= 60) {
            button_2.disabled = false
            button_3.disabled = false
        }
    })
}


let today = new Date();
let dd = today.getDate() + 1;
let mm = today.getMonth() + 1; //January is 0!
let yyyy = today.getFullYear();

if (dd < 10) {
   dd = '0' + dd;
}

if (mm < 10) {
   mm = '0' + mm;
} 
    
today = yyyy + '-' + mm + '-' + dd;
document.getElementById("date").setAttribute("min", today);


function nextForm() {
    let first_name = document.getElementById("vorname").value
    let last_name = document.getElementById("nachname").value
    let phone = document.getElementById("telefonnummer").value
    let mail = document.getElementById("mail").value
    let date = document.getElementById("date").value
    let time = document.getElementById("time").value
    let agb = document.getElementById("agb").value
    if (first_name == null || first_name == "" || last_name == null || last_name == "" || phone == null || phone == "" || mail == null || mail == "" || date == null || date == "" || time == null || time == "" || agb == null || agb == "") {
        console.log("working")
        alert("Bitte füllen Sie alle Felder");
        return false;
      }
    else {
        let part_i = document.querySelector(".part-i")
        let part_ii = document.querySelector(".part-ii")
        part_i.classList.add("display")
        part_ii.classList.remove("display")
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
}


function goBack() {
    let part_i = document.querySelector(".part-i")
    let part_ii = document.querySelector(".part-ii")
    part_ii.classList.add("display")
    part_i.classList.remove("display")
    window.scrollTo({ top: 0, behavior: 'smooth' });
}
