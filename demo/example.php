<?php
$query  = "SELECT * FROM products WHERE id LIKE $_GET['product']";
$result = mssql_query($query);
?>