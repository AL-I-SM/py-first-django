const socket = new WebSocket('ws://' + window.location.host + '/ws/rating/');

    socket.onopen = () => {
        console.log('WebSocket подключен');
        getUserTable();
        getQuestion('');
    };

    // Обработчик ошибок
    socket.onerror = (error) => {
        console.error('WebSocket ошибка:', error);
    };

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

        if (data.type === 'question') {
            // Обновляем вопрос
            console.log(data.user)

            if (data.user === currentUser) {
                console.log('получен вопрос');
                updateDataQuestion(data.content);
            }
        }

        if (data.type === 'start') {
            console.log('начало теста');
            getQuestion('')
        }

        if (data.type === 'end_test') {
            // Закончить тест
            if (data.user === currentUser) {
                endTest(data.content);
            }
        }
    };

    function updateRatingTable(ratingData) {
        const tbody = document.getElementById('ratingTable').getElementsByTagName('tbody')[0];
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

    function appendUser() {
        const waitInfo = document.getElementById('waitInfo');
        waitInfo.textContent = "тест закончен";
        socket.send(JSON.stringify({
            type: "auth",
            user: currentUser
        }));
    }

    function getUserTable() {
        socket.send(JSON.stringify({
            type: "table",
            user: currentUser
        }));
    }

    function manualStartTest() {
        socket.send(JSON.stringify({
            type: "start",
            user: currentUser
        }));
    }

    function sendAnswer() {

        const radios = document.querySelectorAll('input[name="answer"]');
        const answered_at = new Date();

        let answer = '';

        console.log('время: ', answered_at);

        if (radios.length > 0) {
            // Есть радиокнопки
            radios.forEach(r => {
                if (r.checked) answer = r.value;
            });
        }
        else {
            // Поле для ввода
            answer = document.getElementById('answerInput').value;
        }

        if (!answer) {
            alert('Пожалуйста, введите ответ');
            return;
        }

        questionId = document.getElementById('questionId').textContent;

        socket.send(JSON.stringify({
            type: "answer",
            user: currentUser,
            answer: answer,
            question_id: questionId,
            answered_at: answered_at
        }));
        console.log('ответ отправлен: ', answer, 'id :', questionId);
        getQuestion('next');
    }

    function getQuestion(state) {
        console.log('запрос: вопрос');
        socket.send(JSON.stringify({
            type: "question",
            user: currentUser,
            state: state
        }));
    }

    function updateDataQuestion(questionData) {
        console.log('обновлен вопрос');

        document.getElementById('answerOptions').hidden = false;
        document.getElementById('submitButton').hidden = false;
        document.getElementById('answerInput').hidden = false;
        document.getElementById('testQuestion').hidden = false;
        document.getElementById('waitInfo').hidden = true;
        document.getElementById('startTest').hidden = true;

        options = questionData.options;

        const optionsContainer = document.getElementById('answerOptions');
        const testQuestion = document.getElementById('testQuestion');
        const answerInput = document.getElementById('answerInput');
        const questionId = document.getElementById('questionId');

        optionsContainer.innerHTML = '';

        questionId.textContent = questionData.question_id;
        testQuestion.textContent = questionData.text;

        answerInput.value = "";

        if (options && options.length > 0) {
            // Есть варианты — создаем радиокнопки
            options.forEach((option, index) => {
                const label = document.createElement('label');
                label.id = 'radioBlock';
                label.style.display = 'block';
                const radio = document.createElement('input');
                radio.type = 'radio';
                radio.name = 'answer';
                radio.value = option;
                if (index === 0) radio.checked = true; // по умолчанию выбран первый

                label.appendChild(radio);
                label.appendChild(document.createTextNode(option));
                optionsContainer.appendChild(label);
            });
            // Показываем блок с радиокнопками
            document.getElementById('radioBlock').hidden = false;
            // скрываем поле для ввода
            document.getElementById('answerInput').hidden = true;
        } else {
            // Нет вариантов — показываем поле для ввода
            document.getElementById('answerInput').hidden = false;
            document.getElementById('answerInput').value = '';
        }
    }

    function endTest(questionData) {
        console.log('тест закончен');
        const waitInfo = document.getElementById('waitInfo');
        waitInfo.textContent = "тест закончен";

        document.getElementById('answerOptions').hidden = true;
        document.getElementById('submitButton').hidden = true;
        document.getElementById('answerInput').hidden = true;
        document.getElementById('testQuestion').hidden = true;
        document.getElementById('waitInfo').hidden = false;
        
    }
