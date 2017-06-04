function dom(tagName, options, content)
{
	var result = document.createElement(tagName);
	if (options && typeof options === typeof {})
	{
		for (var key in options)
		{
			if (!options.hasOwnProperty(key)) continue;
			result.setAttribute(key, options[key].toString());
		}
	}
	if (content)
	{
		appendContent(result, content);
	}
	return result;
}
function appendContent(el, content)
{
	if (typeof content === typeof '')
		el.innerHTML = content;
	else if (content instanceof HTMLElement)
		el.appendChild(content);
	else if (Array.isArray(content))
		content.forEach(function (c) { appendContent(el, c); });
}

function TextRect (rect)
{
	if (typeof rect !== typeof {}) rect = {};
	if (typeof rect.x !== typeof 0) rect.x = 0;
	if (typeof rect.y !== typeof 0) rect.y = 0;
	if (typeof rect.width !== typeof 0) rect.width = 20;
	if (typeof rect.height !== typeof 0) rect.height = 20;

	this.rect = rect;
	this.el = null;
}
TextRect.prototype.render = function renderTextRect ()
{
	var textRect = this;
	var label = dom('div', { class: 'text_label' }, this.toString());

	var buttons = [
		dom('input', { type: 'button', class: 'btn btn-primary', value: 'Show' }),
		dom('input', { type: 'button', class: 'btn btn-primary edit_btn', value: 'Edit' }),
		dom('input', { type: 'button', class: 'btn btn-danger', value: 'Remove' })
	];
	buttons[0].addEventListener('click', function ()
	{
		TextRectManager.hilight(textRect);
	});
	buttons[1].addEventListener('click', function ()
	{
		TextRectManager.select(textRect);
	});
	buttons[2].addEventListener('click', function ()
	{
		TextRectManager.remove(textRect);
	});

	var container = dom('div', { class: 'text_region' }, [label].concat(buttons));
	this.el = container;
	this.labelEl = label;
	return container;
};
TextRect.prototype.update = function ()
{
	if (this.el === null)
	{
		this.render();
		return;
	}
	this.labelEl.innerHTML = this.toString();
};
TextRect.prototype.toString = function ()
{
	return 'Rect: { x: ' + Math.round(this.rect.x) + ', y: ' + Math.round(this.rect.y) +
	       '; width: ' + Math.round(this.rect.width) + ', height: ' + Math.round(this.rect.height) + ' }';
};

