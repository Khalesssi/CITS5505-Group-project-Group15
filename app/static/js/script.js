// Article Carousel Setup


// Select all carousel items within the article section
let article_carousel_items = document.querySelectorAll('.article-carousel .carousel-item')

// Loop through each carousel item
article_carousel_items.forEach((el) => {
    const minPerSlide = 3 // Minimum number of items visible per slide
    let next = el.nextElementSibling

    // Clone next items to fill up the slide to the minimum count
    for (var i=1; i<minPerSlide; i++) {
        if (!next) {
            // If there's no next element, loop back to the first item (wrap around)
        	next = article_carousel_items[0]
      	}

        // Clone the next item (shallow clone) and append its first child to the current slide
        let cloneChild = next.cloneNode(true)
        el.appendChild(cloneChild.children[0])
        
        // Move to the next sibling in the carousel
        next = next.nextElementSibling
    }
})