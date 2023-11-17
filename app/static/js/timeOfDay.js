let today = new Date();
const time = today.getHours();

if (time > 0 && time < 5) {
    document
    .getElementById("greeting")
    .insertAdjacentHTML("afterbegin", "Het is tijd om naar bed te gaan ");
}
if (time >= 5 && time < 12) {
    document
    .getElementById("greeting")
    .insertAdjacentHTML("afterbegin", "Goedemorgen ");
}
if (time >= 12 && time < 18) {
    document
    .getElementById("greeting")
    .insertAdjacentHTML("afterbegin", "Goedemiddag ");
}
if (time >= 18 && time < 24) {
    document
    .getElementById("greeting")
    .insertAdjacentHTML("afterbegin", "Goedenavond ");
}