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
  background(255);
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
var circle_array = []; // 円の色、位置、半径を記録する用の配列
function draw() {
  done = true;
  noStroke();
  // 円の描写 ここから
  // 円の登録 ここから
  fill("red");
  var random_x = Math.random() * width;
  var random_y = Math.random() * height;
  ellipse(random_x, random_y, 100, 100);
  fill("blue");
  random_x = Math.random() * width;
  random_y = Math.random() * height;
  ellipse(random_x, random_y, 100, 100);

  text("Progress bar blue - size 620", 230, 20);
  //ここまで

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

    // 円の登録 ここから
    var random_x = Math.random() * width;
    var random_y = Math.random() * height;
    circle_array.push(["red", random_x, random_y, 20 * enemy]);
    random_x = Math.random() * width;
    random_y = Math.random() * height;
    circle_array.push(["blue", random_x, random_y, 20 * player]);
    // ここまで

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

function mousePressed() {
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
    done = false;
  }
}
