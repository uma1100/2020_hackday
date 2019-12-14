
var id = setInterval(function () {
    $.ajax({
        type: 'GET',
        url: './get_joycon_data'
    }).done(function (res) {
        test(res.player0,res.player1);
        console.log(res);

    })
}, 1000);
// });

// $('#test').click(function () {
//     var val = int($('#test_val').val());
//     test(val);
// });