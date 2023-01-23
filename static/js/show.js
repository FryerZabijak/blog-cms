document.getElementById("show").addEventListener("click", function(){
    article_id = this.attributes["article-id"].value
    window.location.replace("/article/"+article_id);
});