type = ['primary', 'info', 'success', 'warning', 'danger'];

demo = {
  initDocChart: function() {
    chartColor = "#FFFFFF";
  },

  initDashboardPageCharts: function() {
    function changeText(value){
      console.log("test");
    };

    var chart_data = [];
    var ctx = document.getElementById("emotionDot").getContext('2d');
    var gradientStroke = ctx.createLinearGradient(0, 230, 0, 50);

    gradientStroke.addColorStop(1, 'rgba(72,72,176,0.1)');
    gradientStroke.addColorStop(0.4, 'rgba(72,72,176,0.0)');
    gradientStroke.addColorStop(0, 'rgba(119,52,169,0)');

var ctx = document.getElementById("Timeline").getContext("2d");
    var gradientStroke = ctx.createLinearGradient(0, 230, 0, 50);
    gradientStroke.addColorStop(1, 'rgba(29,140,248,0.05)');
    gradientStroke.addColorStop(0.4, 'rgba(29,140,248,0.0)');
    gradientStroke.addColorStop(0, 'rgba(29,140,248,0)');
  },

  // implement drawBarChart function
  drawBarChart: function(data){
    let barchart_ctx = document.getElementById("moodBarChart").getContext("2d");

    let gradientStroke = barchart_ctx.createLinearGradient(0, 230, 0, 50);

    gradientStroke.addColorStop(1, 'rgba(72,72,176,0.2)');
    gradientStroke.addColorStop(0.2, 'rgba(72,72,176,0.0)');
    gradientStroke.addColorStop(0, 'rgba(119,52,169,0)'); //purple colors

    let gradientChartOptionsConfigurationWithTooltipPurple = {
      maintainAspectRatio: false,
      legend: {
         display: true,
        position: 'bottom',
      },

      tooltips: {
        backgroundColor: '#f5f5f5',
        titleFontColor: '#333',
        bodyFontColor: '#666',
        bodySpacing: 4,
        xPadding: 12,
        mode: "nearest",
        intersect: 0,
        position: "nearest"
      },
      responsive: true,
      scales: {
        yAxes: [{
          barPercentage: 1.6,
          gridLines: {
            drawBorder: false,
            color: 'rgba(29,140,248,0.0)',
            zeroLineColor: "transparent",
          },
          ticks: {
            suggestedMin: 60,
            suggestedMax: 125,
            padding: 20,
            fontColor: "#9a9a9a"
          }
        }],

        xAxes: [{
          barPercentage: 0.9,
          gridLines: {
            drawBorder: false,
            color: 'rgba(225,78,202,0.1)',
            zeroLineColor: "transparent",
          },
          ticks: {
            padding: 20,
            fontColor: "#9a9a9a"
          }
        }]
      }
    };
    let data_new = {
      labels: ['09/24', '09/25', '09/26', '09/27', '09/28', '09/29', '09/30'],
      datasets: [{
        label: "Positive",
        fill: true,
        backgroundColor: gradientStroke,
        hoverBackgroundColor: gradientStroke,
        borderColor: '#00FF00',
        borderWidth: 1,
        borderDash: [],
        borderDashOffset: 0.0,
        data: data['bar_chart_positive'],
      },
      {
        label: "Negative",
        fill: true,
        backgroundColor: gradientStroke,
        hoverBackgroundColor: gradientStroke,
        borderColor: '#FF0000',
        borderWidth: 1,
        borderDash: [],
        borderDashOffset: 0.0,
        data: data['bar_chart_negative'],
      }]
    };

    // if chart already exists, destroy it first
    if(window.myMoodBarChart instanceof Chart)
    {
        window.myMoodBarChart.destroy();
    }

    window.myMoodBarChart = new Chart(barchart_ctx, {
      type: 'bar',
      responsive: true,
      legend: {
        display: true
      },
      data: data_new,
      options: gradientChartOptionsConfigurationWithTooltipPurple
    });
  },

  // implement drawWordCloudGraph function
  drawWordCloudGraph: function(data){
    let wcCanvas = document.getElementById("WordCloud");
    let wcCtx = wcCanvas.getContext('2d');

    function drawMap(imgdata) {
        var img = new Image();
        img.onload = function() {
          var hRatio = wcCanvas.width  / img.width;
          var vRatio =  wcCanvas.height / img.height;
          var ratio  = Math.min ( hRatio, vRatio );
          var centerShift_x = ( wcCanvas.width - img.width*ratio ) / 2;
          var centerShift_y = ( wcCanvas.height - img.height*ratio ) / 2;
          wcCtx.clearRect(0,0,wcCanvas.width, wcCanvas.height);
          wcCtx.drawImage(img, 0, 0, img.width*1.2, img.height*1.2,
                      centerShift_x, centerShift_y, img.width*ratio, img.height*ratio);
        };
        img.src = imgdata;
    }
    wc = data['word_cloud']
    drawMap("data:image/png;base64," + wc);
  },

  // implement drawTimeline function
  drawTimeline: function(data){
    gradientBarChartConfiguration = {
      maintainAspectRatio: false,
      legend: {
        display: true,
        position: 'bottom',
      },
      tooltips: {
        backgroundColor: '#f5f5f5',
        titleFontColor: '#333',
        bodyFontColor: '#666',
        bodySpacing: 4,
        xPadding: 12,
        mode: "nearest",
        intersect: 0,
        position: "nearest"
      },
      responsive: true,
      scales: {
        yAxes: [{
          gridLines: {
            drawBorder: false,
            color: 'rgba(29,140,248,0.1)',
            zeroLineColor: "transparent",
          },
          ticks: {
            suggestedMin: -1,
            suggestedMax: 1,
            padding: 0.2,
            fontColor: "#9e9e9e"
          }
        }],

        xAxes: [{
          gridLines: {
            drawBorder: false,
            color: 'rgba(29,140,248,0.1)',
            zeroLineColor: "transparent",
          },
          ticks: {
            padding: 20,
            fontColor: "#9e9e9e"
          }
        }]
      }
    };

    // if chart already exists, destroy it first
    if(window.myTimeLineChart instanceof Chart)
    {
        window.myTimeLineChart.destroy();
    }

    var timeline_ctx = document.getElementById("Timeline").getContext("2d");
    var gradientStroke = timeline_ctx.createLinearGradient(0, 230, 0, 50);

    gradientStroke.addColorStop(1, 'rgba(29,140,248,0.05)');
    gradientStroke.addColorStop(0.4, 'rgba(29,140,248,0.0)');
    gradientStroke.addColorStop(0, 'rgba(29,140,248,0)'); //blue colors

    var d1 = data['time_line_trend']
    var d2 = data['time_line_avg_score']

    window.myTimeLineChart = new Chart(timeline_ctx, {
      type: 'bar',
      responsive: true,
      legend: {
        display: false
      },
      data: {
        labels: [ '09/22/2021', '09/23/2021', '09/24/2021', '09/27/2021','09/28/2021','09/29/2021','09/30/2021'],
        datasets: [{
          label:"Trend",
          fill: true,
          backgroundColor: gradientStroke,
          hoverBackgroundColor: gradientStroke,
          borderColor: '#1f8ef1',
          borderWidth: 2,
          borderDash: [],
          borderDashOffset: 0.0,
          data: d1,

        },
        {
        label:  "Flair Score",
        type: 'line',
        fill: true,
        backgroundColor: gradientStroke,
        borderColor: '#00d6b4',
        borderWidth: 2,
        borderDash: [],
        borderDashOffset: 0.0,
        pointBackgroundColor: '#00d6b4',
        pointBorderColor: 'rgba(255,255,255,0)',
        pointHoverBackgroundColor: '#00d6b4',
        pointBorderWidth: 20,
        pointHoverRadius: 4,
        pointHoverBorderWidth: 15,
        pointRadius: 4,
        data: d2,
      }]
      },
      options: gradientBarChartConfiguration
    });
  },

  // implement drawTweetDisplay function
  drawTweetDisplay: function(data){
    message = data['tweet_display']
    let table = document.getElementById("tweetMessage");

    // if table already exists, destroy it first
    if(window.tbody != null)
    {
        window.tbody.remove();
    }

    window.tbody = document.createElement('tbody');

    for (var i = 0; i < message[0].length; i++) {
      let tr = document.createElement('tr');
      for (var j = 0; j < 2; j++) {
          let td = document.createElement('td');
          let cellText = document.createTextNode(data['tweet_display'][j][i]);
          td.appendChild(cellText)
          tr.appendChild(td)
      }
      tbody.appendChild(tr);
    }
    table.appendChild(tbody);

  },

  // implement drawEmotionGraph function
  drawEmotionGraph: function(data){
    var ctx = document.getElementById("emotionDot").getContext('2d');
    var gradientStroke = ctx.createLinearGradient(0, 230, 0, 50);
    pairs = data['emotion_display']

    gradientStroke.addColorStop(1, 'rgba(72,72,176,0.1)');
    gradientStroke.addColorStop(0.4, 'rgba(72,72,176,0.0)');
    gradientStroke.addColorStop(0, 'rgba(119,52,169,0)'); //purple colors
    var config = {
      type: 'scatter',
      data: {
        datasets: [{
          label: "My First dataset",
          fill: true,
          backgroundColor: gradientStroke,
          borderColor: '#d346b1',
          borderWidth: 2,
          borderDash: [],
          borderDashOffset: 0.0,
          pointBackgroundColor: '#d346b1',
          pointBorderColor: 'rgba(255,255,255,0)',
          pointHoverBackgroundColor: '#d346b1',
          pointBorderWidth: 20,
          pointHoverRadius: 4,
          pointHoverBorderWidth: 15,
          pointRadius: 4,
          data: pairs
        }],
      },
      options: {
        responsive: true,
        legend: {
          display: false
        },
        scales: {
          xAxes: [
              {
                type: 'linear',
                ticks: {
                  max: 1.1,
                  min: -1.1,
                  stepSize: 0.1
                },
                scaleLabel:{
                  display: true,
                  labelString: 'Negative                                                          Positive',
                  fontColor: "#d346b1"
                }
              }
          ],
          yAxes: [
              {
                type: 'linear',
                ticks: {
                  max: 9,
                  min: 1,
                  stepSize: 1
                },
                scaleLabel:{
                  display: true,
                  labelString: 'Sedate                         Active',
                  fontColor: "#d346b1"
                }
              }
          ]
        },
      }
    };
    // if chart already exists, destroy it first
    if(window.myEmotionDotChart instanceof Chart)
    {
        window.myEmotionDotChart.destroy();
    }
    window.myEmotionDotChart = new Chart(ctx, config);
  }
};