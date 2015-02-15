/**
 * Client library to POST email registrations back to 
 * the register-interest service.
**/

var home = "{{home}}";

var RegisterInterest = (function(w, home) {
	var registerEmail = function(email, callback) {
		// Get the referrer site
		var referrer = w.location.origin;

		// Setup the callback
		var xhr = new XMLHttpRequest();
		xhr.onreadystatechange = function() {
			if(xhr.readyState == 4 && xhr.status == 200) {
				console.log("Successfully posted interest");
				callback();
			}
		}

		// Phone home with the details
		xhr.open('POST', home, true);
		xhr.send('email='+email+'&referrer='+referrer);
	}

	return {
		register: registerEmail
	}
})(window, home);