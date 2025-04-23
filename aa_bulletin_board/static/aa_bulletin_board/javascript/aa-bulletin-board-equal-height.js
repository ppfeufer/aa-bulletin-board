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

    $('.aa-bulletin-board-marker-group-restrictions').tooltip({
        placement: 'bottom',
        html: true
    });
});
