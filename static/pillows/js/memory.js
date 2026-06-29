let firstCard = null;
let secondCard = null;
let lockBoard = false;

const emojis = ["🐶", "🐱", "🦊", "🐻", "🐼", "🐨", "🐯", "🦁", "🐮", "🐷", "🐸", "🐵", "🐔", "🦄", "🐝", "🐛", "🦋", "🐌", "🐞", "🐢", "🐍", "🦖", "🦕", "🐙", "🦑", "🦀"];

function startGame() {
    const widthInput = parseInt(document.getElementById("width").value);
    const heightInput = parseInt(document.getElementById("height").value);
    if (inOutRange(widthInput, 4, 11)) {
        alert("Ширина має бути від 4 до 11");
        return;}

    if (inOutRange(heightInput, 3, 6)) {
        alert("Висота має бути від 3 до 6");
        return;}
    setupBoard(widthInput, heightInput);
}

function inOutRange(value, min, max) {
    return value < min || value > max;
}
function setupBoard(width, height) {
    const board = document.getElementById("board");
    board.innerHTML = "";
    board.style.gridTemplateColumns = `repeat(${width}, 100px)`;
    board.style.gridTemplateRows = `repeat(${height}, 100px)`;
    const numberOfCards = width * height;
    const selectedEmojis = shuffleArray(emojis).slice(0, numberOfCards / 2);
    const doubleEmojis = shuffleArray([...selectedEmojis, ...selectedEmojis]);
    if (numberOfCards % 2 == 1){
        doubleEmojis.push('🃏');
    }
    const gameEmojis = shuffleArray(doubleEmojis);
    gameEmojis.forEach(emojis => {
        const card = document.createElement("div");
        card.classList.add("card");
        card.dataset.emojis = emojis;      

        const elementEmojis = document.createElement('span');
        elementEmojis.textContent = emojis;
        elementEmojis.style.visibility = 'hidden';

        card.appendChild(elementEmojis);
        card.addEventListener('click', () => flipCard(card, elementEmojis));
        board.appendChild(card);
    });
}
function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
}
function flipCard(card, elementEmoji){
    if (lockBoard) return;
    if (card === firstCard || card.classList.contains('matched')){
        return;
    }
    card.classList.add('flipped');
    elementEmoji.style.visibility = 'visible'; 

    if (firstCard === null){
        firstCard = card;
    } else {
        secondCard = card;
        checkForMatch();
    }
}
function checkForMatch(){
    const isMatch = firstCard.dataset.emojis === secondCard.dataset.emojis;
    if (isMatch){
        firstCard.classList.add('matched');
        secondCard.classList.add('matched');
        firstCard = null;
        secondCard = null;
    } else {
        unflipCards();
    }
}   

function unflipCards(){
    lockBoard = true;
    setTimeout(() => {
        // hide emoji spans and flip cards back
        const firstEmoji = firstCard && firstCard.querySelector('span');
        const secondEmoji = secondCard && secondCard.querySelector('span');
        if (firstEmoji) firstEmoji.style.visibility = 'hidden';
        if (secondEmoji) secondEmoji.style.visibility = 'hidden';
        if (firstCard) firstCard.classList.remove('flipped');
        if (secondCard) secondCard.classList.remove('flipped');
        firstCard = null;
        secondCard = null;
        lockBoard = false;
    }, 1000);
}

document.getElementById("start-button").addEventListener("click", startGame);