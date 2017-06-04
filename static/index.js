window.addEventListener('load', function ()
{
	window.el = {
		f: document.getElementById('f'),
		response: document.getElementById('response'),
		file: document.getElementById('file'),
		filename: document.getElementById('filename'),
		b: {
			open: document.getElementById('open_btn'),
			resetCrop: document.getElementById('reset_btn'),
			process: document.getElementById('process_btn'),
			oneMore: document.getElementById('one_more_btn'),

			addText: document.getElementById('text_add_btn'),
			removeAllTexts: document.getElementById('text_remove_all_btn'),
			textDone: document.getElementById('text_done_btn'),
			textMode: document.getElementById('text_mode_btn'),

			saveText: document.getElementById('save_text_btn'),
			saveImg: document.getElementById('save_image_btn')
		},
		r: {
			image: document.getElementById('result_img'),
			text: document.getElementById('result_text'),
			fontSizeLabel: document.getElementById('font_size_label')
		},
		panels: {
			main: document.getElementById('tools_panel'),
			text: document.getElementById('texts_panel')
		},
		textContainer: document.getElementById('text_list_container'),
		c: document.getElementById('c')
	};

	showForm();
	switchPanel('main');
	window.editMode = 'crop';

	window.image = null;
	window.crop = new Cropper();
	window.crop.oncropchanged = function ()
	{
		updateStatus();
	};
	window.crop.sizes.cursor = Settings.crop.cursorSize;
	window.crop.sizes.xm = window.crop.sizes.ym = Settings.imagePadding;
	window.crop.color = Settings.crop.color;
	window.crop.shadowOutside = Settings.crop.shadow;

	TextRectManager.container = el.textContainer;
	TextRectManager.render();
	TextRectManager.initCropper();
	window.crop.onrenderstart = TextRectManager.renderTexts;

	var slider = new Slider('#font_size_slider', {
		min: 8,
		max: 36,
		step: 1,
		value: 14
	});
	slider.on('slide', function (val)
	{
		el.r.fontSizeLabel.innerHTML = el.r.text.style.fontSize = val + 'pt';
	});
	window.fontSlider = slider;

	el.b.open.addEventListener('click', function ()
	{
		el.file.click();
	});

	el.b.resetCrop.addEventListener('click', function ()
	{
		crop.resetCrop();
	});

	el.b.process.addEventListener('click', function ()
	{
		if (sendRequest())
			el.filename.innerHTML = Settings.strings.requestPending;
	});

	el.file.addEventListener('change', function ()
	{
		var theFile = el.file.files[0];
		if (checkValidity(theFile))
			openImage(theFile);
		else
			alert(Settings.strings.wrongFileType);
	});

	el.b.oneMore.addEventListener('click', function ()
	{
		showForm();
	});

	el.b.addText.addEventListener('click', function ()
	{
		TextRectManager.addNew(crop.getCrop());
	});

	el.b.removeAllTexts.addEventListener('click', function ()
	{
		if (confirm(Settings.strings.removeAllTexts))
			TextRectManager.clear();
	});

	el.b.textMode.addEventListener('click', function ()
	{
		switchPanel('text');
		startTextEditing();
	});

	el.b.textDone.addEventListener('click', function ()
	{
		switchPanel('main');
		endTextEditing();
	});

	el.b.saveText.addEventListener('click', function ()
	{
		var blob = new Blob([el.r.text.innerHTML], {type: 'text/plain;charset=utf-8'});
		var name = 'ascii.txt';
		if (window.image && window.image.file && window.image.file.name)
			name = window.image.file.name.replace(/\..+$/g, '.txt');
		saveAs(blob, name);
	});
});

function openImage(file)
{
	window.image = { file: file, url: URL.createObjectURL(file), img: new Image() };
	image.img.onload = function ()
	{
		el.c.width = image.img.width + crop.sizes.xm * 2;
		el.c.height = image.img.height + crop.sizes.ym * 2;
		window.crop.init(el.c, image.img);
		TextRectManager.cropper.init(el.c, image.img);
		TextRectManager.clear();
		updateStatus();
	};
	image.img.src = image.url;
}


function sendRequest()
{
	if (!image || !image.file)
	{
		alert(Settings.strings.noImage);
		return false;
	}
	if (!checkValidity(image.file))
	{
		alert(Settings.strings.wrongFileType);
		return false;
	}

	var req = new XMLHttpRequest();
	var data = new FormData();
	data.append('text', JSON.stringify(TextRectManager.all.map(function (tr) { return tr.rect; })));
	data.append('crop', JSON.stringify(crop.getCrop()));
	data.append('image_type', JSON.stringify(image.file.type));
	data.append('image', image.file);
	console.log(data);
	req.open('POST', 'api/process', true);

	req.onreadystatechange = function ()
	{
		if (req.readyState !== 4) return;
		if (req.status === 200)
		{
			showStatus(Settings.strings.success);
			showResults(JSON.parse(req.responseText));
		}
		else if (req.status > 0)
		{
			el.filename.innerHTML = 'Server reported an error: '
				+ req.statusText
				+ ', message: '
				+ JSON.parse(req.responseText).message;
		}
		else
		{
			showStatus(Settings.strings.serverUnavailable);
		}
	};

	req.send(data);
	return true;
}

function checkValidity(file)
{
	return /image\/.+/.test(file.type);
}


function updateStatus()
{
	var crop = window.crop.getCrop();
	var status = 'Selected: ' + image.file.name
		+ ' (' + image.file.type + '); '
		+ 'Cropped { x: ' + Math.round(crop.x) + ', y: ' + Math.round(crop.y)
		+ '; width: ' + Math.round(crop.width) + ', height: ' + Math.round(crop.height)
		+ ' }';
	el.filename.innerHTML = status;
}
function showStatus (text)
{
	el.filename.innerHTML = text;
}

function showResults(responseObj)
{
	window.el.f.style.display = 'none';
	window.el.response.style.display = 'block';

	console.log(responseObj);

	el.r.image.src = responseObj.image;
	el.r.text.innerHTML = responseObj.text;

	el.b.saveImg.setAttribute('href', responseObj.image);
}

function showForm()
{
	window.el.response.style.display = 'none';
	window.el.f.style.display = 'block';
}

function switchPanel(panelName)
{
	var panels = Object.keys(el.panels);
	for (var i = 0; i < panels.length; i++)
	{
		var curPanelName = panels[i];
		var panel = el.panels[curPanelName];
		if (curPanelName == panelName)
		{
			panel.style.display = 'block';
		}
		else
		{
			panel.style.display = 'none';
		}
	}
}

function startTextEditing()
{
	window.editMode = 'text';
	crop.setEnabled(false);
	TextRectManager.cropper.setEnabled(true);
	if (TextRectManager.all.length)
	{
		TextRectManager.select(TextRectManager.all[0]);
	}
	else
	{
		TextRectManager.cropper.setCrop(crop.getCrop());
	}
	showStatus(Settings.strings.textMode);
	el.textContainer.classList.remove('no_edit');
}

function endTextEditing()
{
	window.editMode = 'crop';
	TextRectManager.cropper.setEnabled(false);
	TextRectManager.current = -1;
	TextRectManager.deselect();
	crop.setEnabled(true);
	updateStatus();
	el.textContainer.classList.add('no_edit');
}
