/* global bootstrap */

$(document).ready(() => {
    'use strict';

    const resizeBulletinCard = () => {
        $('.cards-equal-height').each((_, container) => {
            const excerpts = $('.card-bulletin-excerpt .card', container);
            const maxHeight = Math.max(...excerpts.map((_, el) => $(el).height()).get());

            excerpts.height(maxHeight);
        });
    };

    resizeBulletinCard();

    $(window).resize(() => {
        $('.card-bulletin-excerpt .card').css({'height': ''});

        resizeBulletinCard();
    });

    // Initialize Bootstrap tooltips
    [].slice.call(document.querySelectorAll('[data-bs-tooltip="aa-bulletin-board"]'))
        .map((tooltipTriggerEl) => {
            return new bootstrap.Tooltip(tooltipTriggerEl, {html: true});
        });
});
