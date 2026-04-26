document.addEventListener("DOMContentLoaded", function () {
  const buyButtons = document.querySelectorAll(".buy-ticket-btn");

  buyButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const eventName = this.getAttribute("data-type");
      const eventId = this.getAttribute("data-id");

      if (confirm(`Purchase ticket for ${eventName}?`)) {
        fetch("/api/buy", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ event_id: eventId }),
        })
          .then((res) => res.json())
          .then((data) => {
            if (data.status === "success") {
              alert("Success! Code: " + data.code);
              location.reload();
            } else {
              alert("Error: " + data.message);
            }
          });
      }
    });
  });
});
