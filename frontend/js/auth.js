/**
 * Cartoonify - Authentication JS
 * Handles JWT authentication, route protection, and API helpers
 */


/* ------------------------------------------------
   Require Authentication
------------------------------------------------ */

function requireAuth() {

    const token = localStorage.getItem("cartoonify_token")

    if (!token) {

        window.location.href = "/login.html"
        return false

    }

    try {

        const payload = JSON.parse(atob(token.split(".")[1]))

        if (payload.exp && payload.exp * 1000 < Date.now()) {

            localStorage.removeItem("cartoonify_token")
            localStorage.removeItem("cartoonify_user")

            window.location.href = "/login.html?expired=1"
            return false

        }

    } catch {

        localStorage.removeItem("cartoonify_token")
        window.location.href = "/login.html"
        return false

    }

    return true

}


/* ------------------------------------------------
   Token Helpers
------------------------------------------------ */

function getToken() {
    return localStorage.getItem("cartoonify_token")
}

function getCachedUser() {

    try {
        return JSON.parse(localStorage.getItem("cartoonify_user"))
    } catch {
        return null
    }

}


/* ------------------------------------------------
   Logout
------------------------------------------------ */

function logout() {

    localStorage.removeItem("cartoonify_token")
    localStorage.removeItem("cartoonify_user")

    window.location.href = "/login.html"

}


/* ------------------------------------------------
   API Helpers
------------------------------------------------ */

async function apiGet(url) {

    const token = getToken()

    const res = await fetch(url, {
        headers: {
            "Authorization": "Bearer " + token
        }
    })

    return await res.json()

}


async function apiPost(url, data) {

    const token = getToken()

    const res = await fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token
        },
        body: JSON.stringify(data)
    })

    return await res.json()

}


async function apiDelete(url) {

    const token = getToken()

    const res = await fetch(url, {
        method: "DELETE",
        headers: {
            "Authorization": "Bearer " + token
        }
    })

    return await res.json()

}


/* ------------------------------------------------
   Sidebar User Loader
------------------------------------------------ */

function loadSidebarUser() {

    const user = getCachedUser()

    if (!user) return

    const nameEl = document.getElementById("sidebarUserName")
    const avatarEl = document.getElementById("sidebarAvatar")

    if (nameEl) {
        nameEl.textContent = user.name
    }

    if (avatarEl) {

        avatarEl.src =
            "https://ui-avatars.com/api/?name=" +
            encodeURIComponent(user.name) +
            "&background=7c3aed&color=fff"

    }

}


/* ------------------------------------------------
   Google OAuth Redirect Handler
------------------------------------------------ */

(function () {

    const params = new URLSearchParams(window.location.search)
    const token = params.get("token")

    if (token) {

        localStorage.setItem("cartoonify_token", token)

        history.replaceState({}, document.title, window.location.pathname)

    }

})()


/* ------------------------------------------------
   jQuery AJAX Global Auth
------------------------------------------------ */

if (typeof $ !== "undefined") {

    $.ajaxSetup({

        beforeSend: function (xhr) {

            const token = getToken()

            if (token) {
                xhr.setRequestHeader("Authorization", "Bearer " + token)
            }

        },

        error: function (xhr) {

            if (xhr.status === 401 || xhr.status === 403) {

                localStorage.removeItem("cartoonify_token")
                localStorage.removeItem("cartoonify_user")

                window.location.href = "/login.html"

            }

        }

    })

}


/* ------------------------------------------------
   Sidebar Toggle
------------------------------------------------ */

function toggleSidebar() {
    const sidebar = document.getElementById("sidebar")
    sidebar.classList.toggle("open")
}