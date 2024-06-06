var workoutCards = document.querySelectorAll(".workout-card");
workoutCards.forEach(function (card) {
  card.addEventListener("click", function () {
    var popupWrap = this.querySelector(".exercise-popup-wraps");
    popupWrap.classList.add("active");
  });
});

var closeBtns = document.querySelectorAll(".cross");
closeBtns.forEach(function (btn) {
  btn.addEventListener("click", function (event) {
    var popupWrap = this.closest(".exercise-popup-wraps");
    popupWrap.classList.remove("active");
    event.stopPropagation();
  });
});
