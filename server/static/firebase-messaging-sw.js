importScripts('https://www.gstatic.com/firebasejs/5.7.2/firebase-app.js')
importScripts('https://www.gstatic.com/firebasejs/5.7.2/firebase-messaging.js')

var config = {
apiKey: "AIzaSyCkk7qeZNrqdObznyky_sf3kYrFtOFeCzU",
authDomain: "asint-project-2018.firebaseapp.com",
databaseURL: "https://asint-project-2018.firebaseio.com",
projectId: "asint-project-2018",
storageBucket: "asint-project-2018.appspot.com",
messagingSenderId: "645680161332"
};

firebase.initializeApp(config);

const messaging = firebase.messaging();

messaging.setBackgroundMessageHandler(function(payload) {
	const title = 'Message Received';
	const options = {
		body: payload.data.message
	};
	return self.registration.showNotification(title, options);
});