document.getElementById("create").addEventListener("click", function(){
    article_id = this.attributes["article-id"].value
    window.location.replace("/admin/article/create="+article_id);
});