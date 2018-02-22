document.addEventListener("DOMContentLoaded", function(event) { 

	function sleep(ms) {
	  return new Promise(resolve => setTimeout(resolve, ms));
	}

	async function playback(events) {
		for (var i = 0; i < events.length - 1; i++) {
			el = document.querySelector(events[i].selector);
			el.style.background = 'rgba(255, 0, 0, .5)';
			let difference = events[i+1].timestamp - events[i].timestamp;
			await sleep(difference);
			el.style.background = null;
		}
	}

	playback(events)

})