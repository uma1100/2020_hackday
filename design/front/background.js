var pg;

function preload() {
	font = loadFont('https://openprocessing-usercontent.s3.amazonaws.com/files/user203303/visual808490/h24d7452822eaf68f42a5f583d50117c8/FOUNGM__.TTF');
}
let points;
let bounds;
let fontSize = 250;
let prevSecs;
let start;
// let running = false;
let ellapsed;

function setup() {
	createCanvas(windowWidth, windowHeight);
  bounds = font.textBounds("00:00:00", 0, 0, fontSize);
  ellapsed = 0;
  start = 90;
}

function draw() {
  ellapsed = millis() - start;
  console.log(15-millis()/1000);
  
	background(0);
  var secs = nf(5-ellapsed/1000,1, 2);
  if(secs <= 0){
    secs = -1;
  }
	if (secs >= 0) {
		prevSecs = secs;
		var mins = nf(minute(), 2, 0);
		var hours = nf(hour(), 2, 0);
		points = font.textToPoints(secs, 150, -150, fontSize, {
			sampleFactor: 0.1,
			simplifyThreshold: 0
		});
	}else{
    points = font.textToPoints('EAT BREAD', 150, -100, fontSize-150, {
			sampleFactor: 0.1,
			simplifyThreshold: 0.00
		});
    
    text("win", 230, 20); 
  }
	strokeWeight(abs(sin(frameCount*0.1))*30);
	stroke(255);
	noFill();
	translate((width - bounds.w) / 2, ((height - bounds.h) / 2 ) + bounds.h);
	var amp = map(mouseX*0.01, 0, width, 0, 5);
	var freq = map(mouseY*0.01, 0, height, 0, 3);
	beginShape(POINTS);
	for (let i = 0; i < points.length; i++) {
		let p = points[i];
		var x = p.x + cos(radians(p.y + frameCount*freq)) * amp;
		var y = p.y + tan(radians(p.x + frameCount*freq)) * amp;
		vertex(x+noise(50+frameCount*0.1)*100, y+noise(frameCount*0.1)*100);
	}
  endShape();
  noStroke();
  fill(110,110,255);

  text("Progress bar blue - size 620", 230, 20); 
  rect(230,30, 620, 30 );


  
}