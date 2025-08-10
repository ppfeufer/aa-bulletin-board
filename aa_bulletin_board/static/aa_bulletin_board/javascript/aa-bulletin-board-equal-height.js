/* global bootstrap */

$(document).ready(() => {
    'use strict';

    const resizeBulletinCard = () => {
        $('.cards-equal-height').each((_, elementEqualHeight) => {
            let highestBox = 0;
            const excerpts = $('.card-bulletin-excerpt .card', elementEqualHeight);

            excerpts.each((_, elementExcerpt) => {
                highestBox = Math.max(highestBox, $(elementExcerpt).height());
            });

            excerpts.height(highestBox);
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
