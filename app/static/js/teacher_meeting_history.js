var xValues = ["Aanwezig", "Afwezig", "Afgemeld"];
var barColors = [
  "#1a8754",
  "#dc3545",
  "#6c757d"
];

new Chart("myChart", {
  type: "pie",
  data: {
    labels: xValues,
    datasets: [{
      backgroundColor: barColors,
      data: yValues
    }]
  },
  options: {
    title: {
      display: true,
      text: "World Wide Wine Production"
    }
  }
});