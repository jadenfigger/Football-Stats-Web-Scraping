let selectedPlayerId = null;
let playerToDrop = null;

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

function proposeTransaction() {
  const playerToDropSelect = document.getElementById("id_player_to_drop");
  // const playerToDrop = playerToDropSelect.value;

  if (selectedPlayerId && playerToDrop) {
    const csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0].value;
    const url = `/home/trade_player/${selectedPlayerId}/${playerToDrop}/`;
    fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": csrfToken,
      },
    })
      .then((response) => {
        if (response.ok) {
          alert("Transaction proposed");
          location.reload();
        } else {
          throw new Error("Error proposing transaction");
        }
      })
      .catch((error) => {
        console.error("Error in proposeTransaction:", error);
      });
  } else {
    alert("Please select a player to add and a player to drop");
  }
}


function dropPlayer(playerId) {
  const selectedPlayerDiv = document.getElementById("selected-player");
  selectedPlayerDiv.innerHTML = `Selected Player: ${data.player.name} (${data.player.position})`;
  selectedPlayerDiv.style.display = "block";
  location.reload();
}