	"use strict";
	
	function getLenny(){
		var activated = $('[name=act_lenny]').prop('checked');
		return activated;
	}

	$('[name=act_lenny]').on('click', function() {
		console.log(getLenny());
		if (getLenny() == true) {
			console.log('Lenny Activated');	
		}
		else {
			console.log('Lenny Deactivated');
		NetworkTables.putValue(ntkeys.lenny, getLenny())
		}
	});
		


	$('[name=firer]').on('click', function() {	
	console.log('Fired')
	NetworkTables.putValue(ntkeys.fire', true)
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
	
	$('[name=ball_sensor]').on('click', function() {
		getBallsensor();
		if(getBallsensor()==true) {
			$('p').removeClass('ballout');
			$('p').addClass('ballin');
		}
		else {
			$('p').removeClass('ballin');
			$('p').addClass('ballout');
		NetworkTables.putValue(ntkeys.ballSensor, getBallsensor())
		}
	});
		