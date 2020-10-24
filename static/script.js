var element = document.querySelector(".door");
element.addEventListener("click", toggleDoor);
var element2 = document.querySelector("body");
var element3 = document.querySelector("p");

function toggleDoor() {
  element.classList.add("doorOpen");
  element2.style.backgroundColor = "#05c46b"
  
}