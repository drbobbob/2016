	"use strict";

	
	function getLenny(){
		var activated = $('[name=act_lenny]').prop('checked');
		return activated;
	}
		

	function fireBall() {
		var firing = $('[name=firer]:checked').prop('checked');
		return firing;
	}

	function aim() {
		var aiming = $('[name=aim_guy]:checked').prop('checked');
	}
	
var fireBall = false;
$('[name=firer]').on('click', function() {
	fireBall = !fireBall;
	NetworkTables.putValue(ntkeys.fireToggle, fireBall);
});

	
$('[name=ball_toggle]').on('click',function(){
	NetworkTables.putValue(ntkeys.lettyToggle, getLenny)
});

$('[name=aim_guy]').on('click',function(){
	NetworkTables.putValue(ntkeys.?, aim)
});
	
	function getBallsensor(){
		var guy = $('[name=ball_sensor]').prop('checked');
		return guy;
	}
	
	$('[name=ball_sensor]').on('click',function() {
		console.log(getBallsensor());
		if(getBallsensor() == true) {
			console.log('Ball in');
		}
		else {
			console.log('ball out');
		}
	});



	NetworkTables.addRobotConnectionListener(function(connected) {
		if(connected) {
			$('.robot-image').removeClass('offline');
			$('.robot-image').addClass('online');
		} else {
			$('.robot-image').addClass('offline');
			$('.robot-image').removeClass('online');
		}
	}, true);
		