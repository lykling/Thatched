var canvas = null;
var context = null;
var bufferCanvas = null;
var bufferCanvasCtx = null;
var flakeArray = [];
var flakeTimer = null;
var maxFlakes = 300;
var background = new Image();
var bgpic = new Image();
function init() {
	background.src = '/static/images/backgrounds.jpg';
	canvas = document.getElementById('basic_canvas');
	context = canvas.getContext("2d");
	context.globalAlpha= (Math.sin(10));
	bufferCanvas = document.createElement('canvas');
	bufferCanvasCtx = bufferCanvas.getContext('2d');
	//bufferCanvasCtx.canvas.width = context.canvas.width;
	//bufferCanvasCtx.canvas.height = context.canvas.height;
	bufferCanvasCtx.canvas.width = context.canvas.width;
	bufferCanvasCtx.canvas.height = context.canvas.height;
	flakeTime = setInterval(addFlake, 200);
	Draw();
	setInterval(animate, 30);
}
function addFlake() {
	flakeArray[flakeArray.length] = new Flake();
	if (flakeArray.length == maxFlakes) {
		clearInterval(flakeTimer);
	}
}
function Draw() {
	context.save();
	blank();
	for (var i = 0; i < flakeArray.length; i ++) {
		bufferCanvasCtx.beginPath()
			bufferCanvasCtx.arc(flakeArray[i].x, flakeArray[i].y, flakeArray[i].width + 3, 0, 360, true);
		bufferCanvasCtx.closePath()
			bufferCanvasCtx.fillStyle = "white";
		//bufferCanvasCtx.fillRect(flakeArray[i].x,flakeArray[i].y,flakeArray[i].width,flakeArray[i].height);
		bufferCanvasCtx.fill();
	}
	context.drawImage(bufferCanvas, 0, 0, bufferCanvas.width, bufferCanvas.height);
	context.restore();
}
function animate() {
	Update();
	Draw();
}
function Flake() {
	this.x = Math.round(Math.random() * context.canvas.width);
	this.y = -10;
	this.drift = Math.random();
	this.speed = Math.round(Math.random() * 5) + 1;
	this.width = (Math.random() * 3) + 2;
	this.height = this.width;
}
function blank() {
	//bufferCanvasCtx.beginPath()
	//bufferCanvasCtx.arc(0, 0, Math.random() * 5 + 4, 0, 360, true);
	//bufferCanvasCtx.closePath()
	//bufferCanvasCtx.fillStyle = "#330033";
	//bufferCanvasCtx.fillRect(0, 0, bufferCanvasCtx.canvas.width, bufferCanvasCtx.canvas.height);
	bufferCanvasCtx.drawImage(background, 0, 0, context.canvas.width, context.canvas.height);
	//bufferCanvasCtx.fill();
}
function Update() {
	for (var i = 0; i < flakeArray.length; i ++) {
		if (flakeArray[i].y < context.canvas.height) {
			flakeArray[i].y += flakeArray[i].speed;
			if (flakeArray[i].y > context.canvas.height) {
				flakeArray[i].y -= 5;
			}
			flakeArray[i].x += flakeArray[i].drift;
			if (flakeArray[i].x > context.canvas.width) {
				flakeArray[i].x = 0;
			}
		}
	}
}
