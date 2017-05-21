<?php
class MyDB extends SQLite3
{
    function __construct()
    {
        $this->open('MainDatabase.db');
    }
}

        
        if (@strlen($_REQUEST["device"])<1)
        {
            $device = "B05C10000000021B";
        }
        else
        {
            $device = $_REQUEST["device"];
        }
        
        if (@strlen($_REQUEST["refresh"])<1)
        {
            $refresh = "0";
        }
        else
        {
            $refresh = $_REQUEST["refresh"];
        }
        
        $db = new MyDB();
        if (@strlen($_REQUEST["day"])>1)
        {
            $squery = "SELECT * FROM `MEASURES` WHERE `DATETIME` LIKE '%".$_REQUEST["day"]."%' AND `DEVICE` LIKE '%".$device."%' ORDER BY `DATETIME` ASC LIMIT 0, 1440;";
            $_REQUEST["last"] = 1440;
        }
        elseif (@strlen($_REQUEST["last"])>1)
        {
            $squery = "SELECT * FROM `MEASURES` WHERE `DEVICE` LIKE '%".$device."%' ORDER BY `DATETIME` DESC LIMIT 0, ".$_REQUEST["last"].";";
        }
        else
        {
            $_REQUEST["last"] = 10;     
            $squery = "SELECT * FROM `MEASURES` WHERE `DEVICE` LIKE '%".$device."%' ORDER BY `DATETIME` DESC LIMIT 0, 10;";
        }
            
        //echo $squery;
        $result = $db->query($squery);
        
        switch ($device)
        {
            // ZPA elektroměr
            case "016A449367120102":
            case "016A474275010102":
                $d_value1 = "Night tarif [kWh]";
                $d_value2 = "Day tarif [kWh]";
                $d_measure1 = "##,## kWh";
                $d_measure2 = "##,## kWh";
                break;
            // Bonega vodoměry
            case "EE09210100000106":
                $d_value1 = "Cold water [m3]";
                $d_measure1 = "##,### m3";
            case "EE09210100000107":
                $d_value1 = "Hot water [m3]";
                $d_measure1 = "##,### m3";
                break;
            // Weptech senzor + ostatní defaultně
            default:
                $d_value1 = "Temperature [°C]";
                $d_value2 = "Humidity [% RH]";
                $d_measure1 = "#,## °C";
                $d_measure2 = "##,## %RH";
         }   
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
  background: #ffffff;
}

option
{
    background: #fff;
    border: 1px solid #333;
    color: #333;
}

select
{
    background: #fff;
    border: 1px solid #333;
    color: #333;
}


input
{
    background: #fff;
    border: 1px solid #333;
    color: #333;
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
    background-color: #fff;
    color: black;
    border-radius: 12px 12px 0px 0px;
}

#send
{
    margin-top:15px;
    padding-left: 25px;
    padding-right: 25px;
    cursor: pointer;
    
}

#chart_div
{
cursor:crosshair;
}


