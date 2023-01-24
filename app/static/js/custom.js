document.addEventListener('DOMContentLoaded', function () {
    // tooltips
    const tooltips = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    tooltips.map(function (elem) {
        return new bootstrap.Tooltip(elem)
    })

    // clipboard listeners
    const clipboardButtons = [].slice.call(document.querySelectorAll('.copy-to-clipboard'))
    clipboardButtons.map(function (button) {
        button.addEventListener("click", function (e) {
            let tooltip = bootstrap.Tooltip.getInstance(this);
            tooltip.dispose();
            this.setAttribute('title', 'copied!')
            tooltip = bootstrap.Tooltip.getOrCreateInstance(this);
            tooltip.show();
            navigator.clipboard.writeText(this.getAttribute("data-clipboard"))
        })
    })
}, false);

