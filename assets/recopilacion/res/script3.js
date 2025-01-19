// Constants
const RIGHT_ARROW_HEAVY = '&#129090;';
const LEFT_ARROW_HEAVY = '&#129088;';

// Functions
function changeFrame(filePath) {
    const iframe = document.getElementById("page_frame");
    iframe.src = filePath;
}

function toggleSubTree(element) {
    const nextSibling = element.parentElement.nextElementSibling;
    if (nextSibling && nextSibling.tagName === 'UL') {
        nextSibling.classList.toggle('hide');
        element.textContent = element.textContent === '+' ? '-' : '+';
    }
}

function expandAllSubtrees() {
    document.querySelectorAll(".subtree").forEach(subtree => {
        subtree.classList.remove('hide');
        subtree.previousElementSibling.firstChild.textContent = '-';
    });
}

function collapseAllSubtrees() {
    document.querySelectorAll(".subtree").forEach(subtree => {
        subtree.classList.add('hide');
        subtree.previousElementSibling.firstChild.textContent = '+';
    });
}

function toggleTreePanel() {
    const tree = document.querySelector(".tree-panel");
    const toggleBtn = document.getElementById('tree_panel_toggle_btn');
    if (tree.style.display === 'none') {
        tree.style.display = 'inline';
        toggleBtn.innerHTML = LEFT_ARROW_HEAVY;
        toggleBtn.onmouseenter = null;
    } else {
        tree.style.display = 'none';
        toggleBtn.innerHTML = RIGHT_ARROW_HEAVY;
        toggleBtn.onmouseenter = toggleTreePanel;
    }
}

function handleKeypress(ev) {
    if (ev.key === "Escape") {
        toggleTreePanel();
    }
}

function w3_open() {
    document.getElementById("mySidebar").style.display = "block";
    document.getElementById("myOverlay").style.display = "block";
}

function w3_close() {
    document.getElementById("mySidebar").style.display = "none";
    document.getElementById("myOverlay").style.display = "none";
}

// Event Listeners
window.addEventListener('load', () => {
    const showPage = window.location.hash.substr(1);
    if (showPage) {
        changeFrame(showPage);
    }

    document.addEventListener('keydown', handleKeypress);

    const toggleBtn = document.createElement("button");
    toggleBtn.onclick = toggleTreePanel;
    toggleBtn.innerHTML = LEFT_ARROW_HEAVY;
    toggleBtn.id = 'tree_panel_toggle_btn';
    document.querySelector(".two-panels").insertBefore(toggleBtn, document.querySelector(".two-panels").children[1]);
});