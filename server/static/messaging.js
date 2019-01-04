// Initialize Firebase
var config = {
	apiKey: "AIzaSyCkk7qeZNrqdObznyky_sf3kYrFtOFeCzU",
	authDomain: "asint-project-2018.firebaseapp.com",
	databaseURL: "https://asint-project-2018.firebaseio.com",
	projectId: "asint-project-2018",
	storageBucket: "asint-project-2018.appspot.com",
	messagingSenderId: "645680161332"
};

firebase.initializeApp(config);

//Request permisssion for mesaging
const messaging = firebase.messaging();
messaging.requestPermission()
.then(function() {
	//Got the permission
	console.log('Have permission.');
	
	token = messaging.getToken()
	.then(function(token) {
		var xhttp = new XMLHttpRequest();
		xhttp.onreadystatechange = function(){
	      if (this.readyState == 4 && this.status == 200) {
	      	if(this.responseText == "Not OK"){
	          confirm("Something went wrong sending Message Token!")
	        }
	        else if(this.responseText == "TIMEOUT"){
	          if (confirm("Timeout, press Ok to reload!")) {
	            window.location.replace("/API/Users/Login");
	          } else {
	            window.location.replace("/");
	          }
	        }
	      }
	    };
	    var req = "/API/Users/"+id+"/SetToken?token="+token;
	    xhttp.open("GET",req, true)
	    xhttp.send()
	})
	.catch(function(err){
		console.log('Error Occurred obtaining token.')
	})
})
.catch(function(err) {
	//Denied
	console.log('Error Occurred.');
})

messaging.onMessage(function(payload) {
	var para = document.createElement("p");
	var node1 = document.createTextNode(payload.data.sender);
	var node2 = document.createElement("br")
	var node3 = document.createTextNode('  ->'+payload.data.message);
	para.appendChild(node1);
	para.appendChild(node2);
	para.appendChild(node3);
	var element = document.getElementById("Chat");
	element.appendChild(para);

	console.log('onMessage: ', payload);
});