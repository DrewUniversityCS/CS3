function createChart(ids, dataLables, dataPoints) {

    const check = document.getElementById(ids).style.height || '0px';

    if (document.getElementById(ids).style.height === '0px' || check==='0px') {
        document.getElementById(ids).style.height = "fit-content";
        var ctx = document.getElementById(ids).getContext('2d');
        var chart = new Chart(ctx, {
            // The type of chart we want to create
            type: 'line',

            // The data for our dataset
            data: {
                labels: dataLables,
                datasets: [{
                    label: 'Count',
                    backgroundColor: '#059669',
                    borderColor: '#047857',
                    data: dataPoints
                }]
            },

            // Configuration options go here
            options: {}
        });
    } else {
        document.getElementById(ids).style.height = "0px";
    }
}
