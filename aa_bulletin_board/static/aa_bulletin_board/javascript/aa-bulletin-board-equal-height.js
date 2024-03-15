$(document).ready(() => {
    'use strict';

    const resizeBulletinCard = () => {
        let highestBox = 0;

        $('.cards-equal-height').each((indexEqualHeight, elementEqualHeight) => {
            $('.card-bulletin-excerpt', elementEqualHeight).each((indexExcerpt, elementExcerpt) => {
                const currentBulletinHeight = $(elementExcerpt).height();

                if (currentBulletinHeight > highestBox) {
                    highestBox = currentBulletinHeight;
                }
            });

            $('.card-bulletin-excerpt', elementEqualHeight).height(highestBox);
        });
    };

    resizeBulletinCard();

    $(window).resize(() => {
        $('.card-bulletin-excerpt').css({'height': ''});

        resizeBulletinCard();
    });

    $('.aa-bulletin-board-marker-group-restrictions').tooltip({
        placement: 'bottom',
        html: true
    });
});
