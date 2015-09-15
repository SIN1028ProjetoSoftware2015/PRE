var Script = function () {


    var doughnutData = [
        {
            value: 30,
            color:"#F7464A",
            label: "Red"
        },
        {
            value : 50,
            color : "#46BFBD",
            label: "AAA"
        },
        {
            value : 100,
            color : "#FDB45C",
            label: "BBB"
        },
        {
            value : 40,
            color : "#949FB1",
            label: "RCCCed"
        },
        {
            value : 120,
            color : "#4D5360",
            label: "DDD"
        }

    ];


    var opcoes = {
        //Boolean - Whether we should show a stroke on each segment
        segmentShowStroke : true,

        //String - The colour of each segment stroke
        segmentStrokeColor : "#fff",

        //Number - The width of each segment stroke
        segmentStrokeWidth : 2,

        //Number - The percentage of the chart that we cut out of the middle
        percentageInnerCutout : 50, // This is 0 for Pie charts

        //Number - Amount of animation steps
        animationSteps : 100,

        //String - Animation easing effect
        animationEasing : "easeOutBounce",

        //Boolean - Whether we animate the rotation of the Doughnut
        animateRotate : true,

        //Boolean - Whether we animate scaling the Doughnut from the centre
        animateScale : false,

        //String - A legend template
        legendTemplate : "<ul class=\"<%=name.toLowerCase()%>-legend\"><% for (var i=0; i<segments.length; i++){%><li><span style=\"background-color:<%=segments[i].fillColor%>\"></span><%if(segments[i].label){%><%=segments[i].label%><%}%></li><%}%></ul>"

    }

    var pie_ctx = document.getElementById("doughnut").getContext("2d");
    myPie = new Chart(pie_ctx).Pie(doughnutData, {
        legendTemplate : "<ul class=\"<%=name.toLowerCase()%>-legend\"><% for (var i=0; i<segments.length; i++){%><li><span style=\"background-color:<%=segments[i].fillColor%>\"></span><%if(segments[i].label){%><%=segments[i].label%><%}%></li><%}%></ul>"
    });

    //var myPie = new Chart(document.getElementById("doughnut").getContext("2d")).Doughnut(doughnutData, opcoes);
    var legend = myPie.generateLegend();
    $("#legend").html(legend);

}();