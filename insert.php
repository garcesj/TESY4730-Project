


<?php
	$dbhost = "destinations.coajuzoc6wxq.us-west-2.rds.amazonaws.com";
	$dbuser = "dbuser";
	$dbpass = "dbpassword";

$con = mysql_connect($dbhost,$dbuser,$dbpass);

if (!$con)

  {
  die('Could not connect: ' . mysql_error());
  }


mysql_select_db("destination", $con);

 

$sql="INSERT INTO destination (firstname_author, lastname_author, location_name_city, location_country, date_trip, descr) VALUES ('$_POST[firstname]','$_POST[lastname]','$_POST[cityy]','$_POST[countryy]','$_POST[datee]','$_POST[descriptionn]')";

 

if (!mysql_query($sql,$con))

  {

  die('Error: ' . mysql_error());

  }

echo "1 record added";

mysql_close($con)
?>