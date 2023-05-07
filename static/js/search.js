function searchPlayers() {
  const searchInput = document.getElementById("searchInput");
  const suggestions = document.getElementById("suggestions");
  const searchValue = searchInput.value;

  if (searchValue.length < 2) {
    suggestions.innerHTML = "";
    return;
  }

  fetch(`/home/search/?q=${searchValue}`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      "X-Requested-With": "XMLHttpRequest", // Required for Django to treat the request as AJAX
      "X-CSRFToken": document.getElementsByName("csrfmiddlewaretoken")[0].value, // Django CSRF token
    },
  })
    .then((response) => response.json())
    .then((data) => {
      suggestions.innerHTML = "";
      data.players.forEach((player) => {
        const playerDiv = document.createElement("div");
        playerDiv.className = "suggested-player";
        playerDiv.innerHTML = `${player.name} (${player.position})`;
        playerDiv.onclick = function () {
          addPlayer(player.id);
        };
        suggestions.appendChild(playerDiv);
      });
    });
}

function addPlayer(playerId) {
  fetch(`/home/add_player_to_team/${playerId}/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": document.getElementsByName("csrfmiddlewaretoken")[0].value,
      "X-Requested-With": "XMLHttpRequest",
    },
    body: JSON.stringify({ player_id: playerId }),
  })
    .then((response) => {
      console.log(response);
      if (response.ok) {
        return response.json();
      } else {
        throw new Error("Error adding player to team");
      }
    })
    .then((data) => {
      console.log(data);
      if (data.success) {
        alert("Player added to your team");
      } else {
        alert(data.error);
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}
