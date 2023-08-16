const cells = document.querySelectorAll(".cell");
const statusText = document.querySelector("#statusText");
const restartBtn = document.querySelector("#restartBtn");
const winConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
];

let options = ["", "", "", "", "", "", "", "", ""];
let currentPlayer = "X";
let running = false;

initializeGame();

function initializeGame(){
    cells.forEach(cell => cell.addEventListener("click", cellClicked));
    restartBtn.addEventListener("click", restartGame);
    statusText.textContent = `${currentPlayer}'s turn`;

    running = true;
}

function cellClicked() {
    const cellIndex = this.getAttribute("cellIndex");

    if (options[cellIndex] != "" || !running) {
        return;
    }

    updateCell(this, cellIndex);  // Human makes the move
    checkWinner();  // Check if human wins or it's a draw

    if (running) {  // If the game is still running, AI makes its move
        aiMove();
        checkWinner();  // Check if AI wins or it's a draw
    }
}

function updateCell(cell, index){
    options[index] = currentPlayer;
    cell.textContent = currentPlayer;
}

function changePlayer() {
    currentPlayer = (currentPlayer == "X") ? "O" : "X";
    statusText.textContent = `${currentPlayer}'s turn`;
}

function checkWinner(){

    let roundWon = false;

    for(let i = 0; i < winConditions.length; i++){
        const condition = winConditions[i];
        const cellA = options[condition[0]];
        const cellB = options[condition[1]];
        const cellC = options[condition[2]];

        if(cellA == "" || cellB == "" || cellC == ""){
            continue;
        }

        if(cellA == cellB && cellB == cellC){
            roundWon = true;
            break;
        }
    }

    if(roundWon){
        statusText.textContent = `${currentPlayer} wins!`;
        running = false;
    }

    else if(!options.includes("")){
        statusText.textContent = `Draw!`;
        running = false;
    }

    else{
        changePlayer();
    }
}

function restartGame(){
    currentPlayer = "X";
    options = ["", "", "", "", "", "", "", "", ""];
    statusText.textContent = `${currentPlayer}'s turn`;
    cells.forEach(cell => cell.textContent = "");
    running = true;
}

function aiMove() {
    let bestMove = minimax(options, 0);
    options[bestMove] = "O";
    
    cells[bestMove].textContent = "O";
}

function utility(game_state) {
    if (check_for_winner(game_state) == "X") 
        return 10;
    else if (check_for_winner(game_state) == "O") 
        return -10;
    else 
        return 0;
}

function update(action) {
    if (player(options) == "X") {
        options[action] = "X"
    }
    else {
        options[action] = "O"
    }
}

function terminal(game_state) {
    for (let i = 0; i < 9; i++) {
        if (game_state[i] == "")
            return false;
    }
    return true;
}

function actions(game_state) {
    let moves = []

    for (let i = 0; i < 9; i++) {
        if (game_state[i] == "")
            moves.push(i)
    }
    return moves
}

function check_for_winner(game_state) {
    for (let i = 0; i < 8; i++) {
        if (game_state[winConditions[i][0]] != "" && game_state[winConditions[i][0]] == game_state[winConditions[i][1]] && game_state[winConditions[i][1]] == game_state[winConditions[i][2]]) {
            if (game_state[winConditions[i][0]] == "X")
                return "X";
            else
                return "O";
        }
    }       
    return 1;
}

function update_temp(game_state, action) {
    let temp = []

    for (let i = 0; i < 9; i++) {
        temp[i] = game_state[i]
    }
    for (let j = 0; j < 9; j++) {
        if (j == action && temp[j] == "") {
            if (player(game_state) == "X")
                temp[j] = "X"
            else    
                temp[j] = "O"
        }
    }
    return temp;
}

function player(board) {
    let x = 0
    let o = 0

    for (let i = 0; i < 9; i++) {
        if (board[i] == "X")
            x++
        if (board[i] == "O")
            o++
    }
    if (o >= x)
        return "X"
    else    
        return "O"
}

function minimax(game_state, depth) {
    if (player(game_state) == "X") {
        let best_value = Number.NEGATIVE_INFINITY;
        let best_move = null;

        for (let a = 0; a < actions(game_state).length; a++) {
            value = Math.max(best_value, min_value(update_temp(game_state, actions(game_state)[a]), depth + 1));
            if (value > best_value) {
                best_value = value;
                best_move = actions(game_state)[a];
            }
        }  
        return best_move;
    }

    else {
        let best_value = Number.POSITIVE_INFINITY;
        let best_move = null;
        
        for (let a = 0; a < actions(game_state).length; a++) {
            value = Math.min(best_value, max_value(update_temp(game_state, actions(game_state)[a]), depth + 1));
            if (value < best_value) {
                best_value = value;
                best_move = actions(game_state)[a];
            }
        }  
        return best_move;
    }
}

function max_value(game_state, depth) {
    if (check_for_winner(game_state) == "X" || check_for_winner(game_state) == "O")
        return utility(game_state);
    if (terminal(game_state) == true)
        return utility(game_state);

    let best_value = Number.NEGATIVE_INFINITY;
    for (let a = 0; a < actions(game_state).length; a++) {
        value = Math.max(best_value, min_value(update_temp(game_state, actions(game_state)[a]), depth + 1));
        best_value = Math.max(value, best_value);
    }
        
    return best_value - depth;
}
        
function min_value(game_state, depth) {
    if (check_for_winner(game_state) == "X" || check_for_winner(game_state) == "O")
        return utility(game_state);
    if (terminal(game_state) == true)
        return utility(game_state);

    let best_value = Number.POSITIVE_INFINITY;
    for (let a = 0; a < actions(game_state).length; a++) {
        value = Math.min(best_value, max_value(update_temp(game_state, actions(game_state)[a]), depth + 1));
        best_value = Math.min(value, best_value);
    }    
    return best_value - depth;
}
