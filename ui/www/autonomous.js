//"use strict"; 

function getObsticle() {
	var obsticle = $('[name=obsticle_types]:checked').val();
	return obsticle
}

function getStaging() {
	var staging = $('[name=staging_position]:checked').val();
	return staging
}

function getGoal() {
	var goal = $('[name=shooting_target]:checked').val();
	return goal
}

function passingBall() {
	var passing_ball = $('[name=pass_ball]:checked').prop('checked');
	return passing_ball
}

$('[name=staging_position]').on('click', function() {
	console.log(getStaging()) 
	console.log('staging position changed'); 
	NetworkTables.putValue('/SmartDashboard/stagingposition', getStaging());
	});

$('[name=obsticle_types]').on('click', function() {
	console.log(getObsticle()) 
	console.log('obsticle type changed'); 
	NetworkTables.putValue('/SmartDashboard/obsticletypes', getObsticle());
	});

$('[name=shooting_target]').on('click', function() {
	console.log(getGoal()) 
	console.log('shooting goal changed'); 
	NetworkTables.putValue('/SmartDashboard/shootingtarget', getGoal())
});

$('[name=pass_ball]').on('click', function() {
	if (passingBall()== true) {
		console.log('Passing ball');
	}
	else {
		console.log('Not passing ball')
	}
	NetworkTables.putValue('/SmartDashboard/passball', passingBall())
});


// Staging Position Diagram



$('[name=staging_position]').on('click', function() {
	getStaging();
	if (getStaging()==1) {
		$('[name=staging_diagram]').attr('class', ' field_position_diagram left')
	} 
});

$('[name=staging_position]').on('click', function() {
	getStaging()
	if (getStaging()==2) {
		$('[name=staging_diagram]').attr('class', 'field_position_diagram mid')
	}
});

$('[name=staging_position]').on('click', function() {
	getStaging()
	if (getStaging()==3) {
		$('[name=staging_diagram]').attr('class', 'field_position_diagram right')
	}
});


$('[name=shooting_target]').on('click', function() {
	getStaging();
	if (getStaging()==1) {
		$('[name=staging_diagram]').attr('class', ' field_position_diagram left')
	}
});

$('[name=shooting_target]').on('click', function() {
	getStaging()
	if (getStaging()==2) {
		$('[name=staging_diagram]').attr('class', 'field_position_diagram mid')
	}
});

$('[name=shooting_target]').on('click', function() {
	getStaging()
	if (getStaging()==3) {
		$('[name=staging_diagram]').attr('class', 'field_position_diagram right')
	}
});



$('[name=shooting_target]').on('click', function() {
	getStaging()
	getGoal()
	if (getStaging()==1 && getGoal()==3) {
		$('[name=staging_diagram]').attr('class', 'straight_left')
	}
});

$('[name=shooting_target]').on('click', function() {
	getStaging()
	getGoal()
	if (getStaging()==2 && getGoal()==3) {
		$('[name=staging_diagram]').attr('class', 'straight_mid')
	}
});

$('[name=shooting_target]').on('click', function() {
	getStaging()
	getGoal()
	if (getStaging()==3 && getGoal()==3) {
		$('[name=staging_diagram]').attr('class', 'straight_right')
	}
});


$('[name=staging_position]').on('click', function() {
	getStaging()
	getGoal()
	if (getStaging()==1 && getGoal()==3) {
		$('[name=staging_diagram]').attr('class', 'straight_left')
	}
	NetworkTables.putValue('/SmartDashboard/driveforward', $('[name=staging_position]:checked').val());
});

$('[name=staging_position]').on('click', function() {
	getStaging()
	getGoal()
	if (getStaging()==2 && getGoal()==3) {
		$('[name=staging_diagram]').attr('class', 'straight_mid')
	}
	NetworkTables.putValue('/SmartDashboard/driveforward', $('[name=staging_position]:checked').val());
});

$('[name=staging_position]').on('click', function() {
	getStaging()
	getGoal()
	if (getStaging()==3 && getGoal()==3) {
		$('[name=staging_diagram]').attr('class', 'straight_right')
	}
	console.log('staging position: ', $('[name=staging_position]:checked').val());
	NetworkTables.putValue('/SmartDashboard/driveforward', $('[name=staging_position]:checked').val());//getStaging())
});

// Shooting Diagram

$('[name=shooting_target]').on('click', function() {
	getGoal()
	getStaging()
	if (getGoal()==1 && getStaging()==1)
		$('[name=shooting_diagram]').attr('class', 'high left')
});

