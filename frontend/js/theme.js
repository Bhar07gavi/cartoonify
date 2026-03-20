/* ===============================
   Cartoonify Theme Toggle
================================ */

function applySavedTheme() {

    const saved = localStorage.getItem("cartoonify_theme")

    if (saved === "light") {
        document.body.classList.add("light-theme")
        updateIcon()
    }

}

function toggleTheme() {

    document.body.classList.toggle("light-theme")

    if (document.body.classList.contains("light-theme")) {
        localStorage.setItem("cartoonify_theme", "light")
    } else {
        localStorage.setItem("cartoonify_theme", "dark")
    }

    updateIcon()

}

function updateIcon() {

    const icon = document.querySelector("#themeToggle i")

    if (!icon) return

    if (document.body.classList.contains("light-theme")) {
        icon.className = "bi bi-sun"
    } else {
        icon.className = "bi bi-moon"
    }

}


/* WAIT FOR PAGE LOAD */

window.addEventListener("load", function () {

    applySavedTheme()

    const toggleBtn = document.getElementById("themeToggle")

    if (toggleBtn) {
        toggleBtn.addEventListener("click", toggleTheme)
    }

})