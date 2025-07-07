// // Toggle sidebar on mobile
// document.getElementById('mobileMenuButton').addEventListener('click', function() {
//     document.getElementById('sidebar').classList.add('sidebar-mobile-show');
//     document.getElementById('sidebarOverlay').classList.remove('hidden');
// });

// document.getElementById('toggleSidebar').addEventListener('click', function() {
//     document.getElementById('sidebar').classList.remove('sidebar-mobile-show');
//     document.getElementById('sidebarOverlay').classList.add('hidden');
// });

// document.getElementById('sidebarOverlay').addEventListener('click', function() {
//     document.getElementById('sidebar').classList.remove('sidebar-mobile-show');
//     this.classList.add('hidden');
// });

// // Toggle mobile user menu
// document.getElementById('mobileUserMenuButton').addEventListener('click', function() {
//     document.getElementById('mobileUserMenu').classList.remove('hidden');
// });

// Dropdown functionality
document.addEventListener('click', function(e) {
    if (!e.target.matches('.dropdown button')) {
        var dropdowns = document.getElementsByClassName("dropdown-content");
        for (var i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.style.display === 'block') {
                openDropdown.style.display = 'none';
            }
        }
    }
});

var dropdowns = document.querySelectorAll('.dropdown');
dropdowns.forEach(function(dropdown) {
    dropdown.addEventListener('click', function(e) {
        if (e.target.matches('button')) {
            var content = this.querySelector('.dropdown-content');
            if (content.style.display === 'block') {
                content.style.display = 'none';
            } else {
                content.style.display = 'block';
            }
        }
    });
});




// // Toggle sidebar on mobile
// document.getElementById('mobileMenuButton').addEventListener('click', function() {
//     document.getElementById('sidebar').classList.add('sidebar-mobile-show');
//     document.getElementById('sidebarOverlay').classList.remove('hidden');
// });

// document.getElementById('toggleSidebar').addEventListener('click', function() {
//     document.getElementById('sidebar').classList.remove('sidebar-mobile-show');
//     document.getElementById('sidebarOverlay').classList.add('hidden');
// });

// document.getElementById('sidebarOverlay').addEventListener('click', function() {
//     document.getElementById('sidebar').classList.remove('sidebar-mobile-show');
//     this.classList.add('hidden');
// });

// // Toggle mobile user menu
// document.getElementById('mobileUserMenuButton').addEventListener('click', function() {
//     document.getElementById('mobileUserMenu').classList.remove('hidden');
// });

// // Toggle sidebar collapse (original functionality)
// const toggleSidebar = document.getElementById('toggleSidebar');
// const sidebar = document.getElementById('sidebar');
// const mainContent = document.getElementById('mainContent');

// // Only apply this on desktop if needed
// if (window.innerWidth >= 1024) {
//     toggleSidebar.addEventListener('click', () => {
//         sidebar.classList.toggle('sidebar-collapsed');
//         mainContent.classList.toggle('main-content-expanded');
//         mainContent.classList.toggle('ml-64');
//     });
// }

// // Handle window resize
// window.addEventListener('resize', function() {
//     if (window.innerWidth >= 1024) {
//         document.getElementById('sidebar').classList.remove('sidebar-mobile-show');
//         document.getElementById('sidebarOverlay').classList.add('hidden');
//     }
// });



// static/js/ScriptAdmin.js
document.addEventListener('DOMContentLoaded', function() {
    // Gestion du menu mobile
    const mobileMenuButton = document.getElementById('mobileMenuButton');
    const sidebar = document.getElementById('sidebar');
    const sidebarOverlay = document.getElementById('sidebarOverlay');
    const toggleSidebar = document.getElementById('toggleSidebar');
    
    if (mobileMenuButton && sidebar) {
        mobileMenuButton.addEventListener('click', function() {
            sidebar.classList.toggle('sidebar-mobile-show');
            sidebarOverlay.classList.toggle('hidden');
        });
    }
    
    if (toggleSidebar && sidebar) {
        toggleSidebar.addEventListener('click', function() {
            sidebar.classList.toggle('sidebar-mobile-show');
            sidebarOverlay.classList.toggle('hidden');
        });
    }
    
    if (sidebarOverlay) {
        sidebarOverlay.addEventListener('click', function() {
            sidebar.classList.remove('sidebar-mobile-show');
            sidebarOverlay.classList.add('hidden');
        });
    }
    
    // Gestion du menu utilisateur mobile
    const mobileUserMenuButton = document.getElementById('mobileUserMenuButton');
    const mobileUserMenu = document.getElementById('mobileUserMenu');
    
    if (mobileUserMenuButton && mobileUserMenu) {
        mobileUserMenuButton.addEventListener('click', function() {
            mobileUserMenu.classList.toggle('hidden');
        });
    }
    
    // Gestion du toggle du sidebar (version desktop)
    const desktopToggleSidebar = document.getElementById('desktopToggleSidebar');
    if (desktopToggleSidebar) {
        desktopToggleSidebar.addEventListener('click', function() {
            sidebar.classList.toggle('sidebar-collapsed');
            document.getElementById('mainContent').classList.toggle('main-content-expanded');
        });
    }
});