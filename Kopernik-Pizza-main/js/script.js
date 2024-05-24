const searchForm = document.querySelector(".search-form");
const searchBtn = document.querySelector("#search-btn");

searchBtn.addEventListener("click",function(){
    searchForm.classList.toggle("active");
});

document.addEventListener("click",function(e)
{
    if(!e.composedPath().includes(searchBtn) && !e.composedPath().includes(searchForm)){
        searchForm.classList.remove("active");
    }
})


const cartItem = document.querySelector(".cart-items-container");
const shoppingBtn = document.querySelector("#shopping-btn");

shoppingBtn.addEventListener("click",function(){
    cartItem.classList.toggle("active");
})


document.addEventListener("click",function(e)
{
    if(!e.composedPath().includes(shoppingBtn) && !e.composedPath().includes(cartItem)){
        cartItem.classList.remove("active");
    }
})

const navbar = document.querySelector(".navbar");
const barBtn = document.querySelector("#bar");

barBtn.addEventListener("click",function(){
    navbar.classList.toggle("active");
})


document.addEventListener("click",function(e){
    if(!e.composedPath().includes(barBtn) &&  !e.composedPath().includes(navbar)){
     navbar.classList.remove("active");
    }
})