var TextRectManager = {
	all: [],
	current: -1,
	em: {
		i: -1,
		timer: null,
		alpha: 1.0
	},
	container: null,
	cropper: null,
	render: function ()
	{
		if (TextRectManager.container === null) return;
		if (TextRectManager.all.length === 0)
		{
			TextRectManager.container.innerHTML = Settings.strings.noTexts;
		}
		TextRectManager.all.forEach(function (rect)
		{
			TextRectManager.container.appendChild(rect.render());
		});
	},
	addNew: function (defVals)
	{
		var n = new TextRect(defVals);
		TextRectManager.all.push(n);
		if (TextRectManager.all.length === 0)
			TextRectManager.container.innerHTML = '';
		TextRectManager.container.appendChild(n.render());
		TextRectManager.current = TextRectManager.all.length - 1;
		TextRectManager.updateSelected();
	},
	remove: function (textRect)
	{
		for (var i = 0; i < TextRectManager.all.length; i++)
		{
			var tr = TextRectManager.all[i];
			if (tr === textRect)
			{
				TextRectManager.container.removeChild(tr.el);
				TextRectManager.all.splice(i, 1);
				if (i < TextRectManager.current)
				{
					TextRectManager.current--;
					TextRectManager.updateSelected();
				}
				else if (i === TextRectManager.current)
					TextRectManager.current = -1;

				// make image cropper to update the picture, 'coz we can be in 'crop' mode
				window.crop.refresh();
				break;
			}
		}
	},
	clear: function ()
	{
		TextRectManager.all = [];
		TextRectManager.current = -1;
		TextRectManager.render();
		TextRectManager.cropper.refresh();
		TextRectManager.updateSelected();
	},

	cropChanged: function (newCrop)
	{
		if (TextRectManager.current !== -1)
		{
			var tr = TextRectManager.all[TextRectManager.current];
			if (tr)
			{
				tr.rect = newCrop;
				tr.update();
			}
		}
		else
		{
			// if no crop were selected - create a new one
			TextRectManager.addNew(newCrop);
		}
	},

	select: function (tr)
	{
		for (var i = 0; i < TextRectManager.all.length; i++)
		{
			var current = TextRectManager.all[i];
			if (tr === current)
			{
				TextRectManager.current = i;
				TextRectManager.updateSelected();
				break;
			}
		}
	},

	deselect: function ()
	{
		var all = TextRectManager.all;
		for (var i = 0; i < all.length; i++)
		{
			all[i].el.classList.remove('current');
		}
	},

	updateSelected: function ()
	{
		var current = TextRectManager.all[TextRectManager.current];
		if (!current) return;
		TextRectManager.deselect();
		TextRectManager.cropper.setEnabled(true);
		TextRectManager.cropper.setCrop(current.rect);
		current.el.classList.add('current');
	},

	initCropper: function ()
	{
		var cropper = TextRectManager.cropper = new Cropper();
		cropper.color = '#08f';
		cropper.setEnabled(false);
		cropper.shadowOutside = false;
		cropper.sizes.xm = cropper.sizes.ym = Settings.imagePadding;
		cropper.oncropchanged = function ()
		{
			TextRectManager.cropChanged(TextRectManager.cropper.getCrop());
		};
		cropper.onrenderstart = function (ctx)
		{
			TextRectManager.renderTexts(ctx);
			var crop = window.crop.getCrop();
			var oldStroke = [ctx.strokeStyle, ctx.strokeWidth];
			ctx.strokeStyle = '#800';
			ctx.strokeWidth = '3px';
			ctx.strokeRect(crop.x, crop.y, crop.width, crop.height);
			ctx.strokeStyle = oldStroke[0];
			ctx.strokeWidth = oldStroke[1];
		}
	},

	renderTexts: function (ctx)
	{
		var oldFill = ctx.fillStyle;
		for (var i = 0; i < TextRectManager.all.length; i++)
		{
			if (i === TextRectManager.current)
				ctx.fillStyle = Settings.textRect.activeColor;
			else
				ctx.fillStyle = Settings.textRect.color;
			var r = TextRectManager.all[i].rect;
			ctx.fillRect(r.x, r.y, r.width, r.height);
		}

		if (TextRectManager.em.i !== -1)
		{
			var h = TextRectManager.all[TextRectManager.em.i].rect;
			ctx.fillStyle = Settings.textRect.hilightColor.replace(/\$a/g, TextRectManager.em.alpha + '');
			ctx.fillRect(h.x, h.y, h.width, h.height);
		}
		ctx.fillStyle = oldFill;
	},

	hilight: function (tr)
	{
		var em = TextRectManager.em;
		var params = {
			onInterval: TextRectManager.timerOnInterval,
			onEnd: TextRectManager.timerOnEnd,
			delay: 0,
			iterations: Settings.textRect.hilightFrames,
			interval: 30
		};
		if (em.timer !== null)
		{
			em.timer.interrupt();
		}
		em.timer = new Timer(params);
		em.alpha = 1.0;

		for (var i = 0; i < TextRectManager.all.length; i++)
		{
			var current = TextRectManager.all[i];
			if (tr === current)
			{
				em.i = i;
				break;
			}
		}

		em.timer.start();
	},

	timerOnInterval: function ()
	{
		var em = TextRectManager.em;
		em.alpha -= 1 / Settings.textRect.hilightFrames;
		TextRectManager.cropper.refresh();
		window.crop.refresh();
	},
	timerOnEnd: function ()
	{
		var em = TextRectManager.em;
		em.i = -1;
	}
};