#footer
{
    width:100%;
    color: #DEDEDE;
    font-size:10px;
    text-align:left;
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
                <?php
                        if ($device=="EE09210100000106" or $device=="EE09210100000107")
                        {
                            echo "['-', '".$d_value1."'],";
                        }
                        else
                        {
                           echo "['-', '".$d_value1."','".$d_value2."'],";                               
                        }
                        
                        echo "\n";
                        $inc=0;
                        while($row = $result->fetchArray(SQLITE3_ASSOC) )
                        {
                            $datetime=substr($row['DATETIME'],11,5)." (".ltrim(substr($row['DATETIME'],8,2),"0").".".ltrim(substr($row['DATETIME'],5,2),"0").".)";
                            
                            //Schema Bonega
                            if ($row['DEVICE']=="EE09210100000106" or $row['DEVICE']=="EE09210100000107")
                            {
                                $value1=$row['VALUE1'];
                                $value2='0';
                            }
                            else
                            {
                                $value1=$row['VALUE1'];
                                $value2=$row['VALUE2'];                                 
                            }
                            
                            $inc++;
                            //$value2=0;
                            //$rssi=$row['RSSI'];

                            if ($device=="EE09210100000106" or $device=="EE09210100000107")
                            {
                                echo "\t\t\t\t ['".$datetime."',".$value1."],\n";
                            }
                            else
                            {
                               echo "\t\t\t\t ['".$datetime."',".$value1.",".$value2."],\n";                             
                            }
                             
                        }                        
                ?>
        ]);
          
                  var options = {
            width: 1900, 
            height: 800,
            titleTextStyle: { fontSize: 20, bold: true } ,
            enableInteractivity: true,
            chartArea: {left:85,top:55,bottom:85,right:85},
            crosshair: { focused: { color: '#3bc', opacity: 5.8 } },
            legend: { position: 'top',textStyle:{ fontSize: 12, bold: true } },
            hAxis: {title: 'Measure time', format: 'mm-dd HH:MM', textStyle:{ fontSize: 12, bold: true },titleTextStyle:{ fontSize: 14, bold: true, italic: false}},
            <?php
                if ($device=="EE09210100000106" or $device=="EE09210100000107")
                {
                    echo "vAxis: {title: '<?php echo $d_value1; ?>', format:'<?php echo $d_measure1; ?>', textStyle:{ fontSize: 12, bold: true },titleTextStyle:{ fontSize: 14, bold: true, italic: false },gridlines:{color: 'gray'}},\n";
                }
                else
                {
                    echo "vAxes: {"."\n";
                        echo "0:{title: '".$d_value1."', format:'".$d_measure1."', textStyle:{ fontSize: 12, bold: true },titleTextStyle:{ fontSize: 14, bold: true, italic: false },gridlines:{color: 'gray'}},"."\n";
                        echo "1:{title: '".$d_value2."', format:'".$d_measure2."', textStyle:{ fontSize: 12, bold: true },titleTextStyle:{ fontSize: 14, bold: true, italic: false },gridlines:{color: 'gray'}},"."\n";
                    echo "},"."\n";                             
                }
            ?>
            pointSize: 3,
            series: {0: {pointShape: 'circle',targetAxisIndex:0 }, 1: { pointShape: 'circle',targetAxisIndex:1 }, 2: {pointShape: 'circle',targetAxisIndex:0 }}          
        };
          
      // Create our data table out of JSON data loaded from server.
      //var data = new google.visualization.DataTable(jsonData);

      // Instantiate and draw our chart, passing in some options.
      var chart = new google.visualization.AreaChart(document.getElementById('chart_div'));
        <?php
            if ($inc>2) echo "chart.draw(data, options);";
        ?>
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
<h2>UniPiRaspiWmBus - visualisation</h2>
<form action="/" method="post">
<?php
    $db = new MyDB();
    
    // Hledani podle senzoru
        $result = $db->query("SELECT * FROM `DEVICES` WHERE `DEVICE_GRAPH` LIKE '%1%';");
        echo 'Select device to visualise: <select name="device">';  
        while($row = $result->fetchArray(SQLITE3_ASSOC) )
        {
            var_dump($row['DEVICE_ADDRESS']);
            var_dump($device);
            if ($row['DEVICE_ADDRESS']==$device)
            {
                echo '<option selected="selected" value="'.$row['DEVICE_ADDRESS'].'">'.$row['DEVICE_ADDRESS'].' - '.$row['DEVICE_DESCR'].'</option>';
            }
            else
            {
                echo '<option value="'.$row['DEVICE_ADDRESS'].'">'.$row['DEVICE_ADDRESS'].' - '.$row['DEVICE_DESCR'].'</option>';
            }
        }
        echo '</select>';
       
    // Hledani podle data dne
        $result = $db->query("SELECT * FROM `MEASURES` group by substr(`DATETIME`, 1, 10) ORDER BY `DATETIME` DESC");
        echo '<br />Select date <select name="day">';
            echo '<option value="">-</option>';  
        while($row = $result->fetchArray(SQLITE3_ASSOC) )
        {
            $den = substr($row['DATETIME'],0,10);
            $denfancy = ltrim(substr($row['DATETIME'],8,2),"0").".".ltrim(substr($row['DATETIME'],5,2),"0").".".substr($row['DATETIME'],0,4);
            if ($den==$_REQUEST['day'])
            {
                echo '<option selected="selected" value="'.$den.'">'.$denfancy.'</option>';
            }
            else
            {
                echo '<option value="'.$den.'">'.$denfancy.'</option>';
            }
        }
        echo '</select>';
        
        
    // Hledani posledniho useku hodnot
        $reslast = array ('10080','8640','7200','5760','4320','2880','1440','1080','720','540','360','180','90','45','10');
        echo ' or show last <select name="last">';
        echo '<option value="">-</option>';  
        foreach($reslast as $row)
        {
            $pocet = $row;
            if ($pocet==$_REQUEST['last'])
            {
                echo '<option selected="selected" value="'.$pocet.'">'.ecount($pocet).'</option>';
            }
            else
            {
                echo '<option value="'.$pocet.'">'.ecount($pocet).'</option>';
            }
        }
        echo '</select> values. ';
        
        function ecount($p)
        {
            $day = $p/60;
            $min = $day/24;
            if ($day>0) $ret = $day."h";
            if ($day>23) $ret = $min."d";
            if ($day<2) $ret = $p."m";
            return $p."  (cca ".$ret.")";
        }
        
        
    // Refreshovani grafu v zadanem intervalu
        $refrlast = array ('3600','2700','1800','900','600','300','180','60','45','30','15');
        echo 'Refresh every <select name="refresh">';
        echo '<option value="">-</option>';  
        foreach($refrlast as $row)
        {
            $tajm = $row;
            if ($tajm==$refresh)
            {
                echo '<option selected="selected" value="'.$tajm.'">'.etime($tajm).'</option>';
            }
            else
            {
                echo '<option value="'.$tajm.'">'.etime($tajm).'</option>';
            }
        }
        echo '</select>. ';
        
        function etime($t)
        {
            $min = $t/60;
            $sec = $t%60;
            if ($min>=1) $ret = $min."m ";
            if ($sec>0) $ret .= $sec."s";
            return $ret;
        }
        
?>
<br />
<input type="submit" id="send" name=">>" value="Generate chart visualisation with selected data">    
</form>

    <!--Div that will hold the pie chart-->
    <div id="chart_div">
        <?php
            if ($inc!=0)
            {
                echo "<i style='position:relative;top:400px;'>... generating chart ...</i>";
            }
            else
            {
                echo "<b style='position:relative;top:400px;'>Data with this filter does not exists, generation aborted !</b>";
            }
        ?>
    
    </div>
    <div id="footer">Version 2017-05-21. Url: <?php echo "/MainVisualisation.php?day=".$_REQUEST["day"]."&device=".$device."&last=".$_REQUEST["last"]."&refresh=".$refresh.""; ?></div>
</center>
<?php
            if ($refresh!=0)
            {
                echo '<script type="text/javascript">';
                    echo 'setTimeout(function () { location.reload(true); }, '.($refresh*1000).');';
                echo '</script>';
            }
        ?>
</body>
</html>