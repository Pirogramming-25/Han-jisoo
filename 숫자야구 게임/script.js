let answer = [];
let attempts = 9;

function init_game() {
    attempts = 9;
    document.getElementById("attempts").innerText = attempts;

    document.getElementById("results").innerHTML = "";
    document.getElementById("game-result-img").src = "";

    document.querySelector(".submit-button").disabled = false;

    document.getElementById("number1").value ="";
    document.getElementById("number2").value ="";
    document.getElementById("number3").value ="";

    answer =[];

    while(answer.length < 3) {
        let random = Math.floor(Math.random() * 10);

        if (!answer.includes(random)) {
            answer.push(random);
        }
    }
    console.log(answer);
}
function check_numbers() {
    const num1 = document.getElementById("number1").value;
    const num2 = document.getElementById("number2").value;
    const num3 = document.getElementById("number3").value;

    if (num1 == "" || num2 == "" || num3 == "") {
        clearInput();
        return;
    }
    
    const user = [Number(num1), Number(num2), Number(num3)];

    let strike = 0;
    let ball = 0;

    for (let i = 0; i < 3; i++) {
        if (user[i] == answer[i]) strike ++;
        else if (answer.includes(user[i])) ball++;
    }

let result = "";

if (strike === 0 && ball === 0) result = "0";
else result = `${strike}S ${ball}B`;

document.getElementById("results").innerHTML += `
    <div>${user.join("")} : ${result}</div>
`;

attempts --;
document.getElementById("attempts").innerText = attempts;

if (strike == 3) {
    document.getElementById("game-result-img").src = "success.png";
    document.querySelector(".submit-button").disabled = true;
}
else if (attempts == 0) {
    document.getElementById("game-result-img").src = "fail.png";
    document.querySelector(".submit-button").disabled = true;
}
clearInput();

}
function clearInput() {
    document.getElementById("number1").value = "";
    document.getElementById("number2").value = "";
    document.getElementById("number3").value = "";

    document.getElementById("number1").focus();
}
window.onload = init_game;