//"use strict"; 


// Initialize autonomous slider
$('.autonomous-mode-carousel').slick({
  dots: false,
  arrows: false,
  infinite: true,
  speed: 500,
  //cssEase: 'linear',
  fade: true,
  slide: 'li',
  slidesToShow: 1,
  slidesToScroll : 1
});



function Steps($element, $carousel) {
	this.$element = $element;
	this.$steps = {};
	this.$carousel = $carousel;

	// initialize the steps and get the defaults
	var that = this;
	var defaults = {};
	var firstStep = null;
	$element.find('[data-step]').each(function() {
		var $step = $(this),
			step = $step.data('step'),
			defaultValue = $step.data('step-value');
		
		firstStep = firstStep || step;

		that.$steps[step] = $step;
		defaults[step] = defaultValue;	

		$step.text($step.text());
		$('<span class="value">' + defaultValue + '</span>').appendTo($step);

		// When step is clicked on, go to that step
		$step.on('click', function() {
			that.setStep(step);
		});
	});
 
	$element.trigger('stepInit', [defaults]);

	// set the current step
	this.setFirstStep();
};

Steps.prototype.setValue = function(step, value) {
	this.$steps[step].find('.value').text(value);
};

Steps.prototype.setSteps = function(steps) {
	_.forEach(this.$steps, function($step, step) {
		console.log(steps.indexOf(step) >= 0);
		if(steps.indexOf(step) >= 0) {
			$step.removeClass('disabled');
		} else {
			$step.addClass('disabled');
		}
	});

	this.setFirstStep();
};

Steps.prototype.setFirstStep = function() {
	var $step = this.$element.find('[data-step]:not(.disabled)').first();
	if($step.length > 0) {
		this.setStep($step.data('step'));
	}
};

Steps.prototype.setStep = function(step) {

	var $step = this.$steps[step];

	// set to active step in dom
	this.$element.find('[data-step]').removeClass('active');
	$step.addClass('active');

	// set the carousel slide
	var $slide = this.$carousel.find('[data-step=' + step + ']');
	this.$carousel.slick('slickGoTo', $slide.index());
};


function AutoChooser($element, steps) {
	this.$element = $element;
	this.steps = steps;
	this.modes = {};

	var that = this;

	// Create the mode
	this.$element.find('option').each(function(e) {
		that.modes[$(this).val()] = {
			$element : $(this),
			steps : $(this).data('steps')
		};
	});

	// set the current mode
	this._setMode($element.find('option:selected').val());

	// when select changes set the mode
	$element.on('change', function(e) {
		that._setMode($element.find('option:selected').val());
	});
}


AutoChooser.prototype._setMode = function(mode) {
	var mode = this.modes[mode];
	this.steps.setSteps(mode.steps);
};



var steps = new Steps($('.steps'), $('.autonomous-mode-carousel'));
var autoChooser = new AutoChooser($('.autonomous-chooser'), steps);






function getObsticle() {
	var obsticle = $('[name=obsticle_types]:checked').val();
	return obsticle
}

function getStaging() {
	var staging = $('.field_diagram_button.selected').attr('value');
	return staging;
}

function getGoal() {
	var goal = $('[name=shooting_target]:checked').val();
	return goal
}

function passingBall() {
	var passing_ball = $('[name=pass_ball]:checked').prop('checked');
	return passing_ball;
}


$('[name=obsticle_types]').on('click', function() {
	console.log(getObsticle()) 
	console.log('obsticle type changed'); 
	NetworkTables.putValue(ntkeys.obsticleTypes, getObsticle());
	});

$('[name=shooting_target]').on('click', function() {
	console.log(getGoal()) 
	console.log('shooting goal changed'); 
	NetworkTables.putValue(ntkeys.shootingTarget, getGoal());
});

$('[name=pass_ball]').on('click', function() {
	var passing = passingBall();
	if (passing) {
		console.log('Passing ball');
	} else {
		console.log('Not passing ball')
	}

	// Set value in in steps
	steps.setValue('passBall', passing ? 'yes' : 'no');

	// Set value in Networktables
	NetworkTables.putValue(ntkeys.passBall, passingBall());
});


// Staging Position Diagram
$('.field_diagram_button').on('click', function() {

	var value = $(this).attr('value');
	var position = $(this).attr('value');

	// select the staging position
	$('.field_diagram_button').attr('class', 'field_diagram_button');
	$(this).attr('class', 'field_diagram_button selected');
	
	// show the field trail	for the selected staging position
	$('.field_trail').attr('class', 'field_trail');
	$('.field_trail[value=' + value + ']').attr('class', 'field_trail selected');

	// Set the value in steps
	steps.setValue('stagingPosition', value);

	// Set staging position in NetworkTables
	NetworkTables.putValue(ntkeys.stagingPosition, position);

}); 

//  Set the goal in the diagram when staging position or goal values change
$('[name=shooting_target], .field_diagram_button').on('click', function() {
	var stagingPosition = getStaging();
	var goal = getGoal();

	var classes = [];
	classes.push(goal);

	if(stagingPosition < 3) {
		classes.push('left');
	} else if(stagingPosition == 3||4) {
		classes.push('mid');
	} else {
		classes.push('right');
	}

	$('[name=shooting_diagram]').attr('class', classes.join(' '));
});

$('[name=shooting_target], .field_diagram_button[value=1]').click();

// Set the value of the shooting goal step when selected
steps.setValue('shootingGoal', $('[name=shooting_target]:checked').val());
$('[name=shooting_target]').on('click', function(e) {
	var value = $(this).val();
	steps.setValue('shootingGoal', value);
});

//Obsticle pictures
$('[name=obsticle]').attr('class', getObsticle());
$('[name=obsticle_types]').on('change', function () {
	var obsticle = $(this).val();
	var obsticleTitle = $(this).find('option:selected').text();
	$('[name=obsticle]').attr('class', obsticle);
	steps.setValue('obsticleType', obsticleTitle);
});

$('[name=staging_position]').on('click', function () {
	if (getStaging()==1)
		$('[name=obsticle]').attr('class','low_bar')	
});

$('[name=staging_position]').on('click', function () {
	if (getStaging()==1)
		$('[name=obsticle_types][value=1]').prop('selected', true);
});






	
