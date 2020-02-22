// calender json read
	localStorage.setItem("firstname", "");

var myobj = JSON.parse(data);

var today = new Date();
var tableData = '';

        for (var i = 0; i < myobj.length; i++){
         /* if (myobj[i].cust == 'EliLily') {                      */

              var CurDate = myobj[i].intdt;
              var CDate = new Date(CurDate);	

              if (CurDate == '2020-03-07') {
                
                tableData += '<tr>'; 

                 tableData += '<td>';
                 tableData += myobj[i].cd;
                 tableData += '</td>';
                  /*if (myobj[i].provider == null || myobj[i].provider == undefined || myobj[i].provider == 'select') {
                    tableData += '<td>';
                    tableData += "";
                    tableData += '</td>';
                  }else{*/
                  tableData += '<td>';
				  tableData += '<center>';
                  tableData += myobj[i].scheduler;
				  tableData += '<center>';
                  tableData += '</td>';   
				  tableData += '<td>';
				  tableData += '<center>';
                  tableData += myobj[i].skill;
				  tableData += '<center>';
                  tableData += '</td>'; 				  
                  /*tableData += '<td>';
				  tableData += '<center>';
                  tableData += myobj[i].age;
				  tableData += '<center>';
                  tableData += '</td>';*/
                  tableData += '<td>';
				  tableData += '<center>';
                  tableData += myobj[i].gender;
				  tableData += '<center>';
                  tableData += '</td>';
                  tableData += '<td>';
				  tableData += '<center>';
                  tableData += myobj[i].phone;
				  tableData += '<center>';
                  tableData += '</td>';
                  tableData += '<td>';
				  tableData += '<center>';
                  tableData += myobj[i].jobloc;
				  tableData += '<center>';
                  tableData += '</td>';
                  tableData += '<td>';
				  tableData += '<center>';
                  tableData += myobj[i].natloc;
				  tableData += '<center>';
                  tableData += '</td>';
                  tableData += '<td>';
				  tableData += '<center>';
                  tableData += myobj[i].scdt;
				  tableData += '<center>';
                  tableData += '</td>';
                  tableData += '<td>';
				  tableData += '<center>';
                  tableData += myobj[i].intdt;
				  tableData += '<center>';
                  tableData += '</td>';        
                  /*tableData += '<td>';
				  tableData += '<center>';
                  tableData += myobj[i].last_reminder
				  tableData += '<center>';
                  tableData += '</td>';*/
				  if (myobj[i].Confirmed == "1") {
                    tableData += '<td>';
					tableData += '<center>';
                    tableData += "Yes";
					tableData += '<center>';
                    tableData += '</td>';
                  }else{
                    tableData += '<td>';
					tableData += '<center>';
                    tableData += 'No';
					tableData += '<center>';
                    tableData += '</td>';
                  } 
                            
                  if (myobj[i].pred > 50) {
                    tableData += '<td style="color: green;">';
					tableData += '<center>';
                    tableData += myobj[i].pred;
					tableData += '<center>';
                    tableData += '</td>';
                  }else{					  
                    tableData += '<td style="color: red;">';
					tableData += '<center>';
                    tableData += myobj[i].pred;
					tableData += '<center>';
                    tableData += '</td>';
                  }      
				  if (myobj[i].pred < 50) {
                  tableData += '<td>';
                  tableData += myobj[i].insight;
                  tableData += '</td>';
				  }else{
				  tableData += '<td>';
                  tableData += '';
                  tableData += '</td>';
				  }
                  tableData += '<td>';
                  tableData += '<a href="#">SMS</a><br><a href="#">Call</a><br><a onclick="getId(this)" href="appointment">Reschedule</a>';
                  tableData += '</td>';

                tableData += '</tr>';
              }              
			      
        }
        document.getElementById('tableData').innerHTML = tableData;

    var candidateName = '';
    function  getId(element) {
        var rowNum = element.parentNode.parentNode.rowIndex - 1;
        candidateName = document.getElementById("tableData").rows[rowNum].cells[0].innerHTML;
        localStorage.setItem("firstname", candidateName);
    }

    /* var globalVariable={
       x: patientName
    };*/
