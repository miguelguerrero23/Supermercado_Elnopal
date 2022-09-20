// Set new default font family and font color to mimic Bootstrap's default styling


$(document).ready(function(){
    
    Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
    Chart.defaults.global.defaultFontColor = '#292b2c';
    var ctx = document.getElementById("entrega-fecha");
    var myLineChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: $('#tags-area').html().slice(0,-1).split(','),
            datasets:[{
                label: "Ventas",
                lineTension: 0.3,
                backgroundColor: "rgba(255,103,18,0.2)",
                borderColor: "rgba(255,103,18,1)",
                pointRadius: 5,
                pointBackgroundColor: "rgba(255,103,18,1)",
                pointBorderColor: "rgba(255,255,255,0.8)",
                pointHoverRadius: 5,
                pointHoverBackgroundColor: "255,103,18,1)",
                pointHitRadius: 50,
                pointBorderWidth: 2,
                data: $('#data-area').html().slice(0,-1).split(',')
        }]},
    options: {
    scales: {
        xAxes: [{
            time: {
                unit: 'date'
            },
            gridLines: {
                display: false
            },
            ticks: {
                maxTicksLimit: 7
            }
        }],
        yAxes: [{
            ticks: {
                min: 0,
                max: 6000,
                maxTicksLimit: 5
            },
            gridLines: {
                color: "rgba(0, 0, 0, .125)",
            }
        }],
    },
    legend: {
        display: false
    }
    }
    });
    
    });
    
    