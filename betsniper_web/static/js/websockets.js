// websockets.js

const inputEvent = new Event("input", { bubbles: true });
const socket = io.connect(window.location.origin);

socket.on('connect', function () {
    console.log('Connected to the server.');
});

// Создаем множество (Set) для хранения названий скрытых событий
const hiddenEventNames = new Set();

socket.on('update_events', function (data) {
    const eventsFlaskArray = data.events_flask;
    const tableBody = document.querySelector('tbody.events');
    tableBody.innerHTML = ''; // Очищаем существующее содержимое
    eventsFlaskArray.sort((a, b) => b.profit - a.profit);
    eventsFlaskArray.forEach(newEvent => {
        const currentTime = new Date(); // Текущее время

        const timeElapsed = Math.floor((currentTime - new Date(newEvent.time)) / 1000);
        if (timeElapsed > 0) {
            const timeElapsedText = formatTimeElapsed(timeElapsed);

            const eventRow1 = document.createElement('tr');

            const eventName = newEvent.matchName1;

            const eventContainer = document.createElement('div');
            eventContainer.dataset.eventData = JSON.stringify(newEvent);

            if (!hiddenEventNames.has(eventName)) {
                // Если событие не скрыто, добавляем его в таблицу
                const eventData1 = [
                    `<img src="/static/images/calc.png" class="calc-event" kf_1="${newEvent.coefficient1}" kf_2="${newEvent.coefficient2}" site_1="${newEvent.site1}" site_2="${newEvent.site2}"><img src="/static/images/remove.png" class="delete-event" data-name="${eventName}" alt="Игнорировать событие"><img src="/static/images/tennis.png" alt="Теннис"><br>${timeElapsedText}`,
                    newEvent.profit,
                    `<a href="${newEvent.link1}">${newEvent.site1}</a><br><a href="${newEvent.link2}">${newEvent.site2}</a>`,
                    `<img src="/static/images/copy.png" class="copy-match" data-copy="${eventName}">${eventName}<br><img src="/static/images/copy.png" class="copy-match" data-copy="${newEvent.matchName2}">${newEvent.matchName2}`,
                    `${newEvent.type1}<br>${newEvent.type2}`,
                    `${newEvent.coefficient1}<br>${newEvent.coefficient2}`
                ];

                eventData1.forEach((data, index) => {
                    const cell = document.createElement('td');
                    const div = document.createElement('div');
                    div.innerHTML = data;
                    cell.appendChild(div);
                    eventRow1.appendChild(cell);
                });

                tableBody.appendChild(eventRow1);
            }
        }

    });

    const CalcElements = document.querySelectorAll('.calc-event');
    CalcElements.forEach(element => {
        element.addEventListener('click', function () {
            // Find the closest parent tr element
            // document.getElementById("kontora_1").textContent = (this.getAttribute('site_1'))
            // document.getElementById("kontora_2").textContent = (this.getAttribute('site_2'))
            document.getElementById("kf_1").value = this.getAttribute('kf_1')
            document.getElementById("kf_2").value = this.getAttribute('kf_2')
            document.getElementById("kf_1").dispatchEvent(inputEvent);
        });
    });
    const copyMatchElements = document.querySelectorAll('.copy-match');
    copyMatchElements.forEach(element => {
        element.addEventListener('click', function () {
            const textToCopy = this.getAttribute('data-copy');

            // Создаем временный элемент textarea для копирования текста в буфер обмена
            const tempTextarea = document.createElement('textarea');
            tempTextarea.value = textToCopy;
            document.body.appendChild(tempTextarea);
            tempTextarea.select();
            document.execCommand('copy');
            document.body.removeChild(tempTextarea);

            Swal.fire({
                icon: 'success',
                title: 'Скопировано',
                text: `Название матча "${textToCopy}" скопировано в буфер обмена.`,
                timer: 1000, // Время отображения окна (1 секунда)
                showConfirmButton: false, // Убрать кнопку "OK"
            });
        });
    });

    const deleteEventButtons = document.querySelectorAll('.delete-event');
    deleteEventButtons.forEach(button => {
        button.addEventListener('click', function () {
            const eventName = this.getAttribute('data-name');
            Swal.fire({
                icon: 'question',
                title: "Скрытие события",
                text: `Вы уверены, что хотите скрыть событие - "${eventName}"?`,
                showConfirmButton: true,
                showCancelButton: true, // Показать кнопку "Отмена"
                confirmButtonText: 'Да', // Текст кнопки подтверждения
                cancelButtonText: 'Отмена', // Текст кнопки отмены
                preConfirm: () => {
                    // Этот блок выполняется после нажатия на кнопку подтверждения
                    hiddenEventNames.add(eventName); // Добавляем название скрытого события в множество
                    const eventRow = this.closest('tr'); // Находим ближайшую строку
                    eventRow.style.display = 'none'; // Скрываем строку
                },
            });
        });
    });
});


function formatTimeElapsed(seconds) {
    if (seconds < 60) {
        if (seconds === 0) {
            return '0 сек';
        }
        return `${seconds} сек`;
    } else {
        const minutes = Math.floor(seconds / 60);
        const remainingSeconds = seconds % 60;
        return `${minutes} мин ${remainingSeconds} сек`;
    }
}
