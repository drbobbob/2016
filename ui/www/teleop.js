"use strict";

function fireBall() {
	var firing = $('[name=firer]:checked').prop('checked');
	return firing ? true : false;
}

function aim() {
	var aiming = $('[name=aim_guy]:checked').prop('checked');
	return aiming ? true : false;
}

$('[name=firer]').on('click', function() {
	NetworkTables.putValue(ntkeys.fireToggle, fireBall());
});

$('[name=aim_guy]').on('click',function(){
	NetworkTables.putValue(ntkeys.autoAimToggle, aim());
});

/**
	Useful jquery extension:
	
	$.nt_toggle(key, function)
	
	- When a networktables variable changes, the function will be called with 
	  the value of the variable. 
	
*/
$.fn.extend({
	nt_toggle: function(k, fn) {
		
		fn = fn.bind(this);
		
		// only call the function when the key changes -- not when the user 
		// clicks it (this allows simultaneous pages to function correctly)
		NetworkTables.addKeyListener(k, function(k, v) {
			fn(v);
		}, true);
		
		return this.each(function() {
			$(this).on('click', function() {
				NetworkTables.setValue(k, NetworkTables.getValue(k) ? false : true);
			});
		});
	}
});



$('#ball_in').nt_toggle(ntkeys.ball_in, function(v){
	if (v) {
		NetworkTables.putValue(ntkeys.ball_out, false);
	}
	this.css('background-color', v ? 'green' : 'gray');

	if(v) {
		animate.load();
	}
});

$('#ball_out').nt_toggle(ntkeys.ball_out, function(v){
	if (v) {
		NetworkTables.putValue(ntkeys.ball_in, false);
	}
	this.css('background-color', v ? 'green' : 'gray');

	if(v) {
		animate.unload();
	}
});

NetworkTables.addKeyListener(ntkeys.shooting, function(k, v) {
	if(v) {
		animate.shoot();
	}
}, true);


$(document).ready(function(){
	
	//
	// Set up the cameras
	//
	
    loadCameraOnConnect({
        container: '#left_camera', // where to put the img tag
        proto: null,                    // optional, defaults to http://
        host: null,                     // optional, if null will use robot's autodetected IP address
        port: 5800,                     // webserver port
        image_url: '/?action=stream',   // mjpg stream of camera
        data_url: '/program.json',      // used to test if connection is up
        wait_img: null,                 // optional img to show when not connected, can use SVG instead
        error_img: null,                // optional img to show when error connecting, can use SVG instead
        attrs: {                        // optional: attributes set on svg or img element
            width: 400,                     // optional, stretches image to this width
            height: 300,                    // optional, stretches image to this width
        }
    });
	
    loadCameraOnConnect({
        container: '#right_camera', // where to put the img tag
        proto: null,                    // optional, defaults to http://
        host: null,                     // optional, if null will use robot's autodetected IP address
        port: 5801,                     // webserver port
        image_url: '/?action=stream',   // mjpg stream of camera
        data_url: '/program.json',      // used to test if connection is up
        wait_img: null,                 // optional img to show when not connected, can use SVG instead
        error_img: null,                // optional img to show when error connecting, can use SVG instead
        attrs: {                        // optional: attributes set on svg or img element
            width: 400,                     // optional, stretches image to this width
            height: 300,                    // optional, stretches image to this width
        }
    });
	
	// connection indicator for debugging
	attachRobotConnectionIndicator('#connected', 20);
	
	// ball indicator
	NetworkTables.addKeyListener(ntkeys.ballSensor, function(k, v) {
		$('#robot_ball').fadeTo(250, v ? 1 : 0);
	}, true);
	
});

// Animations for ball
var animate = (function() {
	var animateTimeoutId = null;
	var $robotBall = $('#robot_ball');
	var animations = [
		{ state : 'unload', time : 2 },
		{ state : 'load', time : 2 },
		{ state : 'load-shooter', time : 1 },
		{ state : 'shoot', time : .1 }
	];

	function getAnimationIndex(state) {
		return _.findIndex(animations, function(o) { return o.state == state });
	}

	function getAnimation() {
		return $('#robot_ball').attr('class') ? $('#robot_ball').attr('class') : 'load';
	}

	function reset() {
		$robotBall.css('transition', 'none');

		requestAnimationFrame(function() {
			$robotBall.attr('class', 'reset unload');

			requestAnimationFrame(function() {
				$robotBall.css('transition', 'opacity 2s');
				$robotBall.attr('class', 'unload');
			});
		});
	}

	function animate(state) {

		clearTimeout(animateTimeoutId);

		var curAnimationIndex = getAnimationIndex(getAnimation());
		var targetAnimationIndex = getAnimationIndex(state);
		var indexDiff = targetAnimationIndex - curAnimationIndex;
		
		if(indexDiff == 0) {
			if(animations[targetAnimationIndex].state == 'shoot') {
				reset();
			}
			return;
		}

		var nextAnimationIndex = curAnimationIndex + (indexDiff < 0 ? -1 : 1);
		var nextAnimation = animations[nextAnimationIndex];
		var transition = 'transform ' + nextAnimation.time + 's linear';
		$robotBall.css('transition', transition);
		$robotBall.attr('class', nextAnimation.state);

		animateTimeoutId = setTimeout(function() {
			animate(state);
		}, 1000 * nextAnimation.time);
	} 

	return {
		reset : reset,
		unload : function() { animate('unload'); },
		load : function() { animate('load'); },
		loadShooter : function() { animate('load-shooter'); },
		shoot : function() { animate('shoot'); }
	};

})();