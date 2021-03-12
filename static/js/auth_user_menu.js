function onDocumentClick(event) {
    // Check if the menu is hidden or not.
    var menu = document.querySelector('.auth-user-menu-container .auth-menu')
    var isMenuVisible = !menu.classList.contains('hide')

    // Check if the clicked element is a child of the menu-container.
    var menuContainer = document.querySelector('.auth-user-menu-container');
    if (isMenuVisible && !menuContainer.contains(event.target)) {
        triggerAuthMenuClick();
    }
}

function triggerAuthMenuClick(event) {
    if(event) {
        event.preventDefault();
        event.stopPropagation();
    }

    var menu = document.querySelector('.auth-user-menu-container .auth-menu')
    menu.classList.toggle('hide')

    var icon = document.querySelector('.auth-user-menu-container .arrow')
    icon.classList.toggle('fa-angle-down')
    icon.classList.toggle('fa-angle-up')
}

(function () {
    var authMenuTrigger = document.getElementById('auth-menu-trigger')
    authMenuTrigger.addEventListener('click', triggerAuthMenuClick);

    document.addEventListener('click', onDocumentClick);
})();
