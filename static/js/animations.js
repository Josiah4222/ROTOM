/**
 * Image Smooth Transitions
 * Handles fade-in effect for images as they load
 */

(function() {
    'use strict';

    // Add js-enabled class to document
    document.documentElement.classList.add('js-enabled');

    /**
     * Add fade-in effect to images as they load
     */
    function initImageFadeIn() {
        const images = document.querySelectorAll('img');
        
        images.forEach(img => {
            // If image is already loaded or is the hero background (which we want to show fast)
            if (img.complete || img.classList.contains('hero-background')) {
                img.classList.add('loaded');
            } else {
                // Add loaded class when image loads
                img.addEventListener('load', function() {
                    this.classList.add('loaded');
                }, { once: true });
                
                // Handle error case
                img.addEventListener('error', function() {
                    this.classList.add('loaded'); // Still show it even if error
                }, { once: true });
            }
        });
    }

    /**
     * Initialize on DOM ready
     */
    function init() {
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', init);
            return;
        }
        
        initImageFadeIn();
        
        // Re-check for dynamically loaded images
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                mutation.addedNodes.forEach(function(node) {
                    if (node.tagName === 'IMG') {
                        if (node.complete) {
                            node.classList.add('loaded');
                        } else {
                            node.addEventListener('load', function() {
                                this.classList.add('loaded');
                            });
                        }
                    } else if (node.querySelectorAll) {
                        const imgs = node.querySelectorAll('img');
                        imgs.forEach(img => {
                            if (img.complete) {
                                img.classList.add('loaded');
                            } else {
                                img.addEventListener('load', function() {
                                    this.classList.add('loaded');
                                });
                            }
                        });
                    }
                });
            });
        });
        
        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    }

    // Start initialization
    init();

})();
