'use strict';

/**
 * navbar variables
 */

const navOpenBtn = document.querySelector("[data-menu-open-btn]");
const navCloseBtn = document.querySelector("[data-menu-close-btn]");
const navbar = document.querySelector("[data-navbar]");
const overlay = document.querySelector("[data-overlay]");

const navElemArr = [navOpenBtn, navCloseBtn, overlay];

for (let i = 0; i < navElemArr.length; i++) {

  navElemArr[i].addEventListener("click", function () {

    navbar.classList.toggle("active");
    overlay.classList.toggle("active");
    document.body.classList.toggle("active");

  });

}



/**
 * header sticky
 */

const header = document.querySelector("[data-header]");

window.addEventListener("scroll", function () {

  window.scrollY >= 10 ? header.classList.add("active") : header.classList.remove("active");

});



/**
 * go top
 */

const goTopBtn = document.querySelector("[data-go-top]");

window.addEventListener("scroll", function () {

  window.scrollY >= 500 ? goTopBtn.classList.add("active") : goTopBtn.classList.remove("active");

});

function toggleSearch() {
    const searchInput = document.getElementById('search-input');
    searchInput.classList.toggle('active');
}

// Handle search form submission
function submitSearch(event) {
    event.preventDefault();  // Stop default form submission

    const searchQuery = document.getElementById('search-input').value;
    const page = 1;  // Default to page 1 on the first search

    // Redirect to Flask /search route with query and page as GET parameters
    window.location.href = `/search?query=${encodeURIComponent(searchQuery)}&page=${page}`;
}

function Open_new_link(url, new_tab) {
    if (new_tab) {
        window.open(url, "_blank");
    } else {
        window.location.href = url;
    }
}

function setLanguage(language) {
        // Create a new XMLHttpRequest object
        var xhr = new XMLHttpRequest();

        // Configure it: POST-request for the URL /set_language
        xhr.open('POST', '/set_language', true);

        // Set the request header for form data
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

        // Send the request with the selected language
        xhr.send('language=' + language);

        // Optionally, update the "Current Language" text dynamically without reloading the page
        xhr.onload = function() {
            if (xhr.status === 200) {
                window.location.reload();
            }
            else
                (console.log(xhr.responseText));
        };
    }