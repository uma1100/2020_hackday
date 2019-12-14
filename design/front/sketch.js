// example progressbar 
// default variables for progressbar
// start the time for progressbar
var startTime; 
// counter progressbar 
var counter;
// maximum time progressbar
var maxTime; 
// boolean for the end progressbar 
var done; 
let font;

let points;
let bounds;
let fontSize = 250;
let prevSecs;


var hitpoint;
var damage;
var hp_width;
var active;
var count;
// settings for this example
function setup() { 
	bounds = font.textBounds("00:00:00", 0, 0, fontSize);

// set title of window
//frame.setTitle("Example progressbar | free-tutorials.org");
// window size and background color
// p5.js
createCanvas(windowWidth,windowHeight);
 
//size(640,130);
background(25); 
// set variables of progressbar
counter = 0; 
startTime= millis(); 
maxTime=int(random(1000,1976)); 
done=false; 
active = false;
hp_width = 620;
hitpoint = hp_width / 2;
damage = 0;
count = 0;
attack_val = 0;
//end settings
} 
function sleep(waitMsec) {
  var startMsec = new Date();
 
  // 指定ミリ秒間だけループさせる（CPUは常にビジー状態）
  while (new Date() - startMsec < waitMsec);
}
// draw all text and progressbar
function draw() { 
  fill('red');
  rect(width/2-310,height/2, 620, 30 );
  // set same background color
  // background(255); 
 
  // check end of progressbar fill
  if (counter-startTime < maxTime) {
  counter=millis();
  }  else { done=true;  }
  // create the color for fill progressbar
  fill(110,110,255);
  // no stroke for draw
  noStroke();
  // show all text variables and progressbar
  text("Progress bar blue - size 620", 230, 20); 
  fill('red');
  rect(width/2-310,height/2, 620, 30 );
  fill('blue');
  rect(width/2-310,height/2,hitpoint,30);
  if(damage > 0){
    hitpoint += attack_val;
    count++;
  }else{
    hitpoint -= attack_val;
    count++;
  }
  if(count > Math.abs(damage)){
    attack_val = 0;
  }
  rect(width/2-310,height/2, hitpoint, 30 );
  console.log(hitpoint);
  
  
  // rect(width/2-310,height/2,map(counter-startTime,0,maxTime,0,310), 30 );
  // text("counter- startTime "+int(counter- startTime)+" ",10,80);
  // text("maxTime "+ int(maxTime) +  " ", 10,100);
  // text("map converted counter-startTime"+ int ( map(counter-startTime,0,maxTime,0,200)), 10,120);
  noFill();
 
  }
// reload the draw of progress bar 
function test (val) { 
  if (done) {
    counter = 0; startTime= millis();
    attack_val = 1;
    damage = val;
    maxTime=int(random(1000,1976)); 
    done=false;
    active=true;
    count = 0;
  }
}
