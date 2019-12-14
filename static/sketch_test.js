// example progressbar
// default variables for progressbar
// start the time for progressbar
// boolean for the end progressbar
var done;

var hitpoint;
var evaluation;
var hp_width;
var count;
var judge;
function preload() {
  font = loadFont(
    "https://openprocessing-usercontent.s3.amazonaws.com/files/user203303/visual808490/h24d7452822eaf68f42a5f583d50117c8/FOUNGM__.TTF"
  );
}
let points;
let bounds;
let fontSize = 250;
let prevSecs;
let start;
var player_point = 0;
var enemy_point = 0;
// let running = false;
let ellapsed;
// settings for this example
function setup() {
  Img = loadImage("../static/pan.png");
  // set title of window
  //frame.setTitle("Example progressbar | free-tutorials.org");
  // window size and background color
  // p5.js
  createCanvas(windowWidth, windowHeight);
  bounds = font.textBounds("00:00:00", 0, 0, fontSize);
  ellapsed = 0;
  start = false;

  //size(640,130);
  background(25);
  // set variables of progressbar
  done = false;
  hp_width = 620;
  hitpoint = 1;
  evaluation = 0;
  count = 0;
  attack_val = 0;
  judge = true;
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
  // set same background color
  background(255);

  // background(0);
  noStroke();

  if (start) {
    ellapsed = millis();
    var secs = nf(30 - ellapsed / 1000, 1, 2);
    if (secs <= 0) {
      secs = -1;
    }
    if (secs >= 0) {
      for (let [cloor, x, y, r] of circle_array) {
        fill(cloor);
        ellipse(x, y, r, r);
      }
      fill(0, 100, 0);
      textSize(200);
      text("Battle!!!", 350, 150);

      prevSecs = secs;
      var mins = nf(minute(), 2, 0);
      var hours = nf(hour(), 2, 0);
      points = font.textToPoints(secs, 190, -150, fontSize, {
        sampleFactor: 0.1,
        simplifyThreshold: 0
      });
      if (hitpoint >= hp_width) {
        hitpoint = hp_width;
      } else if (hitpoint <= 0) {
        hitpoint = 0;
      }
      console.log(hitpoint);
      
    } else {
      evaluation = 0;
      if (hitpoint >= hp_width / 2) {
        console.log("finish");
        image(Img, 200, 300, 300, 300);
        points = font.textToPoints("EAT BREAD", 240, -100, fontSize - 150, {
          sampleFactor: 0.1,
          simplifyThreshold: 0.0
        });
        if (judge) {
          finish_notice(1);          
          judge = false;
        }
        // noLoop();
      } else {
        image(Img, 1000, 300, 300, 300);
        console.log("bad finish");
        points = font.textToPoints("NOT EAT", 250, -100, fontSize - 150, {
          sampleFactor: 0.1,
          simplifyThreshold: 0.0
        });
        if (judge) {
          finish_notice(0);          
          judge = false;
        }
        // noLoop();
      }
    }
  } else {
    // fill(110, 110, 255);
    // no stroke for draw
    points = font.textToPoints("Loading...", 150, -150, fontSize - 100, {
      sampleFactor: 0.1,
      simplifyThreshold: 0
    });
  }
  strokeWeight(abs(sin(frameCount * 0.1)) * 30);
  // stroke(255);
  // noFill();
  stroke(0);
  noFill();
  translate((width - bounds.w) / 2, (height - bounds.h) / 2 + bounds.h);
  var amp = map(mouseX * 0.01, 0, width, 0, 5);
  var freq = map(mouseY * 0.01, 0, height, 0, 3);
  beginShape(POINTS);
  for (let i = 0; i < points.length; i++) {
    let p = points[i];
    var x = p.x + cos(radians(p.y + frameCount * freq)) * amp;
    var y = p.y + tan(radians(p.x + frameCount * freq)) * amp;
    vertex(
      x + noise(50 + frameCount * 0.1) * 100,
      y + noise(frameCount * 0.1) * 100
    );
  }
  endShape();

  // check end of progressbar fill
  done = true;
  // create the color for fill progressbar
  // no stroke for draw
  noStroke();
  // show all text variables and progressbar

  fill("blue");
  textSize(100);
  textFont(font);
  text(str(player_point), 110, 90);
  text("PLAYER", -20, 200);
  fill("red");
  text(str(enemy_point), 900, 90);
  text("ENEMY", 750, 200);
  textSize(15);

  fill("red");
  rect(230, 30, 620, 30);
  // rect(width / 2 - 310, height / 2, hitpoint, 30);
  hitpoint += evaluation;
  count++;
  if (count > Math.abs(evaluation)) {
    evaluation = 0;
  }
  fill("blue");

  rect(230, 30, hitpoint, 30);
  // evaluation = 0;
  // console.log(hitpoint);

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
    bias = 0.5;
    var random_x = Math.random() * width;
    var random_y = Math.random() * height;
    circle_array.push(["#E7B8C2", random_x, random_y, 20 * enemy]);
    random_x = Math.random() * width;
    random_y = Math.random() * height;
    circle_array.push(["#008DBD", random_x, random_y, 20 * player]);
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
    enemy_point = enemy;
    player_point = player;

    maxTime = int(random(1000, 1976));
    done = false;
    active = true;
    start = true;
    count = 0;
  }
}

// function mousePressed () {
//   if (done) {
//     // counter = 0; startTime = millis();
//     // attack_val = 1;
//     bias = 10;
//     evaluation += 30;
//     console.log(evaluation);

//     // maxTime = int(random(1000, 1976));
//     done = false;
//     active = true;
//     count = 0;
//   done=false;
//   }
// }
