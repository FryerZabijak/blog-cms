document.getElementById("save").addEventListener("click", function(event){
    event.preventDefault()
    article_id = this.attributes["article-id"].value
    window.location.replace("/admin/article/edit="+article_id);
});