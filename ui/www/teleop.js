	"use strict";

		

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
	NetworkTables.putValue(ntkeys.lettyToggle, getLenny);
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

// toggle switch
$('[name=toggle_left]').on('click', function {
	if($('[name="toggle"]').hasClass(toggled_in)) {
		$('[name="toggle"]').attr('class', toggle);
		$('[name="toggle"]').val(1);
	}
	else {
		$('[name="toggle"]').attr('class', toggled_in);
		$('[name="toggle"]').val(2);
	}
});
	
$('[name=toggle_right]').on('click', function {
	if($('[name="toggle"]').hasClass(toggled_out)) {
		$('[name="toggle"]').attr('class', toggle);
		$('[name="toggle"]').val(1);
	}
	else {
		$('[name="toggle"]').attr('class', toggled_out);
		$('[name="toggle"]').val(3);
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
		