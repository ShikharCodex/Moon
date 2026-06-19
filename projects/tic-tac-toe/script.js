'use strict';

const cells = Array.from(document.querySelectorAll('.cell'));
const statusEl = document.getElementById('status');
const resetBtn = document.getElementById('reset');

let board = Array(9).fill(null);
let currentPlayer = 'X';
let gameActive = true;

const winningCombos = [
  [0,1,2], [3,4,5], [6,7,8],
  [0,3,6], [1,4,7], [2,5,8],
  [0,4,8], [2,4,6]
];

function updateStatus(msg) { statusEl.textContent = msg; }

function getWinLine(player) {
  for (const [a,b,c] of winningCombos) {
    if (board[a] === player && board[b] === player && board[c] === player) return [a,b,c];
  }
  return null;
}

function handleCellClick(e) {
  const cell = e.currentTarget;
  const index = parseInt(cell.dataset.index, 10);
  if (!gameActive || board[index]) return;

  board[index] = currentPlayer;
  cell.textContent = currentPlayer;
  cell.classList.add(`p-${currentPlayer.toLowerCase()}`);
  cell.setAttribute('aria-label', `Cell ${index + 1}: ${currentPlayer}`);

  const winLine = getWinLine(currentPlayer);
  if (winLine) {
    gameActive = false;
    updateStatus(`Player ${currentPlayer} wins!`);
    winLine.forEach(i => cells[i].classList.add('win'));
    return;
  }

  if (board.every(v => v)) {
    gameActive = false;
    updateStatus(`It's a draw!`);
    return;
  }

  currentPlayer = currentPlayer === 'X' ? 'O' : 'X';
  updateStatus(`Player ${currentPlayer}'s turn`);
}

cells.forEach(btn => btn.addEventListener('click', handleCellClick));

resetBtn.addEventListener('click', resetGame);

function resetGame() {
  board = Array(9).fill(null);
  currentPlayer = 'X';
  gameActive = true;
  updateStatus(`Player ${currentPlayer}'s turn`);
  cells.forEach((cell, i) => {
    cell.textContent = '';
    cell.classList.remove('p-x', 'p-o', 'win');
    cell.setAttribute('aria-label', `Cell ${i + 1}: empty`);
  });
}