$('[name=shooting_target]').on('click', function() {
	getGoal()
	getStaging()
	if (getGoal()==1 && getStaging()==2)
		$('[name=shooting_diagram]').attr('class', 'high mid')
});

$('[name=shooting_target]').on('click', function() {
	getGoal()
	getStaging()
	if (getGoal()==1 && getStaging()==3)
		$('[name=shooting_diagram]').attr('class', 'high right')
});

$('[name=shooting_target]').on('click', function() {
	getGoal()
	getStaging()
	if (getGoal()==2 && getStaging()==1)
		$('[name=shooting_diagram]').attr('class', 'low left')
});

$('[name=shooting_target]').on('click', function() {
	getGoal()
	getStaging()
	if (getGoal()==2 && getStaging()==3)
		$('[name=shooting_diagram]').attr('class', 'low right')
});

$('[name=shooting_target]').on('click', function() {
	getGoal()
	getStaging()
	if (getGoal()==3)
		$('[name=shooting_diagram]').attr('class', 'nothing')
});

$('[name=shooting_target]').on('click', function() {
	getGoal()
	getStaging()
	if (getGoal()==2 && getStaging()==2)
		$('[name=shooting_diagram]').attr('class', 'nothing')
});








$('[name=staging_position]').on('click', function() {
	if (getGoal()==1 && getStaging()==1)
		$('[name=shooting_diagram]').attr('class', 'high left')
});

$('[name=staging_position]').on('click', function() {
	if (getGoal()==1 && getStaging()==2)
		$('[name=shooting_diagram]').attr('class', 'high mid')
});

$('[name=staging_position]').on('click', function() {
	if (getGoal()==1 && getStaging()==3)
		$('[name=shooting_diagram]').attr('class', 'high right')
});


$('[name=staging_position]').on('click', function() {
	if (getGoal()==2 && getStaging()==1)
		$('[name=shooting_diagram]').attr('class', 'low left')
});

$('[name=staging_position]').on('click', function() {
	if (getGoal()==2 && getStaging()==3)
		$('[name=shooting_diagram]').attr('class', 'low right')
});

$('[name=staging_position]').on('click', function() {
	if (getGoal()==3)
		$('[name=shooting_diagram]').attr('class', 'nothing')
});

$('[name=staging_position]').on('click', function() {
	if (getGoal()==2 && getStaging()==2)
		$('[name=shooting_diagram]').attr('class', 'nothing')
});

//Obsticle pictures

$('[name=obsticle_types]').on('click', function () {
	getObsticle()
	if (getObsticle()==1)
		$('[name=obsticle]').attr('class','low_bar')	
});

$('[name=obsticle_types]').on('click', function () {
	getObsticle()
	if (getObsticle()==2)
		$('[name=obsticle]').attr('class','portcullis')	
});

$('[name=obsticle_types]').on('click', function () {
	getObsticle()
	if (getObsticle()==3)
		$('[name=obsticle]').attr('class','cheval_de_frise')	
});

$('[name=obsticle_types]').on('click', function () {
	getObsticle()
	if (getObsticle()==4)
		$('[name=obsticle]').attr('class','moat')	
});

$('[name=obsticle_types]').on('click', function () {
	getObsticle()
	if (getObsticle()==5)
		$('[name=obsticle]').attr('class','ramparts')	
});

$('[name=obsticle_types]').on('click', function () {
	getObsticle()
	if (getObsticle()==6)
		$('[name=obsticle]').attr('class','drawbridge')	
});

$('[name=obsticle_types]').on('click', function () {
	getObsticle()
	if (getObsticle()==7)
		$('[name=obsticle]').attr('class','sally_port')	
});

$('[name=obsticle_types]').on('click', function () {
	getObsticle()
	if (getObsticle()==8)
		$('[name=obsticle]').attr('class','rock_wall')	
});

$('[name=obsticle_types]').on('click', function () {
	getObsticle()
	if (getObsticle()==9)
		$('[name=obsticle]').attr('class','rough_terrain')	
});

$('[name=staging_position]').on('click', function () {
	getStaging
	if (getStaging()==1)
		$('[name=obsticle]').attr('class','low_bar')	
});

$('[name=staging_position]').on('click', function () {
	//getStaging
	if (getStaging()==1)
		$('[name=obsticle_types][value=1]').prop('checked', true);
});