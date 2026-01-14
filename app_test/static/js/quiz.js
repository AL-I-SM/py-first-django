// Укажите URL WebSocket
const socket = new WebSocket('ws://' + window.location.host + '/ws/rating/');

// Обработчик открытия соединения
socket.onopen = () => {
    console.log('WebSocket подключен');
    getUserTable();
};

// Обработчик ошибок
socket.onerror = (error) => {
    console.error('WebSocket ошибка:', error);
};

// Обработчик получения сообщений
socket.onmessage = (event) => {

    const data = JSON.parse(event.data);
    if (data.type === 'rating_updates') {
        // Обновляем таблицу
        console.log('обновление рейтинга');
        updateRatingTable(data.content);
    }

    if (data.type === 'rating_table') {
        // Обновляем таблицу
        console.log('получена таблица рейтнига');
        updateRatingTable(data.content);
    }

    if (Array.isArray(data)) {
        console.log('is array!');
    }
};

// Обновление таблицы рейтинга
function updateRatingTable(ratingData) {
    const tbody = document.getElementById('ratingTable').getElementsByTagName('tbody')[0];

    // Очистить существующие строки
    tbody.innerHTML = '';

    for (const key in ratingData) {
        const row = tbody.insertRow();
        const userName = key;             // 'computer', 'computer1'
        const userData = ratingData[key]; // объект с score и time

        row.insertCell().textContent = userName;
        row.insertCell().textContent = userData.score;
        row.insertCell().textContent = userData.time;

    }

}

function getUserTable() {
    socket.send(JSON.stringify({ type: "table", user: currentUser }));
}

function appendUser() {
    socket.send(JSON.stringify({ type: "auth", user: currentUser }));

}
function joinAndRedirect() {
    appendUser();
    window.location.href = urlQuestions;
}
// Можно также отправлять сообщения, если потребуется
// socket.send(JSON.stringify({message: 'что-то'}));
