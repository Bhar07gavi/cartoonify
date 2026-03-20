/**
 * Cartoonify - Editor JS
 * Before/After draggable comparison slider
 */

function initComparisonSlider(wrapId = "comparisonContainer") {

    const wrapEl =
        typeof wrapId === "string"
            ? document.getElementById(wrapId)
            : wrapId

    if (!wrapEl) return

    const innerWrap =
        wrapEl.querySelector(".comparison-slider-wrap") || wrapEl

    const before = innerWrap.querySelector(".comp-before")
    const after = innerWrap.querySelector(".comp-after")
    const slider = innerWrap.querySelector(".comp-slider")

    if (!before || !after || !slider) return


    /* ─────────────────────────────────────────
       Set slider container height
    ───────────────────────────────────────── */

    function setHeight() {

        const width = innerWrap.offsetWidth

        innerWrap.style.height = Math.round(width * 0.6) + "px"

    }

    setHeight()

    window.addEventListener("resize", setHeight)


    /* ─────────────────────────────────────────
       Slider Movement Logic
    ───────────────────────────────────────── */

    let dragging = false

    function move(clientX) {

        const rect = innerWrap.getBoundingClientRect()

        let percent =
            ((clientX - rect.left) / rect.width) * 100

        percent = Math.max(0, Math.min(100, percent))

        slider.style.left = percent + "%"

        before.style.clipPath = `inset(0 ${100 - percent}% 0 0)`
        after.style.clipPath = `inset(0 0 0 ${percent}%)`

    }


    /* ─────────────────────────────────────────
       Mouse Events
    ───────────────────────────────────────── */

    innerWrap.addEventListener("mousedown", e => {

        dragging = true
        move(e.clientX)

        e.preventDefault()

    })

    document.addEventListener("mousemove", e => {

        if (dragging) move(e.clientX)

    })

    document.addEventListener("mouseup", () => {

        dragging = false

    })


    /* ─────────────────────────────────────────
       Touch Events
    ───────────────────────────────────────── */

    innerWrap.addEventListener("touchstart", e => {

        dragging = true
        move(e.touches[0].clientX)

    }, { passive: true })

    document.addEventListener("touchmove", e => {

        if (dragging) move(e.touches[0].clientX)

    }, { passive: true })

    document.addEventListener("touchend", () => {

        dragging = false

    })


    /* ─────────────────────────────────────────
       Start slider at center
    ───────────────────────────────────────── */

    function initCenter() {

        const rect = innerWrap.getBoundingClientRect()

        move(rect.left + rect.width / 2)

    }

    // wait until images load
    setTimeout(initCenter, 100)

}