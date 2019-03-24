var count = 0;

setInterval(()=>{
	$.getJSON('/count', function(data) {
        console.log(count);
        console.log(data);
		if(count < data['data']) createTables();
	})
}, 5000)

function createTables() {
    $.getJSON('/catch', function(data) {
    //document.getElementById("timeTable").outerHTML = "";
    //document.getElementById("count").outerHTML = "";   
	var timeTable = $('<table></table>').attr({ id: "timeTable" });
    
    var head = $('<tr></tr>').attr({ class: ['head'].join(' ')}).appendTo(timeTable);
		$('<td></td>').text('Time').appendTo(head);
		$('<td></td>').text('Type').appendTo(head);
		$('<td></td>').text('Total people').appendTo(head);	

	count = 0;
	var total_in_room = data[data.length-1][2];
	var trace = {x:[], y:[], name:'TIME', type:'bar'}
    
	$("#timeTable tr").remove();
	$("#count").remove();

	for (var line in data) {
		var row = $('<tr></tr>').attr({ class: "row-class" }).appendTo(timeTable);
			row.appendTo(timeTable)
			$('<td></td>').text(data[line][0]).appendTo(row);
			$('<td></td>').text(data[line][1]).appendTo(row);
			$('<td></td>').text(data[line][2]).appendTo(row);

	        trace.x.push(data[line][0])
            	trace.y.push(data[line][2])

		console.log(data[line]);
		count++;            
        }
    var count1 = $("<h1></h1>").text("Number of people in the room: " + total_in_room).attr({id: 'count'}).appendTo("#table");
	timeTable.appendTo("#table")
		
        // var data = [ trace ];
        // var layout = {barmode: 'group'};
	Plotly.newPlot('myGraph', data, layout, {}, {showSendToCloud: true})
    })
}