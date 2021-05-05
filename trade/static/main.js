console.log('JS is attached');

var BNB_rate = new WebSocket("wss://stream.binance.com:9443/ws/bnbusdt@kline_1m");

// Live data (market tile) 

BNB_rate.onmessage = function(event) {

    messageObject = JSON.parse(event.data)

    market_price = parseFloat(messageObject.k.c)
    average_price = parseFloat(document.getElementById('average_price').innerText)

    percentage_p_l = document.getElementById('perc_p_l')
    potential_p_l = document.getElementById('prof_loss')
    document.getElementById('BNB-USD_rate').innerText = market_price
    
    lpm = ((market_price / average_price)*100).toFixed(2)
    if (isNaN(lpm) != true){
        document.getElementById('live_percentage_market').innerText = String(lpm) + '%'
    }
        
    ldc = parseFloat(document.getElementById('spent').innerText) * (market_price / average_price).toFixed(2)
    
    if (isNaN(ldc) != true){
        document.getElementById('live_dollar_change').innerText = String(ldc) + '$'
    }
    
    pot_pl = (market_price - average_price).toFixed(2)
    
    if (isNaN(pot_pl) != true){
        potential_p_l.innerText = pot_pl
    }
    
    perc_pl = (((market_price / average_price) - 1) * 100).toFixed(2)
    
    if (isNaN(perc_pl) != true){
        percentage_p_l.innerText = String(perc_pl) + '%'
    }
    
};



function limit_percentage_change(){
    div0 = document.getElementById('value0').value;
    div1 = document.getElementById('value1').value;
    div2 = document.getElementById('value2').value;
    div3 = document.getElementById('value3').value;
    div4 = document.getElementById('value4').value;
    div5 = document.getElementById('value5').value;
    h3 = document.getElementById('limit_percentage')
    
    average_price = document.getElementById('average_price')
    value = div0 + div1 + div2 + div3 + div4 + div5
    
    ih = ((parseFloat(value) / parseFloat(average_price.innerHTML))*100).toFixed(2)

    if (isNaN(ih) != true){
        h3.innerHTML = String(ih) + '%'
    }

}

function butt1up(){
    div = document.getElementById('value0');
    if (parseInt(div.value) < 10){
        div.value = parseInt(div.value) + 1
    }
    if (parseInt(div.value) == 10){
        div.value = 0
    }
}   
function butt2up(){
    div = document.getElementById('value1');
    if (parseInt(div.value) < 10){
        div.value = parseInt(div.value) + 1
    }
    if (parseInt(div.value) == 10){
        div.value = 0
    }
}
function butt3up(){
    div = document.getElementById('value2');
    if (parseInt(div.value) < 10){
        div.value = parseInt(div.value) + 1
    }
    if (parseInt(div.value) == 10){
        div.value = 0
    }
}
function butt4up(){
    div = document.getElementById('value4');
    if (parseInt(div.value) < 10){
        div.value = parseInt(div.value) + 1
    }
    if (parseInt(div.value) == 10){
        div.value = 0
    }
}
function butt5up(){
    div = document.getElementById('value5');
    if (parseInt(div.value) < 10){
        div.value = parseInt(div.value) + 1
    }
    if (parseInt(div.value) == 10){
        div.value = 0
    }
}


function butt1down(){
    div = document.getElementById('value0');
    if (parseInt(div.value) > -1){
        div.value = parseInt(div.value) - 1
    }
    if (parseInt(div.value) == -1){
        div.value = 9
    }
}
function butt2down(){
    div = document.getElementById('value1');
    if (parseInt(div.value) > -1){
        div.value = parseInt(div.value) - 1
    }
    if (parseInt(div.value) == -1){
        div.value = 9
    }
}
function butt3down(){
    div = document.getElementById('value2');
    if (parseInt(div.value) > -1){
        div.value = parseInt(div.value) - 1
    }
    if (parseInt(div.value) == -1){
        div.value = 9
    }
}
function butt4down(){
    div = document.getElementById('value4');
    if (parseInt(div.value) > -1){
        div.value = parseInt(div.value) - 1
    }
    if (parseInt(div.value) == -1){
        div.value = 9
    }
}
function butt5down(){
    div = document.getElementById('value5');
    if (parseInt(div.value) > -1){
        div.value = parseInt(div.value) - 1
    }
    if (parseInt(div.value) == -1){
        div.value = 9
    } 
}
