myclick();

function myclick(){
    console.log("print");
    
    $.getJSON('/catch', function(data) {
            
        for(var line in data){
            console.log(data[line])
            for(var i in data[line])
                console.log(data[line][i]);
        }


        $("#myTable tr").remove();

        var trace = {x:[], y:[], mode: 'lines+markers'}
        myTable = $('<table></table>').attr({ id: "myTable" });
        var brain = $('<tr></tr>').attr({ class: ["class1"].join(' ') }).appendTo(myTable)
        $('<th></th>').text("date/time").appendTo(brain); 
        $('<th></th>').text("C").appendTo(brain); 
        $('<th></th>').text("F").appendTo(brain); 

        for (var line in data) {
            var row = $('<tr></tr>').attr({ class: ["class1"].join(' ') }).appendTo(myTable);
            trace.x.push(data[line][0])

            trace.y.push(data[line][2]);
            for (var i in data[line]) {
                $('<td></td>').text(data[line][i]).appendTo(row); 
            }
                    
        }
        var data = [ trace ];
        var layout = {};
        myTable.appendTo("#box");	 

        Plotly.newPlot('myGraph', data, layout, {showSendToCloud: true});

        console.log(data);
    });
}