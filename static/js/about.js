async function getFact(){
    fetch('https://uselessfacts.jsph.pl/random.json?language=en')
    .then(res => res.json())
    .then(data => document.getElementById("random_fact").textContent = data.text) 
 }
 getFact()
 var intervalId = window.setInterval(function(){
 getFact()
 }, 9000); 