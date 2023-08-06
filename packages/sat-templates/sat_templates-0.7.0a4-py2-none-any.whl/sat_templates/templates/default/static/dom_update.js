/* This script check for well-known DOM element to modify when javascript is enabled */

const EXPAND_LIMIT = 250; // max height before expanding is needed, in pixels
const MAGIC_CLASSES = {
    "box--expand": "handleBoxExpand"};


function addExpandListeners(elt, expand_elt, reduce_elt) {
    let on_click = function(){
        clicked_mh_fix(elt);
    };
    expand_elt.addEventListener('click', on_click, false);
    reduce_elt.addEventListener('click', on_click, false);
}

function handleBoxExpand(box_elt) {
    /* Add expand zone elements if box height is > EXPAND_LIMIT
     *
     * Those zone will expand/reduce the box when clicked
     * @param box_elt(DOM element): element with box--expand class
     */
    let content_elt = box_elt.getElementsByClassName("box__content")[0];

    if (content_elt === undefined) {
        return;
    }

    if (content_elt.offsetHeight > EXPAND_LIMIT) {
        /* top expand box */
        let reduce_elt = document.createElement("div");
        reduce_elt.className = "box__expand_zone box__expand_zone--top show_if_parent_clicked";
        let p_elt = document.createElement("p");
        p_elt.textContent = reduce_txt;
        reduce_elt.appendChild(p_elt);
        box_elt.insertBefore(reduce_elt, box_elt.firstChild);

        /* bottom expand box */
        let expand_elt = document.createElement("div");
        expand_elt.className = "box__expand_zone box__expand_zone--bottom";
        let p_elt_clicked = document.createElement("p");
        p_elt_clicked.textContent = expand_txt;
        p_elt_clicked.className = "show_if_grandparent_not_clicked";
        let p_elt_not_clicked = document.createElement("p");
        p_elt_not_clicked.textContent = reduce_txt;
        p_elt_not_clicked.className = "show_if_grandparent_clicked";
        expand_elt.appendChild(p_elt_clicked);
        expand_elt.appendChild(p_elt_not_clicked);
        box_elt.appendChild(expand_elt);

        addExpandListeners(box_elt, expand_elt, reduce_elt);
    }
}


function handleStateInit(elt) {
    /* Add a click listener which remove state_init
     *
     * The listener will call magic classes handlers when suitable
     * @param elt(DOM element): element with state_init class
     */
    function onClick() {
        elt.removeEventListener('click', onClick, false);
        elt.classList.remove("state_init");

        for (let [className, funcName] of Object.entries(MAGIC_CLASSES)){
            if (elt.classList.contains(className)) {
                window[funcName](elt);
            }
        }
    }
    elt.addEventListener('click', onClick, false);
}

// we first have to handle "state_init"
for (let elt of document.getElementsByClassName("state_init")) {
    handleStateInit(elt);
}

// we then launch every handler where "state_init" is not set
// "state_init" handler will launch the handlers itself on first click
for (let [className, funcName] of Object.entries(MAGIC_CLASSES)){
    for (let box_elt of document.getElementsByClassName(className)) {
        if (!box_elt.classList.contains("state_init")) {
            window[funcName](box_elt);
        }
    }
}
