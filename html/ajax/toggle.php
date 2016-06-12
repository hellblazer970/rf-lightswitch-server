<?php

// define the location of the codesend program
$PROG = '/home/pi/rfswitches/codesend ';

// get parameters of which switch and mode to use
$id = $_GET['id'];
$mode = $_GET['mode'];

// codes
$lights = Array();
$lights['1'] = Array( 'on' => 333107, 'off' => 333116 );
$lights['2'] = Array( 'on' => 333251, 'off' => 333260 );
$lights['3'] = Array( 'on' => 333571, 'off' => 333580 );
$lights['4'] = Array( 'on' => 335107, 'off' => 335116 );
$lights['5'] = Array( 'on' => 341251, 'off' => 341260 );

// form command
$code = $lights[$id][$mode];
if ( !$code ) {
	echo json_encode(array('status' => 0, 'message' => 'Error: invalid switch ID or mode.', 'log' => ''));
	die;
}
$cmd = $PROG . $lights[$id][$mode];

// execute command
$ll = exec($cmd.' 2>&1', $output, $return_var);
if ( $return_var != 0 ) {
	$status = 1;
} else {
	$status = 0;
}

// generate log console
$log = '$ '.$cmd.'<br>'.implode('<br>',$output);

// return status
echo json_encode(array('status' => $status, 'message' => 'Switch '.$id.' toggled '.$mode, 'log' => $cmd));
?>
