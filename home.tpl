<!doctype: xhtml>
<html>
	<head>
		<title>Vancouver News {{title}}</title>
		<link rel="stylesheet" href="/static/screen.css" type="text/css" media="screen, projection">
		<link rel="stylesheet" href="/static/custom.css" type="text/css" media="screen, projection">
		<link rel="stylesheet" href="/static/print.css" type="text/css" media="print">	
		<!--[if lt IE 8]><link rel="stylesheet" href="/static/ie.css" type="text/css" media="screen, projection"><![endif]-->
		<script type="text/javascript" src="/static/jquery.js"></script>
		<script type="text/javascript" src="/static/jquery.throbber.js"></script>
		<script type="text/javascript" src="/static/dojo.js"></script>
		<script type="text/javascript" src="/static/jsonpath.js"></script>
	</head>
	<body>
		<div class="container showgrid">
			<div class="span-24 last">
				<h1>Student Info: <b>N</b>ews <b>R</b>easoning <b>A</b>gent</h1>
			</div>
            <hr />
            <div class="span-3">Latitude: <input value="" id="lat"></input></div>
            <div class="prepend-1 span-3">Longitude: <input value="" id="lon"></input></div>
            <div class="prepend-2 span-3 append-12 last"><button id="navreload">Refresh</button></div>
            <hr />
                    <div class="span-24 last">
                        <div class="span-7 colborder">
                            <h3>Bus Info</h3>
                            <p id='businfo'></p>
                            <form action="/ajax/bus/loc" method="get">
                              <input type="text" name="lat" />
                              <input type="text" name="lon" />
                              <input type="submit" />
                            </form>
                        </div>
                        <div class="span-6 colborder">
                            <h3>Weather</h3>
                            <div id="times">
                            </div>
                            <div class='response'><span id="response">?</span> </div>
                            </div>
                        <div class="span-7 last">
                        <h3>Garbage Pickup</h3>
			%for subject in subjects:
                                <h4>{{subject}}</h4>
			%end
                                <h4 id="throbtest">ThrobTest</h4>
                        </div>
                    </div>
                </div>
	</body>
<script type="text/javascript">
        $(document).ready(function(){
            // the main jQuery code
            function build_watch() { // the main location function. Refreshable
                navigator.geolocation.getCurrentPosition(function(position) {
                    $('#lat').val(position.coords.latitude);
                    $('#lon').val(position.coords.longitude);
                    
                    // $('#businfo').load('/ajax/bus/loc/' + String(position.coords.latitude)+ ',' + String(position.coords.longitude));
                    $('#businfo').load('/ajax/bus/loc/' + String(position.coords.latitude) + '/' + String(position.coords.longitude));
                }); 
            }
            build_watch;
            $('#navreload').click(build_watch);
            
            /*$.getJSON('/ajax/bus/loc/49.229195/-122.947248', function(json) {
              $('#response').html('grabbed: ' + json.bustimes[0][0].stopName);
              var out = "";
              out += jsonPath(json, "$..*",{resultType:"PATH"}).toJSONString();
              $('#response').html('this is what I got: <br />' + out);
            });*/
            
            /*
            $.getJSON('/ajax/bus/loc/49.229195/-122.997248', function(json) {
                var busset = "<h3>Closest " + json.bustimes.length + " Stops</h3>";
                var ii=0;
                for (ii=0; ii<=(json.bustimes.length-1); ii++) {
                    busset += "<p><b>" + (ii+1) + "</b>: " + json.bustimes[ii][0].stopName + "</p>";
                }
                $('#response').html(busset);
            });
            */
            var watcher = navigator.geolocation.watchPosition(function(position) {
                $('#lat').val(position.coords.latitude);
                $('#lon').val(position.coords.longitude);
             }
            );
            
            $('#throbtest').throbber("dblclick", {image: "/static/img/throbber.gif"});

            $('#response').throbber({image: "/static/img/throbber.gif"});
            $('#businfo').throbber({image: "/static/img/throbber.gif"});
            $.getJSON('/ajax/bus/ids/loc/49.2814856/-122.9573012', function(json) {
                ii = 0;
                for (ii=0; ii != json.busids.length; ii++) {
                    $.getJSON('/ajax/bus/times/' + json.busids[ii], function(buses) {
                        var ii = 0;
                        var wellthen = "";
                        for (ii=0; ii!=buses.idinfo.slice().length;ii++){
                            wellthen += buses.idinfo[ii].times.slice();
                        }
                        $('#response').append("<ul>"+wellthen+"</ul>");
                    });
                }
            });
            
            /*$.getJSON('/ajax/bus/loc/49.2814856/-122.9573012', function(json) {
                //$('#response').html(json.bustimes.length);
                var ii=0;
                for (ii=0; ii<=(json.bustimes.length-1); ii++) { // step through the stops
                    var jj=0;
                    var stopid = json.bustimes[ii][0].stopID;
                    var stopname = json.bustimes[ii][0].stopName;
                    var times = "";
                    var jj = 0
                    for (jj=0; jj<=(json.bustimes[ii].slice().length-1); jj++) {
                        var kk = 0;
                        //for (kk=0; kk<=(json.bustimes[ii][jj].times.length-1); kk++) {
                           times += "<li>" + json.bustimes[ii][jj].times.slice(0,4) + "</li>";
                        //}
                    }
            
                    $('#response').append("<b>" + stopid + "</b><br />" + "<p>" + stopname + "</p><ul class='times'>" + times + "</ul>");
                }
            });*/

            //$('#response').load('/ajax/888')
            //$('#businfo').load('/ajax/bus/close_stops')

            });
</script>
</html>
