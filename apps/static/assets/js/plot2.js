function updateChartToPlot2(myChart) {
    myChart.data.labels = ["Jun", "Jul", "Aug", "Sep", "Oct"];
    myChart.data.datasets[0].data = [50, 40, 30, 20, 10];
    myChart.data.datasets[0].label = "Revenue 2023";
    myChart.data.datasets[0].backgroundColor = "rgba(255, 99, 132, 0.2)";
    myChart.data.datasets[0].borderColor = "rgba(255, 99, 132, 1)";
    myChart.update();
}
