document.querySelectorAll(".show").forEach((btn) => {
    btn.addEventListener("click", () => {
        article_id = btn.attributes["article-id"].value
        window.location.replace("/article/" + article_id);
    })
})
