// store data
var mylist = (JSON.parse(localStorage.getItem("mybrowsersession")) || [])

// create items
function createItem() {
	var newItem = {text: window.prompt("Enter your item here:") , style:"none"}
	mylist.push(newItem)
	localStorage.setItem("mybrowsersession", JSON.stringify(mylist))
	printItem(newItem)
}

//print items
function printItem(item) {
	var p = document.createElement("p")
	p.innerHTML = item.text
	p.className = item.style
	p.onclick = function(){
		this.className = item.style = (this.className=="none") ? "strike" : "invisible"
		localStorage.setItem("mybrowsersession", JSON.stringify(mylist))
	}
	document.getElementById("myDiv").appendChild(p)
}

//loop and print list
for (x=0;x < mylist.length;x++){
	printItem(mylist[x])
}