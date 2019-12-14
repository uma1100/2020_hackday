
// example progressbar 
// default variables for progressbar
// start the time for progressbar
// boolean for the end progressbar 
var done;

var hitpoint;
var evaluation;
var hp_width;
var count;
// settings for this example
function setup() {
  // set title of window
  //frame.setTitle("Example progressbar | free-tutorials.org");
  // window size and background color
  // p5.js
  createCanvas(windowWidth, windowHeight);

  //size(640,130);
  background(25);
  // set variables of progressbar
  done = false;
  hp_width = 620;
  hitpoint = 1;
  evaluation = 0;
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
  // set same background color
  background(255);

  // check end of progressbar fill
  done = true;
  // create the color for fill progressbar
  fill(110, 110, 255);
  // no stroke for draw
  noStroke();
  // show all text variables and progressbar
  text("Progress bar blue - size 620", 230, 20);
  fill('red');
  rect(width / 2 - 310, height / 2, 620, 30);
  fill('blue');
  // rect(width / 2 - 310, height / 2, hitpoint, 30);
  hitpoint += evaluation;
  count++;
  if (count > Math.abs(evaluation)) {
    evaluation = 0;
  }

  rect(width / 2 - 310, height / 2, hitpoint, 30);
  // evaluation = 0;
  // console.log(hitpoint);
  if (hitpoint >= hp_width) {
    console.log("finish");
    finish_notice(3);
    noLoop();
  }
  if (hitpoint <= 0) {
    console.log("bad finish");
    finish_notice(2);
    noLoop();

  }
  sleep(300);


  // rect(width/2-310,height/2,map(counter-startTime,0,maxTime,0,310), 30 );
  // text("counter- startTime "+int(counter- startTime)+" ",10,80);
  // text("maxTime "+ int(maxTime) +  " ", 10,100);
  // text("map converted counter-startTime"+ int ( map(counter-startTime,0,maxTime,0,200)), 10,120);
  noFill();

}
// reload the draw of progress bar 
function battle(player, enemy) {
  if (done) {
    attack_val = 1;
    bias = 5;
    if (enemy < player) {
      // playerのほうが運動量が多いとき
      evaluation = bias * player;
    } else if (enemy == player) {
      evaluation = 0;
    } else {
      // enemyのほうが運動量が多いとき
      evaluation = -1 * enemy * bias;
    }
    console.log("自分" + player + "相手" + enemy + "評価" + evaluation);

    maxTime = int(random(1000, 1976));
    done = false;
    active = true;
    count = 0;
  }
}

function mousePressed () { 
  if (done) { 
    // counter = 0; startTime = millis();
    // attack_val = 1;
    bias = 10;
    evaluation += 30;
    console.log(evaluation);

    // maxTime = int(random(1000, 1976));
    done = false;
    active = true;
    count = 0; 
  done=false;
  }
}
