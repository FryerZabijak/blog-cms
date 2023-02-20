const likebtn = document.querySelector("[btn-type=like]");
const dislikebtn = document.querySelector("[btn-type=dislike]");
const finalratingel = document.getElementById("final-rating");
let finalratingnum = Number(finalratingel.innerHTML);
const ratingUrl = window.location.href.concat("/rating");

likebtn.addEventListener("click",() => {
    console.log("dal si like");
    fetch(ratingUrl, {
        method:"POST",
        body:JSON.stringify({rating:1}),
        headers:{
            "Content-Type":"application/json"
        }
    }).then(response => {
        location.reload();
    })
    .catch(error => {
        console.log(error);
        alert("Byl zde problém s uložením vašeho hodnocení");
    })
})

dislikebtn.addEventListener("click",() => {
    console.log("dal si dislike");
    fetch(ratingUrl, {
        method:"POST",
        body:JSON.stringify({rating:-1}),
        headers:{
            "Content-Type":"application/json"
        }
    }).then(response => {
        location.reload();
    })
    .catch(error => {
        console.log(error);
        alert("Byl zde problém s uložením vašeho hodnocení");
    })
})