document.getElementById("delete").addEventListener("click", function(){
    article_id = this.attributes["article-id"].value
    window.location.replace("/admin/article/delete="+article_id);
});