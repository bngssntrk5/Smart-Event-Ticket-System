document.addEventListener("DOMContentLoaded", function () {
  const buyButtons = document.querySelectorAll(".buy-ticket-btn");

  buyButtons.forEach((button) => {
    button.addEventListener("click", function (e) {
      const ticketType = this.getAttribute("data-type") || "Ticket";
      const confirmPurchase = confirm(
        `Are you sure you want to purchase a ${ticketType}?`,
      );

      if (!confirmPurchase) {
        e.preventDefault();
        console.log("Ticket purchase cancelled by user.");
      } else {
        console.log("Ticket purchase confirmed, redirecting to backend...");
      }
    });
  });
});
