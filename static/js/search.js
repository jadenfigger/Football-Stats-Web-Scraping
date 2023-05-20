let selectedPlayerId = null;

function selectPlayer(playerId, playerName, playerPosition) {
  selectedPlayerId = playerId;
  const selectedPlayerDiv = document.getElementById("selected-player");
  selectedPlayerDiv.innerHTML = `Selected Player: ${playerName} (${playerPosition})`;
  selectedPlayerDiv.style.display = "block";
}

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
      "X-Requested-With": "XMLHttpRequest",
      "X-CSRFToken": document.getElementsByName("csrfmiddlewaretoken")[0].value,
    },
  })
    .then((response) => response.json())
    .then((data) => {
      suggestions.innerHTML = "";

      data.players.forEach((player) => {
        const playerButton = document.createElement("button");
        playerButton.className = "suggested-player";
        playerButton.type = "button";
        playerButton.textContent = `${player.name} (${player.position})`;
        playerButton.onclick = function () {
          selectPlayer(player.id, player.name, player.position);
          suggestions.innerHTML = ""; // Close the suggestions box
        };
        suggestions.appendChild(playerButton);
      });
    });
}

function addPlayer(playerId, playerToDrop) {
  console.log("addPlayer function called with playerId:", playerId);
  const url = `/home/add_player_to_team/${playerId}/${playerToDrop}/`;
  fetch(url, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      "X-Requested-With": "XMLHttpRequest",
      "X-CSRFToken": document.getElementsByName("csrfmiddlewaretoken")[0].value,
    },
  })
    .then((response) => {
      console.log(response);
      if (response.ok) {
        return response.json();
      } else {
        throw new Error("Error fetching player information");
      }
    })
    .then((data) => {
      const selectedPlayerDiv = document.getElementById("selected-player");
      selectedPlayerDiv.innerHTML = `Selected Player: ${data.player.name} (${data.player.position})`;
      selectedPlayerDiv.style.display = "block";
      location.reload();
    })
    .catch((error) => {
      console.error("Error in addPlayer:", error);
    });
}

function proposeTransaction() {
  const playerToDropSelect = document.getElementById("player_to_drop");
  const playerToDrop = playerToDropSelect.value;

  if (selectedPlayerId && playerToDrop) {
    addPlayer(selectedPlayerId, playerToDrop);
    alert("Transaction proposed");
  } else {
    alert("Please select a player to add and a player to drop");
  }
}

function dropPlayer(playerId) {
  fetch(`/home/drop_player/${playerId}/`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      "X-Requested-With": "XMLHttpRequest",
      "X-CSRFToken": document.getElementsByName("csrfmiddlewaretoken")[0].value,
    },
  })
    .then((response) => {
      if (response.ok) {
        return response.json();
      } else {
        throw new Error("Error dropping player");
      }
    })
    .then((data) => {
      if (data.success) {
        // Refresh the page after the player is dropped
        location.reload();
      } else {
        console.error("Error dropping player:", data.error);
      }
    })
    .catch((error) => {
      console.error("Error in dropPlayer:", error);
    });
}
