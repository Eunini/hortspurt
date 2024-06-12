/**  ***************** Beginning of SCRIPT  FOR  SLIDE-IN ANIMATIONS  USING Observer Api   *************  */
 
/***** Beginning Of  Script for Greybox *****/

    // This is the target element
    const targetElement1 = document.querySelector('.greybox');

    // setup the intersection observer
    const observer1 = new IntersectionObserver((entries, observer) => {
       entries.forEach(entry => {
           if (entry.isIntersecting) {
               // add the css class that triggers the animation
               targetElement1.classList.add('animate__animated', 'animate__fadeInLeft');
               
               // stop observing once the animation is triggered
               observer1.unobserve(entry.target);
           }
       });
    }, { threshold: 0.5}); // adjust the threshhold as needed
    
    // start observing the target element
    observer1.observe(targetElement1);
   
/***** End Of Script for Greybox *****/



/***** Beginning Of  Script for Purplebox *****/

    // This is the target element
    const targetElement2 = document.querySelector('.purplebox');

    // setup the intersection observer
    const observer2 = new IntersectionObserver((entries, observer) => {
       entries.forEach(entry => {
           if (entry.isIntersecting) {
               // add the css class that triggers the animation
               targetElement2.classList.add('animate__animated', 'animate__flipInY');
               
               // stop observing once the animation is triggered
               observer2.unobserve(entry.target);
           }
       });
    }, { threshold: 0.5}); // adjust the threshhold as needed
    
    // start observing the target element
    observer2.observe(targetElement2);
   
/***** End Of Script for purplebox *****/



/***** Beginning Of  Script for Greybox2 *****/

    // This is the target element
    const targetElement3 = document.querySelector('.greybox2');

    // setup the intersection observer
    const observer3 = new IntersectionObserver((entries, observer) => {
       entries.forEach(entry => {
           if (entry.isIntersecting) {
               // add the css class that triggers the animation
               targetElement3.classList.add('animate__animated', 'animate__fadeInRight');
               
               // stop observing once the animation is triggered
               observer3.unobserve(entry.target);
           }
       });
    }, { threshold: 0.5}); // adjust the threshhold as needed
    
    // start observing the target element
    observer3.observe(targetElement3);
   
/***** End Of Script for Greybox2 *****/



/***** Beginning Of  Script for ServiceImg *****/

    // This is the target element
    const targetElement4 = document.querySelector('.serviceImg');

    // setup the intersection observer
    const observer4 = new IntersectionObserver((entries, observer) => {
       entries.forEach(entry => {
           if (entry.isIntersecting) {
               // add the css class that triggers the animation
               targetElement4.classList.add('animate__animated', 'animate__slideInDown');
               
               // stop observing once the animation is triggered
               observer4.unobserve(entry.target);
           }
       });
    }, { threshold: 0.5}); // adjust the threshhold as needed
    
    // start observing the target element
    observer4.observe(targetElement4);
   
/***** End Of Script for ServiceImg *****/



/***** Beginning Of  Script for serviceList *****/

    // This is the target element
    const targetElement5 = document.querySelector('.serviceList');

    // setup the intersection observer
    const observer5 = new IntersectionObserver((entries, observer) => {
       entries.forEach(entry => {
           if (entry.isIntersecting) {
               // add the css class that triggers the animation
               targetElement5.classList.add('animate__animated', 'animate__slideInDown');
               
               // stop observing once the animation is triggered
               observer5.unobserve(entry.target);
           }
       });
    }, { threshold: 0.5}); // adjust the threshhold as needed
    
    // start observing the target element
    observer5.observe(targetElement5);
   
/***** End Of Script for ServiceImg *****/





/***** Beginning Of  Script for aboutImg *****/

    // This is the target element
    const targetElement6 = document.querySelector('.aboutImage');

    // setup the intersection observer
    const observer6 = new IntersectionObserver((entries, observer) => {
       entries.forEach(entry => {
           if (entry.isIntersecting) {
               // add the css class that triggers the animation
               targetElement6.classList.add('animate__animated', 'animate__fadeInLeft');
               
               // stop observing once the animation is triggered
               observer6.unobserve(entry.target);
           }
       });
    }, { threshold: 0.5}); // adjust the threshhold as needed
    
    // start observing the target element
    observer6.observe(targetElement6);
   
/***** End Of Script for aboutImg *****/



/***** Beginning Of  Script for footer *****/

    // This is the target element
    const targetElement7 = document.querySelector('.footer');

    // setup the intersection observer
    const observer7 = new IntersectionObserver((entries, observer) => {
       entries.forEach(entry => {
           if (entry.isIntersecting) {
               // add the css class that triggers the animation
               targetElement7.classList.add('animate__animated', 'animate__fadeInRight');
               
               // stop observing once the animation is triggered
               observer7.unobserve(entry.target);
           }
       });
    }, { threshold: 0.5}); // adjust the threshhold as needed
    
    // start observing the target element
    observer7.observe(targetElement7);
   
/***** End Of Script for aboutImg *****/



/***** Beginning Of  Script for up *****/

    // This is the target element
    const targetElement8 = document.querySelector('.mobileServices');

    // setup the intersection observer
    const observer8 = new IntersectionObserver((entries, observer) => {
       entries.forEach(entry => {
           if (entry.isIntersecting) {
               // add the css class that triggers the animation
               targetElement8.classList.add('animate__animated', 'animate__fadeInRight');
               
               // stop observing once the animation is triggered
               observer8.unobserve(entry.target);
           }
       });
    }, { threshold: 0.5}); // adjust the threshhold as needed
    
    // start observing the target element
    observer8.observe(targetElement8);
   
/***** End Of Script for up *****/