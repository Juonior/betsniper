var radioButtons = document.querySelectorAll('input[type="radio"]');

radioButtons.forEach(function(radioButton) {
    radioButton.addEventListener('change', function() {
        // Отключаем другой радио-баттон
        radioButtons.forEach(function(rb) {
            if (rb !== radioButton) {
                rb.checked = false;
            }
        });
    });
});

function handleTableChanges(event) {
    var target = event.target;

    // Проверка, принадлежит ли измененный элемент таблице с классом "Calc"
    if (target.closest(".Calc")) {
        var kf_1 = parseFloat(document.getElementById("kf_1").value);
        var summ_1_element = document.getElementById("summ_1")
        var summ_1 = parseFloat(summ_1_element.value);
        var kf_2 = parseFloat(document.getElementById("kf_2").value);
        var summ_2_element = document.getElementById("summ_2")
        var summ_2 = parseFloat(summ_2_element.value);
        var radio_1 = document.getElementById("radio_1").checked;

        // Расчет суммы ставки на второе событие
        var money_k2 = Math.round((summ_1 * kf_1) / kf_2);

        var profit_1_element = document.getElementById("profit_1")
        var profit_2_element = document.getElementById("profit_2")
        // Расчет профита
        var profit = (summ_1 * kf_1) - (money_k2 + summ_1);
        var profit2 = (money_k2 * kf_2) - (money_k2 + summ_1);

        if (radio_1) {
            // Если radio_1 выбран
            if (!isNaN(money_k2)){
                summ_2_element.value = money_k2;
            }
            profit_1_element.textContent = profit.toFixed(1);
            profit_2_element.textContent = profit2.toFixed(1);
        
            if (profit > 0) {
                profit_1_element.style.color = "green";
            } else {
                profit_1_element.style.color = "red";
            }
        
            if (profit2 > 0) {
                profit_2_element.style.color = "green";
            } else {
                profit_2_element.style.color = "red";
            }
        } else {
            // Если radio_2 выбран
            // Ваш код, если radio_2 выбран
            // Например, можно обновить сумму для первого коэффициента
            var newSumm1 = Math.round((summ_2 * kf_2) / kf_1);
            if (!isNaN(newSumm1)){
                summ_1_element.value = newSumm1;
            }
            // Расчет профита для второго случая
            var newMoney_k2 = Math.round((newSumm1 * kf_1) / kf_2);
            var newProfit = (newSumm1 * kf_1) - (newMoney_k2 + newSumm1);
            
            // Рассчитываем профит для второго случая
            var newMoney_k2 = Math.round((newSumm1 * kf_1) / kf_2);
            var newProfit2 = (newMoney_k2 * kf_2) - (newMoney_k2 + newSumm1);

            profit_1_element.textContent = newProfit.toFixed(1);
            profit_2_element.textContent = newProfit2.toFixed(1);

            if (newProfit > 0) {
                profit_1_element.style.color = "green";
            } else {
                profit_1_element.style.color = "red";
            }

            if (newProfit2 > 0) {
                profit_2_element.style.color = "green";
            } else {
                profit_2_element.style.color = "red";
            }
        }
        
        var profit_kf_element = document.getElementById("profit_kf")
        var all_summ_element = document.getElementById("all_summ")
        profit_kf =  100 * (kf_1 / (1 + kf_1 / kf_2) - 1)
        if (!isNaN(profit_kf)){
            profit_kf_element.textContent = profit_kf.toFixed(2)+"%"
            if (profit_kf > 0) {
                profit_kf_element.style.color = "green";
            } else {
                profit_kf_element.style.color = "red";
            }
        }
        if (!isNaN( parseFloat(summ_1_element.value) + parseFloat(summ_2_element.value))){
            all_summ_element.textContent = parseFloat(summ_1_element.value) + parseFloat(summ_2_element.value);
        }
        // Ваши действия с полученными значениями
        // console.log("Коэффициент 1: " + kf_1);
        // console.log("Сумма 1: " + summ_1);
        // console.log("Коэффициент 2: " + kf_2);
        // console.log("Сумма 2: " + summ_2);
        // console.log("Сумма ставки на второе событие: " + money_k2);
        // console.log("Профит 1: " + profit);
        // console.log("Профит 2: " + profit2);
    }
}

var tables = document.querySelectorAll(".Calc");
for (var i = 0; i < tables.length; i++) {
    tables[i].addEventListener("input", handleTableChanges);
}
