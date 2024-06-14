 /**  *****************Beginning Of SCRIPT  FOR DATA DEALS SLIDER  *************  */
 
 /* Card Slider - Swiper */
 var cardSlider = new Swiper('.card-slider', {
    autoplay: {
        delay: 4000,
        disableOnInteraction: false
    },

    pagination: {
       el: '.swiper-pagination',
    },

    loop: true,
    navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev'
    },
    slidesPerView: 4,
    spaceBetween: 40,
    breakpoints: {
        // when window is <= 767px
        767: {
            slidesPerView: 1,
            spaceBetween: 20,
        },
        // when window is <= 991px
        991: {
            slidesPerView: 2,
            spaceBetween: 40
        }
    }
});
 /**  ***************** END OF  SCRIPT  FOR DATA DEALS SLIDER  *************  */