$(document).ready(function () {
  // Click event for workout card
  $(".workout-card").click(function () {
    // Add 'active' class to exercise popup
    $(this).find(".exercise-popup-wraps").addClass("active");
  });

  // Click event for close button inside exercise popup
  $(".cross").click(function (event) {
    // Remove 'active' class from exercise popup
    $(this).closest(".exercise-popup-wraps").removeClass("active");
    // Stop the propagation of the click event
    event.stopPropagation();
  });
});
