
var id = setInterval(function () {
    $.ajax({
        type: 'GET',
        url: './get_joycon_L_data'
    }).done(function (res) {
        test(res.L_data);
        console.log(res.L_data);

    })
}, 1000);
// });

// $('#test').click(function () {
//     var val = int($('#test_val').val());
//     test(val);
// });