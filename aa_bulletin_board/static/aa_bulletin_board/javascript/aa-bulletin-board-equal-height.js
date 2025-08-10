/* global bootstrap */

$(document).ready(() => {
    'use strict';

    /**
     * Resize bulletin card excerpts to equal height.
     *
     * This function calculates the maximum height of all bulletin card excerpts
     * and sets that height to all excerpts within the same container.
     * It is designed to ensure that all bulletin cards have the same height,
     * which is particularly useful for responsive designs where card heights may vary.
     *
     * The function is debounced to improve performance during window resize events.
     */
    const resizeBulletinCard = () => {
        $('.cards-equal-height').each((_, container) => {
            const excerpts = $('.card-bulletin-excerpt .card', container);
            const maxHeight = Math.max(...excerpts.map((_, el) => $(el).height()).get());

            excerpts.height(maxHeight);
        });
    };

    /**
     * Debounce function to limit the rate at which a function can fire.
     * This is useful for performance optimization, especially during events like window resizing.
     * It ensures that the function is not called too frequently, which can lead to performance issues
     * by accumulating calls and executing only after a specified wait time.
     *
     * @param {Function} func The function to debounce.
     * @param {int} wait The number of milliseconds to wait before calling the function.
     * @returns {(function(...[*]): void)|*} A debounced version of the function that will only execute after the specified wait time has passed since the last call.
     */
    const debounce = (func, wait) => {
        let timeout;

        return (...args) => {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };

            clearTimeout(timeout);

            timeout = setTimeout(later, wait);
        };
    };

    resizeBulletinCard();

    $(window).resize(debounce(resizeBulletinCard, 250));

    // Initialize Bootstrap tooltips
    [].slice.call(document.querySelectorAll('[data-bs-tooltip="aa-bulletin-board"]'))
        .map((tooltipTriggerEl) => {
            return new bootstrap.Tooltip(tooltipTriggerEl, {html: true});
        });
});
