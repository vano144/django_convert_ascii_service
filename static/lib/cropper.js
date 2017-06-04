/**
 * @author BobNobrain
 * Created at 03.06.2017
 *
 * A lib for simple rectangle selection on an image
 * Look for usage example at https://github.com/BobNobrain/vanya-client/blob/master/index.js
 */

window.Cropper = (function (global)
{
	'use strict';

	function Cropper()
	{
		var crop = { x1: 0, y1: 0, x2: 0, y2: 0 };
		var c = null, image = null;
		var sizes = { xm: 20, ym: 20, cursor: 10 };
		var drag = {
			start: null,
			fin: null,
			dragging: false,
			obj: null
		};
		var enabled = true;

		this.init = function initCropper(canvas, img)
		{
			c = canvas;
			image = img;

			c.addEventListener('mousedown', function (ev)
			{
				if (!enabled) return;
				drag.start = relativeCoords(ev, sizes);
				drag.dragging = false;
			});
			c.addEventListener('mousemove', function (ev)
			{
				if (!enabled) return;
				if (!drag.start) return;
				var relCoords = relativeCoords(ev, sizes);
				var mx = relCoords.x, my = relCoords.y;
				if (drag.dragging) {
					drag.fin = { x: mx, y: my };
					doDrag(mx, my);
					refreshCanvas();
				}
				else {
					var dx = drag.start.x - mx, dy = drag.start.y - my;
					if (dx * dx + dy * dy > 25) {
						startDrag();
						doDrag(mx, my);
						refreshCanvas();
					}
				}
			});
			c.addEventListener('mouseup', function (ev)
			{
				if (!enabled) return;
				if (drag.dragging)
				{
					var rc = relativeCoords(ev, sizes);
					doDrag(rc.x, rc.y);
				}
				if (drag.start)
				{
					finDrag();
					refreshCanvas();
				}
			});
			c.addEventListener('mouseout', function ()
			{
				if (!enabled) return;
				if (drag.start)
				{
					finDrag();
					refreshCanvas();
				}
			});
			c.addEventListener('dragstart', function (ev) { return false; });

			resetCrop();
			refreshCanvas();
		};

		var _t = this;
		this.isDragging = function () { return drag.dragging; };
		this.getCanvas = function () { return c; };
		this.sizes = sizes;
		this.color = '#000';
		this.shadowOutside = true;
		this.isEnabled = function () { return enabled; };
		this.setEnabled = function (val) { enabled = val; refreshCanvas(); };
		this.getCrop = function ()
		{
			return { x: crop.x1, y: crop.y1, width: crop.x2 - crop.x1, height: crop.y2 - crop.y1 };
		};
		this.setCrop = function (newCrop)
		{
			crop.x1 = newCrop.x; crop.y1 = newCrop.y;
			crop.x2 = newCrop.width + newCrop.x; crop.y2 = newCrop.height + newCrop.y;
			this.oncropchanged();
			refreshCanvas();
		};
		this.resetCrop = function ()
		{
			resetCrop();
			refreshCanvas();
			this.oncropchanged();
		};
		this.oncropchanged = function () {};
		this.onrenderend = function () {};
		this.onrenderstart = function () {};
		this.refresh = refreshCanvas;

		//
		// helper functions
		//

		function ctx()
		{
			return c.getContext('2d');
		}

		function resetCanvas()
		{
			c.width += 0;
		}

		function resetCrop()
		{
			crop.x1 = crop.y1 = 0;
			crop.x2 = image.width;
			crop.y2 = image.height;
		}

		function refreshCanvas()
		{
			if (!enabled) return;
			resetCanvas();

			var c = ctx();
			c.translate(sizes.xm, sizes.ym);
			c.drawImage(image, 0, 0);

			_t.onrenderstart(c);

			c.fillStyle = _t.color;
			c.strokeStyle = _t.color;
			drawCursor(c, crop.x1, crop.y1);
			drawCursor(c, crop.x1, crop.y2);
			drawCursor(c, crop.x2, crop.y1);
			drawCursor(c, crop.x2, crop.y2);
			c.moveTo(crop.x1 + 0.5, crop.y1 + 0.5);
			c.lineTo(crop.x2 + 0.5, crop.y1 + 0.5);
			c.lineTo(crop.x2 + 0.5, crop.y2 + 0.5);
			c.lineTo(crop.x1 + 0.5, crop.y2 + 0.5);
			c.lineTo(crop.x1 + 0.5, crop.y1 + 0.5);
			c.stroke();

			if (_t.shadowOutside)
			{
				c.fillStyle = 'rgba(0, 0, 0, 0.5)';
				var left = Math.min(crop.x1, crop.x2);
				var right = Math.max(crop.x1, crop.x2);
				var top = Math.min(crop.y1, crop.y2);
				var bottom = Math.max(crop.y1, crop.y2);
				c.fillRect(0, 0, left, top);
				c.fillRect(left, 0, right - left, top);
				c.fillRect(right, 0, image.width - right, top);

				c.fillRect(0, top, left, bottom - top);
				c.fillRect(right, top, image.width - right, bottom - top);

				c.fillRect(0, bottom, left, image.height - bottom);
				c.fillRect(left, bottom, right - left, image.height - bottom);
				c.fillRect(right, bottom, image.width - right, image.height - bottom);
			}

			c.translate(-sizes.xm, -sizes.ym);
			_t.onrenderend(c);
		}

		function drawCursor(c, cx, cy)
		{
			c.fillRect(cx - sizes.cursor / 2, cy - sizes.cursor / 2, sizes.cursor, sizes.cursor);
		}

		function startDrag()
		{
			drag.dragging = true;
			drag.initialCrop = { x1: crop.x1, x2: crop.x2, y1: crop.y1, y2: crop.y2 };
			drag.obj = getDragObject(drag.start.x, drag.start.y, sizes.cursor, crop);
		}

		function doDrag(mx, my)
		{
			drag.fin = { x: mx, y: my };
			if (drag.obj !== null)
			{
				drag.obj.update(drag.start, drag.fin, drag.initialCrop, crop);
				_t.oncropchanged();
			}
		}

		function finDrag()
		{
			drag.start = null;
			drag.fin = null;
			drag.dragging = false;
			drag.obj = null;
			drag.initialCrop = null;

			// make crop rect not to be outside of image
			var x1 = boundify(crop.x1, 0, image.width);
			var x2 = boundify(crop.x2, 0, image.width);
			var y1 = boundify(crop.y1, 0, image.height);
			var y2 = boundify(crop.y2, 0, image.height);
			crop.x1 = Math.min(x1, x2);
			crop.x2 = Math.max(x1, x2);
			crop.y1 = Math.min(y1, y2);
			crop.y2 = Math.max(y1, y2);
			_t.oncropchanged();
		}
	}

	// enum
	var DragObject = {
		CURSOR_LT: {
			name: 'lt',
			update: function (dst, dfn, initC, c) { c.x1 = dfn.x; c.y1 = dfn.y; },
			hit: function (x, y, sz, crop) { return squareHit(x, y, crop.x1, crop.y1, sz) }
		},
		CURSOR_RT: {
			name: 'rt',
			update: function (dst, dfn, initC, c) { c.x2 = dfn.x; c.y1 = dfn.y; },
			hit: function (x, y, sz, crop) { return squareHit(x, y, crop.x2, crop.y1, sz) }
		},
		CURSOR_LB: {
			name: 'lb',
			update: function (dst, dfn, initC, c) { c.x1 = dfn.x; c.y2 = dfn.y; },
			hit: function (x, y, sz, crop) { return squareHit(x, y, crop.x1, crop.y2, sz) }
		},
		CURSOR_RB: {
			name: 'rb',
			update: function (dst, dfn, initC, c) { c.x2 = dfn.x; c.y2 = dfn.y; },
			hit: function (x, y, sz, crop) { return squareHit(x, y, crop.x2, crop.y2, sz) }
		},

		CURSOR_L: {
			update: function (dst, dfn, initC, c) { c.x1 = dfn.x; },
			hit: function (x, y, sz, crop) { return lineHitV(x, y, crop.y1, crop.y2, crop.x1, sz); }
		},
		CURSOR_R: {
			update: function (dst, dfn, initC, c) { c.x2 = dfn.x; },
			hit: function (x, y, sz, crop) { return lineHitV(x, y, crop.y1, crop.y2, crop.x2, sz); }
		},
		CURSOR_T: {
			update: function (dst, dfn, initC, c) { c.y1 = dfn.y; },
			hit: function (x, y, sz, crop) { return lineHitH(x, y, crop.x1, crop.x2, crop.y1, sz); }
		},
		CURSOR_B: {
			update: function (dst, dfn, initC, c) { c.y2 = dfn.y; },
			hit: function (x, y, sz, crop) { return lineHitH(x, y, crop.x1, crop.x2, crop.y2, sz); }
		},

		NONE: {
			name: 'none',
			update: function (dst, dfn, initC, c)
			{
				var dx = dfn.x - dst.x, dy = dfn.y - dst.y;
				c.x1 = initC.x1 + dx;
				c.x2 = initC.x2 + dx;
				c.y1 = initC.y1 + dy;
				c.y2 = initC.y2 + dy;
			},
			hit: function (x, y, sz, crop) { return true; }
		}
	};

	function getDragObject(x, y, sz, crop)
	{
		var objs = Object.keys(DragObject);
		for (var i = 0; i < objs.length; i++)
		{
			var obj = DragObject[objs[i]];
			if (obj.hit(x, y, sz, crop))
				return obj;
		}
		return DragObject.NONE;
	}

	function squareHit(x, y, cx, cy, sz)
	{
		if (x > cx + sz/2) return false;
		if (x < cx - sz/2) return false;
		if (y > cy + sz/2) return false;
		if (y < cy - sz/2) return false;
		return true;
	}

	function lineHitH(x, y, lineStart, lineEnd, lineY, sz)
	{
		if (x < lineStart) return false;
		if (x > lineEnd) return false;
		if (y > lineY + sz/2) return false;
		if (y < lineY - sz/2) return false;
		return true;
	}

	function lineHitV(x, y, lineStart, lineEnd, lineX, sz)
	{
		if (y < lineStart) return false;
		if (y > lineEnd) return false;
		if (x > lineX + sz/2) return false;
		if (x < lineX - sz/2) return false;
		return true;
	}

	function relativeCoords(event, sizes)
	{
		var bounds = event.target.getBoundingClientRect();
		var x = event.clientX - bounds.left;
		var y = event.clientY - bounds.top;
		return { x: x - sizes.xm, y: y - sizes.ym };
	}

	function boundify(val, min, max)
	{
		if (val < min) val = min;
		if (val > max) val = max;
		return val;
	}

	return Cropper;

})(window);
