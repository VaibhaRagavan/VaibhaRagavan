async function dbconnection() {
    const resp = await fetch("/dblinkjs");
    const tag = await resp.json();
    return tag;

}

const resultsbox = document.querySelector(".result-box");
const inputbox = document.getElementById("tags");

dbconnection().then((avtag) => {
    var avaliablekeywords = avtag;
    var avkeywords = avaliablekeywords.flat();
    console.log(avkeywords);
    inputbox.onkeyup = function () {
        let results = [];
        let input = inputbox.value;
        if (input.length){
            results = avkeywords.filter((keyword) => {
                return keyword.toLowerCase().includes(input.toLowerCase());
            });
            
        }
        display(results);
        if (!results.length) {
            resultsbox.innerHTML = " ";
        }

    }
});


function display(results) {
    const content = results.map((list) => {
            return "<li onclick=selected(this) >" + list + "</li>"
        })

    resultsbox.innerHTML = "<ui>" + content.join('') + "</ui>";
    }
function selected(list) {
    inputbox.value = list.innerHTML;
    resultsbox.innerHTML = " ";
}





