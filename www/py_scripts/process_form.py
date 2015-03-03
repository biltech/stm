#!/usr/bin/env python

from mod_python.util import FieldStorage
import paper_scraper
import cgi
import re

def get_info(req):

	error = None
	full_name = None
	word = None
	data = req.form

	if not (re.search( 'arxiv.org/abs/', data['full_name'])):
		error = " Enter a valid arXiv address "
		choice = int(data['layerss'])
		threshold = data['threshold']
	else:
		full_name = data['full_name']
		choice = int(data['layerss'])
		if not ( str( data['threshold']).isdigit() ):
			threshold = 1
		else:
			threshold = int(data['threshold'])

		# avoid script injection
		full_name = cgi.escape(full_name)

	if choice == 1:
		artName, nums, strr, enti = paper_scraper.auts1NL(full_name, threshold)
	elif choice == 2:
		artName, nums, strr, enti = paper_scraper.auts2NL(full_name, threshold)

	if not error:
		result = enti #nums
	else:
		result = error

	s = """
<html>
<head>
<title>StemSeeker</title>
<link rel="stylesheet" href="styles/main.css">
<link href="bootstrap/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
<div class="container">
<div class="col-xs-offset-3 col-xs-8"><h3> Key entities : </h3></div>
<div class="col-xs-offset-2">
<div id="well-box" class="well col-xs-offset-0 col-xs-8"> %s </div>
</div></div>
<br>
<!-- tree || http://jsfiddle.net/umutc1/eyf9q87c/ -->
	<div class="tree well">
	    <ul>
	        <li>
	            <span><i class="icon-folder-open"></i> %s </span> <a href=""></a>
	            <ul>
			        %s
			    </ul>
	        </li>
	    </ul>
	</div>
<br>
<script type="text/javascript" src="jQuery/jquery-2.1.1.min.js"></script>
<script src="bootstrap/js/bootstrap.min.js"></script>
<script src="main.js"></script>
<script> $(function(){ 
$('#tmpTxt').fadeOut(200);
	});  </script>	
</body>
</html>
"""

	if data.has_key( 'async' ):
		req.content_type = 'text/plain'
		s = result + s
	else:
		req.content_type = 'text/html'

	return s % (result, artName, strr)



