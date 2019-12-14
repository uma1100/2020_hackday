
var enemy = 0;
var player = 0;
var id = setInterval(function () {
    console.log('get');
    $.ajax({
        type: 'GET',
        url: './get_joycon_data'
    }).done(function (res) {
        console.log(res);
        enemy = res.player1;
    }).fail(function() {
        console.log('正しい結果を得られませんでした。');
      });
}, 1000);

var id = setInterval(function () {
    console.log("local");
    $.ajax({
        type: 'GET',
        url: './get_joycon_L_data'
    }).done(function (res) {
        console.log(res);
        player = res.L_data;
        test(enemy,player);

    }).fail(function() {
        console.log('正しい結果を得られませんでした。');
      });
}, 200);
// });

// $('#test').click(function () {
//     var val = int($('#test_val').val());
//     test(val);
// });