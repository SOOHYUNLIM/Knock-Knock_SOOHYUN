const drawChart = (() => {
    const donut = (arr) => {
        let data = {labels: [], series: []}
        arr.forEach(item => {
            data.labels.push(item.category)
            data.series.push(item.count)
        })

        let options = {
            labelInterpolationFnc: function (value) {
                return value[0]
            }
        }

        let responsiveOptions = [
            ['screen and (min-width: 640px)', {
                chartPadding: 30,
                labelOffset: 100,
                labelDirection: 'explode',
                labelInterpolationFnc: function (value) {
                    return value;
                }
            }],
            ['screen and (min-width: 1024px)', {
                labelOffset: 80,
                chartPadding: 20
            }]
        ]
        new Chartist.Pie('.ct-Donutchart', data, options, responsiveOptions);
    }

    const line = (arr) => {
        let data = {labels: null, series: []}

        let type = arr.pop().type
        let labels = []
        let graphAll = new Array(24).fill(0)
        let graphMen = new Array(24).fill(0)
        let graphWomen = new Array(24).fill(0)

        if (type === 'H') {
            for (let i = 1; i < 24; i++)
                labels.push(i)
            arr.forEach(item => graphAll[item.date] += item.count)
        } else if (type === 'D') {
            labels = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
            graphAll.length = 7
            graphMen.length = 7
            graphWomen.length = 7
            arr.forEach(item => {
                let idx = item.date - 1
                graphAll[idx] = graphAll[idx] + item.count
                item.sex === 'M' ? graphMen[idx] += item.count : graphWomen[idx] += item.count
            })
        }
        data.labels = labels
        data.series.push(graphAll)
        data.series.push(graphMen)
        data.series.push(graphWomen)

        new Chartist.Line('.ct-chart', data,
            {
                fullWidth: true,
                chartPadding: {
                    right: 40
                }
            });
    }

    return {donut, line}
})()