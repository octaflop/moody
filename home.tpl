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
			<div class="span-12 append-12 last">
				<!-- map coming soon enough<div id="map_canvas" style="width: 500px; height: 300px"></div>-->
			</div>
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
		    <div class='span-24 last'><h2>Debug Console</h2>
		    <script type="text/javascript" src='/static/firebug-lite.js'></script>
		    </div>
                </div>
	</body>
<!--<script src="http://maps.google.com/maps?file=api&amp;v=2&amp;sensor=true&amp;key=ABQIAAAA_6YxpRQIVJjIx8daYGWgaRSoe-VhWat6qM5h3ZKg1qD5_SlhqhRRcZsNaAPttPkDvNO1UjWo8d7_9g" type="text/javascript"></script>-->
<script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=true"></script>
<script type="text/javascript" src="http://code.google.com/apis/gears/gears_init.js"></script>
<script type="text/javascript">

var initialLocation;
var siberia = new google.maps.LatLng(60, 105);
var newyork = new google.maps.LatLng(40.69847032728747, -73.9514422416687);
var browserSupportFlag =  new Boolean();
var map;
var infowindow = new google.maps.InfoWindow();
  
function initialize() {
  var myOptions = {
    zoom: 6,
    mapTypeId: google.maps.MapTypeId.ROADMAP
  };
  map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);
  
  // Try W3C Geolocation method (Preferred)
  if(navigator.geolocation) {
    browserSupportFlag = true;
    navigator.geolocation.getCurrentPosition(function(position) {
      initialLocation = new google.maps.LatLng(position.coords.latitude,position.coords.longitude);
      contentString = "Location found using W3C standard";
      map.setCenter(initialLocation);
      infowindow.setContent(contentString);
      infowindow.setPosition(initialLocation);
      infowindow.open(map);
    }, function() {
      handleNoGeolocation(browserSupportFlag);
    });
  } else if (google.gears) {
    // Try Google Gears Geolocation
    browserSupportFlag = true;
    var geo = google.gears.factory.create('beta.geolocation');
    geo.getCurrentPosition(function(position) {
      initialLocation = new google.maps.LatLng(position.latitude,position.longitude);
      contentString = "Location found using Google Gears";
      map.setCenter(initialLocation);
      infowindow.setContent(contentString);
      infowindow.setPosition(initialLocation);
      infowindow.open(map);
    }, function() {
      handleNoGeolocation(browserSupportFlag);
    });
  } else {
    // Browser doesn't support Geolocation
    browserSupportFlag = false;
    handleNoGeolocation(browserSupportFlag);
  }
}

function handleNoGeolocation(errorFlag) {
  if (errorFlag == true) {
    initialLocation = newyork;
    contentString = "Error: The Geolocation service failed.";
  } else {
    initialLocation = siberia;
    contentString = "Error: Your browser doesn't support geolocation. Are you in Siberia?";
  }
  map.setCenter(initialLocation);
  infowindow.setContent(contentString);
  infowindow.setPosition(initialLocation);
  infowindow.open(map);
}
</script>
<script type="text/javascript">
        $(document).ready(function(){
            // the main jQuery code
/*    function initialize(lat,lon) { 
     if (GBrowserIsCompatible()) { 
       var map = new GMap2(document.getElementById("map_canvas"));
       map.setCenter(new GLatLng(lat, lon), 13);
// Create our "tiny" marker icon
var blueIcon = new GIcon(G_DEFAULT_ICON);blueIcon.image = "http://www.google.com/intl/en_us/mapfiles/ms/micons/blue-dot.png";                // Set up our GMarkerOptions object
markerOptions = { icon:blueIcon };
var point = new GLatLng(lat, lon);
       map.addOverlay(new GMarker(point, markerOptions));
       map.setUIToDefault();
      }
    }*/
            function build_watch() { // the main location function. Refreshable
                navigator.geolocation.getCurrentPosition(function(position) {
                    $('#lat').val(position.coords.latitude);
                    $('#lon').val(position.coords.longitude);
                    var lat = position.coords.latitude;
                    var lon = position.coords.longitude;
		    //initialize(lat,lon);
             $.getJSON('/ajax/bus/ids/loc/' + lat + '/' + lon, function(json) {
                ii = 0;
                for (ii=0; ii != json.busids.length; ii++) {
                    $.getJSON('/ajax/bus/times/' + json.busids[ii], function(buses) {
                        var ii = 0;
                        var times = "";
			var businfo = "";
			businfo += "<div class='busstop'><h4>" + buses.idinfo[ii].stopName + "</h4><b>" + buses.idinfo[ii].stopID + "</b>"
                        for (ii=0; ii!=buses.idinfo.slice().length;ii++){
                            times += "<li>" + buses.idinfo[ii].times.slice() + "</li>";
                        }
                        $('#businfo').append(businfo +  "<ul>" + times + "</ul></div>");
                    });
                }
            });                   
	}); 
    }
            build_watch;
            $('#navreload').click(build_watch);
            
                var watcher = navigator.geolocation.watchPosition(function(position) {
                $('#lat').val(position.coords.latitude);
                $('#lon').val(position.coords.longitude);
             }
            );
            
            $('#throbtest').throbber("dblclick", {image: "/static/img/throbber.gif"});

            $('#response').throbber({image: "/static/img/throbber.gif"});
            $('#businfo').throbber({image: "/static/img/throbber.gif"});

	        });
</script>
</html>
