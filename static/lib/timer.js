/**
 * @author BobNobrain
 * Created at 03.06.2017
 * Simple lib for a bit more complex work with setInterval and setTimeout
 * (actually, uses only setTimeout and clearTimeout)
 */
window.Timer = (function (setTimeout, clearTimeout)
{
	'use strict';

	function noop () {}

	function Timer(params)
	{
		if (typeof params !== typeof {}) params = {};
		if (typeof params.duration !== typeof 0) params.duration = 5000;
		if (typeof params.interval !== typeof 0) params.interval = 1;
		if (typeof params.delay !== typeof 0) params.delay = 0;
		if (typeof params.onStart !== typeof noop) params.onStart = noop;
		if (typeof params.onInterval !== typeof noop) params.onInterval = noop;
		if (typeof params.onEnd !== typeof noop) params.onEnd = noop;
		if (typeof params.sync !== typeof false) params.sync = false;

		if (typeof params.iterations === typeof 0)
		{
			params.duration = params.interval * params.iterations;
		}

		var timer = -1;
		var running = false;
		this.isRunning = function () { return running; };

		var left = 0;

		this.interrupt = function ()
		{
			if (timer !== -1)
			{
				clearTimeout(timer);
				running = false;
			}
		};

		this.start = function ()
		{
			running = true;
			left = Math.floor(params.duration / params.interval);
			if (params.sync && params.delay === 0)
			{
				firstIteration();
			}
			else
			{
				timer = setTimeout(firstIteration, params.delay);
			}
		};

		function firstIteration()
		{
			params.onStart();
			timer = setTimeout(nextIteration, params.interval)
		}
		function nextIteration()
		{
			if (left > 0)
			{
				--left;
				params.onInterval();
				timer = setTimeout(nextIteration, params.interval);
			}
			else if (left === 0)
			{
				params.onInterval();
				var ms = params.duration - Math.floor(params.duration / params.interval) * params.interval;
				if (params.sync && ms === 0)
					lastIteration();
				else
					timer = setTimeout(lastIteration, ms);
			}
		}
		function lastIteration()
		{
			params.onEnd();
			timer = -1;
			running = false;
		}
	}

	return Timer;
})(window.setTimeout, window.clearTimeout, window.setInterval, window.clearInterval);
