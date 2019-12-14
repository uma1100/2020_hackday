
var enemy = 0;
var player = 0;
var flag = false;
var Right = setInterval(function () {
    $.ajax({
        type: 'GET',
        url: './get_joycon_R_data'
    }).done(function (data) {
        enemy = data.player1;
        flag = true;
    }).fail(function() {
        console.log('正しい結果を得られませんでした。');
      });
}, 1000);

var Left = setInterval(function () {
    $.ajax({
        type: 'GET',
        url: './get_joycon_L_data'
    }).done(function (data) {
        console.log(data);
        player = data.L_data;
        if(flag){
            battle(enemy,player);
        }

    }).fail(function() {
        console.log('正しい結果を得られませんでした。');
      });
}, 200);
// });

// $('#test').click(function () {
//     var val = int($('#test_val').val());
//     test(val);
// });