# Plazma-Browser-Pygame

## Plazma Browser is a work in progress!!!

### About

At the moment Plazma Browser can only render text, but the foundations are being laid for a solid renderer.
Once it's fully implemented adding new tags and styles will be extremely easy, especially with a pygame-gui integration.

### Implementation

Plazma Browser uses a sub-repository called STR (Plazma Styled Text Renderer) which handles the render surface.
It is also responsible for the text rendering and styling.

At the moment the browser uses 'Pre-parsing' which converts all text in the html into '<browser_text>' tags.
This allows for easy tracking of text and means that every single element is represented with some sort of tag.

The browser uses 'surface containers' which means that every object has its total rect size and the rect size that is not used.
This allows for elements to be reloaded, moved and scaled instantly without redrawing the whole page.
This can be done due to finding and replacing the portion of the render surface that corresponds to the element your changing's rects, and all element's rects moved depending on the change.

### Installation

1. Download the zip file or clone the repo.
2. Open your terminal in the root directory of the Browser.
3. Clone all submodules including STR: `git submodule update --init --recursive`
4. Install requirements: `pip install -r requirements.txt`
5. Run the browser: `python3 main.py`

### Plans

I have many plans for Plazma Browser, and as you can see from version 1 there are many improvements to the HTML structure, stability and readability of the browser!

At this stage I am dedicated to building a solid foundation for the renderer and making the browser as efficient and portable.

In the future I am looking forward to adding links, images, divs and many more tags + a vast range of styles and basic Javascript.
