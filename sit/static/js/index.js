function setupConditionChart(excellent, good, fair, poor) {
    let ctx = $('#conditionChart');
    const conditionChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Excellent', 'Good', 'Fair', 'Poor'],
            datasets: [{
                label: '# of Items',
                data: [excellent, good, fair, poor],
                backgroundColor: [
                    'rgba(53, 161, 71, 1.0)',
                    'rgba(61, 55, 189, 1.0)',
                    'rgba(99, 99, 99, 1.0)',
                    'rgba(158, 33, 33, 1.0)',
                ],
                borderWidth: 1
            }]
        },
        options: {
            plugins: {
                title: {
                    display: true,
                    text: 'Condition Breakdown'
                }
            }
        },
    });
}