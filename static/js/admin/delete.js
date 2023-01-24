document.querySelectorAll(".delete").forEach((btn) => {
    btn.addEventListener("click", () => {
        article_id = btn.attributes["article-id"].value
        window.location.replace("/admin/article/delete=" + article_id);
    })
})
