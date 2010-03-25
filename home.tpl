<!doctype: xhtml>
<html>
	<head>
		<title>Vancouver News {{title}}</title>
		<link rel="stylesheet" href="/static/screen.css" type="text/css" media="screen, projection">
		<link rel="stylesheet" href="/static/print.css" type="text/css" media="print">	
		<!--[if lt IE 8]><link rel="stylesheet" href="/static/ie.css" type="text/css" media="screen, projection"><![endif]-->
		<script type="text/javascript" src="/static/jquery.js"></script>
		<script type="text/javascript">
			$(document).ready(function(){
			    // the main jQuery code
			tester = $.get("/ajax/2");
			    $("div.response").append(tester);
			});
		</script>
	</head>
	<body>
		<div class="container showgrid">
			<div class="span-24 last">
				<h1>Student Info: <b>N</b>ews <b>R</b>easoning <b>A</b>gent</h1>
			</div>
			%for subject in subjects:
			<div class="span-3">
				<h2>{{subject}}</h2>
			</div>
			%end
			<div class='response'>The response should be here: </div>
		</div>
	</body>
</html>
