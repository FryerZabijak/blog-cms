document.getElementById("create").addEventListener("click", function(){
    article_id = this.attributes["article-id"].value
    window.location.replace("/admin/article/edit="+article_id);
});