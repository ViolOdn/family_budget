$(document).ready(function(){
$('#add1').click(function (e) {
    $('#add_flow_table').show()
})

    $('#reg1').click(function (e) {
       e.preventDefault()
       $.post(
    "check_name",
        {
            'name': $('#name1').val()
        },
    function(response){
        if (response.flag == 1) {
            alert('Данное имя пользователя уже занято')

        }
        }
    );


        if ($('#name1').val().length > 15)
        {
            alert('Имя не должно содержать более 15 символов')
            e.preventDefault()
        }
        if (parseInt(($('#name1').val())))
        {
            alert('Имя не должно состоять из цифр')
            e.preventDefault()
        }

        if ($('#email1').val().indexOf('@') == -1)
        {
            alert('Введите корректный e-mail')
            e.preventDefault()
        }

        if ($('#pass1').val().length < 4)
        {
            alert('Введите пароль более 4 символов')
            e.preventDefault()
        }


})
})



/*
    $('#button1').click(function(e){
    $.post(
    "ajax_path",
        {
        'a': '42'
        },
    function(response){
    alert(response.message)
        }
        );
    })
    */
/*
$('#add1').click(function (e) {
       $.get(
    "add_flow_to_table",
        {

        },
    function(response){
        }
    );

})
*/