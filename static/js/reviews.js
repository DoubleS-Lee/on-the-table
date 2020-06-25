const cEBtn = document.querySelectorAll(".commentEditBtn");
const cEInput = document.querySelectorAll(".commentEInput");
const cEIBtn = document.querySelectorAll(".commentEIBtn");

const editActive = "showing";
const editDeactive = "noShowing";

function reviewEdit(event) {
    const reviewNum = event.target.value;
    console.log(event);
    event.target.classList.remove(editActive);
    event.target.classList.add(editDeactive);
    for (var i = 0; i < cEInput.length; i++){
        cEInput[i].classList.add(editDeactive);
        cEInput[i].classList.remove(editActive);
        cEIBtn[i].classList.add(editDeactive);
        cEIBtn[i].classList.remove(editActive);
        if (cEIBtn[i].value == reviewNum) {
            cEInput[i].classList.remove(editDeactive);
            cEInput[i].classList.add(editActive);
            cEIBtn[i].classList.remove(editDeactive);
            cEIBtn[i].classList.add(editActive);
        }
    }
}


function init(){

    Array.from(cEBtn).forEach(reviewNum => reviewNum.addEventListener("click", reviewEdit));
}

init();