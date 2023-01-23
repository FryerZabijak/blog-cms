document.querySelectorAll(".edit").forEach((btn) => {
    btn.addEventListener("click", () => {
        article_id = btn.attributes["article-id"].value
        window.location.replace("/admin/article/edit/" + article_id);
    })
})
