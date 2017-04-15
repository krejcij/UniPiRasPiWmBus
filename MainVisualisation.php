<?php
class MyDB extends SQLite3
{
    function __construct()
    {
        $this->open('MainDatabase.db');
    }
}

        
        if (!isset($_POST["device"]))
        {
            $device = "B05C10000000021B";
        }
        else
        {
            $device = $_POST["device"];
        }
        
        $db = new MyDB();
        $result = $db->query("SELECT * FROM `MEASURES` WHERE `DEVICE` LIKE '%".$device."%' ORDER BY `DATETIME` DESC LIMIT 0, 500;");
?>

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
    <meta http-equiv="content-type" content="text/html; charset=utf-8">
    <title>UniPiRaspiWmBus - visualisation</title>
    <style>
 
    @import url('//fonts.googleapis.com/css?family=Open+Sans');
html {
	font-family:'Open Sans', sans-serif;
    	line-height:2em;
}

    body {
  margin: 0;
  padding: 0;
  background: #ccc;
}

/* Add a black background color to the top navigation */
.obalnav {
    background-color: #333;
    overflow: hidden;
    margin-bottom:20px;
}

.topnav {
    width:650px;margin: 0 auto;
    background-color: #333;
    overflow: hidden;
}

/* Style the links inside the navigation bar */
.topnav a {
    float: left;
    display: block;
    color: #f2f2f2;
    text-align: center;
    padding: 1px 30px;
    text-decoration: none;
    font-size: 14px;
}

/* Change the color of links on hover */
.topnav a:hover {
    background-color: #ddd;
    border-radius: 12px 12px 0px 0px;
    color: #333;
}

/* Add a color to the active/current link */
.topnav a.active {
    background-color: #ccc;
    color: black;
    border-radius: 12px 12px 0px 0px;
}


    </style>
    <!--Load the AJAX API-->
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script type="text/javascript" src="//ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
    <script type="text/javascript">
    
    // Load the Visualization API and the piechart package.
    google.charts.load('current', {'packages':['corechart']});
      
    // Set a callback to run when the Google Visualization API is loaded.
    google.charts.setOnLoadCallback(drawChart);
      
    function drawChart() {
          var data = google.visualization.arrayToDataTable(
        [
                ['-', 'Teplota [°C]', 'Vlhkost [%RV]'],
                <?php
                        echo "\n";
                        while($row = $result->fetchArray(SQLITE3_ASSOC) )
                        {
                            $datetime=$row['DATETIME'];
                            $value1=$row['VALUE1'];
                            $value2=$row['VALUE2'];
                            //$rssi=$row['RSSI'];

                            echo "\t\t\t\t ['".$datetime."',".$value1.",".$value2."],\n";
                        }
                ?>
        ]);
          
                  var options = {
            width: 1200, 
            height: 500,
          title: 'Kompletni zachyceni zarizeni <?php echo $device; ?>',
          titleTextStyle: { fontSize: 20, bold: true } ,
          enableInteractivity: true,
          //colors: ['#FF0000', '#0000FF'],
          //curveType: 'function',
          backgroundColor: {stroke:'#000000',strokeWidth:1},
          chartArea: {left:75,top:45,bottom:75,right:150},
          crosshair: { focused: { color: '#3bc', opacity: 5.8 } },
          legend: { position: 'right',textStyle:{ fontSize: 12, bold: true } },
          hAxis: {title: 'Čas měření', format: 'yyyy-mm-dd HH:MM', textStyle:{ fontSize: 12, bold: true },titleTextStyle:{ fontSize: 14, bold: true, italic: false}},
          vAxes: {
            0:{title: 'Teplota', format:'#,## °C', textStyle:{ fontSize: 12, bold: true },titleTextStyle:{ fontSize: 14, bold: true, italic: false },gridlines:{color: 'gray'}},
            1:{title: 'Vlhkost', format:'#,##%', textStyle:{ fontSize: 12, bold: true },titleTextStyle:{ fontSize: 14, bold: true, italic: false },gridlines:{color: 'gray'}}
          },
          pointSize: 3,
          series: {0: {pointShape: 'circle',targetAxisIndex:0 }, 1: { pointShape: 'circle',targetAxisIndex:1 }, 2: {pointShape: 'circle',targetAxisIndex:0 }}          
        };
          
      // Create our data table out of JSON data loaded from server.
      //var data = new google.visualization.DataTable(jsonData);

      // Instantiate and draw our chart, passing in some options.
      var chart = new google.visualization.AreaChart(document.getElementById('chart_div'));
      chart.draw(data, options);
    }

    </script>
  </head>
<body>
<div class="obalnav">
    <div class="topnav" id="myTopnav">
      <a href="/" class="active">Graphs explorer</a>
      <a href="/db/">Database explorer</a>
      <a href="/logs/">Logs explorer</a>
    </div>
</div>
<center>
<h1>UniPiRaspiWmBus visualisation</h1>
<form action="/index.php" method="post">
<?php

$db = new MyDB();
$result = $db->query("SELECT * FROM 'DEVICES'");
echo '<b> Vyber zarizeni k vizualizaci:</b> <select name="device">';  
while($row = $result->fetchArray(SQLITE3_ASSOC) ){
    if ($row['DEVICE_ADDRESS']==$device)
    {
        echo '<option selected="selected" value="'.$row['DEVICE_ADDRESS'].'">'.$row['DEVICE_ADDRESS'].' - '.$row['DEVICE_INFO'].'</option>';
        $caption = $row['DEVICE_INFO'];
        $sensor = $row['DEVICE_ADDRESS'];
    }
    else
    {
        echo '<option value="'.$row['DEVICE_ADDRESS'].'">'.$row['DEVICE_ADDRESS'].' - '.$row['DEVICE_INFO'].'</option>';
    }
        
   }
   echo '</select>&nbsp;&nbsp;';
?>
<input type="submit" name=">>" value=">>">
</form>
<h2><?php echo $caption;?></h2>
    <!--Div that will hold the pie chart-->
    <div id="chart_div"></div>
</center>
</body>
</html>