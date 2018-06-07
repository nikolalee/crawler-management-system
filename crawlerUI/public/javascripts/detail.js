$(document).ready(function(){
    var menuList = $('#menu');
    //menu animation
    $('#menu').add('#create').mouseout(function(){
        menuList.css('height','0');
    })
    $('#create').add('#menu').mouseover(function(){
        menuList.css('height','162px');
    })
    
})

