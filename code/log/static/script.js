myFunction();

function myFunction(){
    $.getJSON('/fetch', function(data) {
            
        $('#basicTable').remove()
    
        mytable = $('<table></table>').attr({ id: "basicTable" });
        var head = $('<tr></tr>').attr({ class: ["class1"].join(' ') }).appendTo(mytable)
        $('<th></th>').text("date/time").appendTo(head); 
        $('<th></th>').text("C").appendTo(head); 
        $('<th></th>').text("F").appendTo(head); 

        var trace = {x:[], y:[], mode: 'lines+markers'}

        for (var line in data) {
            var row = $('<tr></tr>').attr({ class: ["class1"].join(' ') }).appendTo(mytable);
            trace.x.push(data[line][0])
            
            trace.y.push(data[line][1]);
            for (var i in data[line]) {
                $('<td></td>').text(data[line][i]).appendTo(row); 
            }
                    
        }
          var data = [ trace ];
          
          var layout = {};
          
          Plotly.newPlot('myDiv', data, layout, {showSendToCloud: true});
        
        mytable.appendTo("#box");	 


    });
}