
var _enemy = 0;
var player = 0;
var flag = false;
setInterval(function () {
    $.ajax({
        type: 'GET',
        url: './get_joycon_R_data'
    }).done(function (data) {
        _enemy = int(data.R_data);
        flag = true;
    }).fail(function() {
        console.log('正しい結果を得られませんでした。');
      });
}, 1000);

setInterval(function () {
    $.ajax({
        type: 'GET',
        url: './get_joycon_L_data'
    }).done(function (data) {
        // console.log(data);
        player = int(data.L_data);
        // console.log(_enemy);
        
        if(flag){
            battle(player,_enemy);
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