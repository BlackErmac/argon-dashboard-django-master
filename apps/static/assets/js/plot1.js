function updateChartToPlot1(myChart) {
    myChart.data.labels = ["Jan", "Feb", "Mar", "Apr", "May"];
    myChart.data.datasets[0].data = [10, 20, 30, 40, 50];
    myChart.data.datasets[0].label = "Revenue 2024";
    myChart.data.datasets[0].backgroundColor = "rgba(75, 192, 192, 0.2)";
    myChart.data.datasets[0].borderColor = "rgba(75, 192, 192, 1)";
    myChart.update();
}
