function scrape() {
    // Elements
    let spinner = document.getElementById("spinner");
    let url = document.getElementById("url").value;
    let term = document.getElementById("term").value;
    
    console.log(term, url)
    // Display spinner
    spinner.style.display = "block"

    fetch(`http://localhost:8080/scrape/${term}?url=${url}`)
    .then((response) => {
        readFromReader( response.body.getReader(), spinner)
    })
}

function addToResults(result){
    let formattedObj = formatResult(result);
    if(formattedObj.results && formattedObj.href){
        var parent = document.getElementById('logParent');
        var li = document.createElement('li');
    
        li.innerHTML = "Link: " + formattedObj.href + " results: " + formattedObj.results + " time: " + formattedObj.time;
        parent.appendChild(li);
    }
}

function readFromReader(reader, spinner){
    reader.read().then((response)=>{
        if(!response.done){
            addToResults(String.fromCharCode(...response.value))
            readFromReader(reader, spinner)
        }
        else
            spinner.style.display = "none"
    })
}

function formatResult(result){
    let stripped = result.replace(/\}|\{|\'|\"/g, '').trim(); //Strip out ending brackets
    const vals = stripped.split(',');
    obj = {}
    for(let i in vals){
        if(vals[i].includes('href: '))
            obj.href =  vals[i].split("href: ")[1].trim()
        if(vals[i].includes('time: '))
            obj.time =  vals[i].split("time: ")[1].trim()
        if(vals[i].includes('results: '))
            obj.results =  vals[i].split("results: ")[1].trim().replace(/\[|\]/g, '').split(",")
    }
    return obj
}