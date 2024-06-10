window.addEventListener("load", function() {
    console.log("Hello World");
    document.querySelectorAll(".score").forEach(function(element) {
        let score = Math.floor(element.getAttribute("score"));
        console.log(score);
        let newimg = document.createElement("img");
        
        if (score >= 0 && score < 5) {
            newimg.src = "/static/images/sproutsby_sprites/stage1_open.png"
        } else if (score >=5 && score < 10) {
            newimg.src = "/static/images/sproutsby_sprites/stage2_open.png"
        } else if (score >= 10 && score < 20) { 
            newimg.src = "/static/images/sproutsby_sprites/stage3_open.png"
        } else if (score >= 20 && score < 35) {
            newimg.src = "/static/images/sproutsby_sprites/stage4_open.png" 
        } else if (score >= 35 && score < 50) {
            newimg.src = "/static/images/sproutsby_sprites/stage5_open.png"
        } else if (score >= 50) {
            newimg.src = "/static/images/sproutsby_sprites/dead.png"
        }
        element.appendChild(newimg);
    });
});
