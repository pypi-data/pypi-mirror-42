var __session_storage_available;
var __local_storage_available;

function storageAvailable(type) {
    /* check if session or local storage is available
     *
     * @param type(string): "session" or "storage"
     * @return (boolean): true if requested storage is available
     */
    console.assert(type === 'session' || type === 'storage', "bad storage type (%s)", type);
    const var_name = '__' + type + '_storage_available';
    var available = window[var_name];
    if (available === undefined) {
        // test method from https://developer.mozilla.org/en-US/docs/Web/API/Web_Storage_API/Using_the_Web_Storage_API
        var storage = window[type + 'Storage'];
        try {
            x = '__storage_test__';
            storage.setItem(x, x);
            storage.removeItem(x);
            available = true;
        }
        catch(e) {
            available = e instanceof DOMException && (
                    // everything except Firefox
                    e.code === 22 ||
                    // Firefox
                    e.code === 1014 ||
                    // test name field too, because code might not be present
                    // everything except Firefox
                    e.name === 'QuotaExceededError' ||
                    // Firefox
                    e.name === 'NS_ERROR_DOM_QUOTA_REACHED') &&
                // acknowledge QuotaExceededError only if there's something already stored
                storage.length !== 0;
        }

        if (!available) {
            console.warn("%s storage not available", type);
        }
        window[var_name] = available;
    }

    return available;
}

function toggle_clicked_class_tag(tag_name, class_name='state_clicked') {
    for (let elt of document.getElementsByTagName(tag_name)) {
        elt.classList.toggle(class_name);
    }
}

function toggle_clicked_class_sel(selectors, class_name='state_clicked') {
    for (let elt of document.querySelectorAll(selectors)) {
        elt.classList.toggle(class_name);
    }
}

function set_clicked_class_id(trigger_elem_id, target_elem_id=null, class_name='state_clicked') {
    if (target_elem_id === null) { target_elem_id = trigger_elem_id; }
    document.getElementById(trigger_elem_id).addEventListener(
        "click",
        function() {
            document.getElementById(target_elem_id).classList.toggle(class_name);
        }
    );
}

function tab_select(tab_btn_elt, tab_page_id) {
    for (let elt of document.getElementsByClassName("tab__btn")) {
        if (elt === tab_btn_elt) {
            elt.classList.add('state_clicked');
        }
        else {
            elt.classList.remove('state_clicked');
        }
    }
    let tab_page_elt = document.getElementById(tab_page_id);
    for (let elt of document.getElementsByClassName("tab__page")) {
        if (elt === tab_page_elt) {
            elt.classList.add('state_clicked');
        }
        else {
            elt.classList.remove('state_clicked');
        }
    }
}

function get_elt(arg) {
    if (typeof arg === 'string') {
        // we should have an id
        return document.getElementById(arg);
    }
    else {
        // we should have an element
        return arg;
    }
}

function clicked_cls(elt) {
    /* toggle "state_clicked" class on each click, and remove "state_init" class if present */
    // state_init
    if (elt.classList.contains("state_init")) {
        elt.classList.remove("state_init");
    }

    // clicked
    elt.classList.toggle("state_clicked");
}

function clicked_mh_fix(arg, max_height) {
    /* toggle state_clicked, and fix max-height on transitionend
     *
     * needed to workaround transition issue with max-height:none
     * inspired from https://css-tricks.com/using-css-transitions-auto-dimensions,
     * thanks to Brandon Smith
     *
     * @param arg(string, DOM element): element to toggle (id as string, or element itself)
     * @param max_height(int): maximum height when collapsed (default to clientHeight)
     * */
    elt = get_elt(arg);

    if (!elt.classList.contains("state_clicked")) {
        /* expand */
        let fix_expand = function(event) {
            elt.removeEventListener("transitionend", fix_expand, false);
            if (elt.classList.contains("state_clicked")) {
                /* if event is clicked quicker than transition time,
                 * this callback can be called on reduce */
                elt.style.maxHeight = "none";
            }
        };

        if (!elt.hasAttribute('_max_height_init')) {
            elt.setAttribute('_max_height_init', max_height!==undefined?max_height:elt.clientHeight);
        }
        elt.addEventListener("transitionend", fix_expand, false);
        clicked_cls(elt);
        elt.style.maxHeight = elt.scrollHeight + 'px';

    }
    else {
        /* reduce */
        let transition_save = elt.style.transition;
        elt.style.transition = '';
        requestAnimationFrame(function() {
            elt.style.maxHeight = elt.scrollHeight + 'px';
            elt.style.transition = transition_save;

            requestAnimationFrame(function() {
                elt.style.maxHeight = elt.getAttribute('_max_height_init') + 'px';
            });
        });

        clicked_cls(elt);
    }
}

function createElement(html) {
    /* create a DOM element from raw HTML
     *
     * @param html(string): raw HTML to parse
     * @return: DOM element
     */

    let template = document.createElement('template');
    template.innerHTML = html.trim();
    new_element = template.content.firstChild;
    return new_element;
    }


function fitHeightToContent(elt) {
    /* adapt height to content, specially useful for iframe */
    elt.style.height = elt.contentWindow.document.body.scrollHeight + 80 + 'px';
}
