
$.ajax({
    type: 'GET',
    url: './get_joycon_L_data'
}).done(function (res) {
    test(res.L_data);
    console.log(res.L_data);
});