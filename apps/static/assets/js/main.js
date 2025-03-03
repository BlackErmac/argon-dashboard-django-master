document.addEventListener("DOMContentLoaded", function () {
    const ctx = document.getElementById("chart-bars").getContext("2d");

    // Initialize Chart.js with default data
    const myChart = new Chart(ctx, {
        type: "line",
        data: {
            labels: ["Jan", "Feb", "Mar", "Apr", "May"],
            datasets: [{
                label: "Initial Data",
                data: [10, 20, 30, 40, 50],
                borderColor: "rgba(75, 192, 192, 1)",
                backgroundColor: "rgba(75, 192, 192, 0.2)"
            }]
        },
        options: { responsive: true }
    });

    // // Event listeners for buttons
    // document.getElementById("btnPlot1").addEventListener("click", function () {
    //     updateChartToPlot1(myChart);
    // });

    // document.getElementById("btnPlot2").addEventListener("click", function () {
    //     updateChartToPlot2(myChart);
    // });
});
