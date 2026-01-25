

### main content, nagivation + toc:
* when brought to chapter, would be nice to still have Part #num. (without title) greyed out at top

### sidebar:
* have Terms triangle in sidebar rotate on click

### equations + figures:
- make transparent box to fit all subfigures into so all of the set of subfigures are same size
- on hover over \eqref{} show equation at top or bottom of page, and all variables as side of page
    - use latex equation label as equation divs id
    - have onmousehover have JS show div of eqution using the label/id at top or bottom of page depending on mouse position
- see if there is automatic mathjax resizing for equations that overflow
* when hover over actual equation show terms at top or bottom of page * create empty thing to show on hover for now
* onhover of figure ref, have caption show in left sidebar
* get parser to automatically recognise multi line equations ("mini derivations") and only show final variable on LHS (last one due to case were equation is rearranged) and equation after last = on RHS and only show this and have expand button to show derivation, which will load full equation into div when clicked and change to revert button that when clicked again reverts (( or possibly for whole derivation including text, this would require flags in the * latex, whether these are just in code of in shown in pdf as well))

### formating:
* latex sidenotes not on newline this could possible due to blank lines being removed or not registered when rendered, might need \n<br>\n for blank lines
* use .hide() .show() Instead of manually setting the style attribute with .attr(), in bottom javascript
* make logo svg ( python script, miniturise, see if gzipping it is possible when being used)
* script all text into <p>

### css/style:
* use same font size as wikipedia
* maybe have title svg and part by itself with a begin > button * bt need to remove references (possibly only have used refs in parts/chapters load, would need to have extra tag/info on bibs)
* subfigure captions height alinment is off
* next/previous button brings up to book title instead of chapter

### checks:
* check for no duplicate id's

### html tips:
* use em to size relative to parents font size, or rem which is relative to root font size
* this can help get rid of need for media quiery
* can use p { width: clamp(45ch, 50%, 75ch); } to make paragraphs width in content min 45 character length and max 75ch and prefered 50%
* try changing rgb to hls instead for easier clour choices
* create variables for things such as navbar hieght and padding, you set the variable as global with :root { --VarName: value; } and call it using for example height: var(--VarName);
* center divs inside a tag vertically using .ClassName {display: flex; align-items: centre; justify-content: center; } or do it using .ClassName { * display: grid; place-items: center; }
* change scrollbar using ::-webkit-scrollbar (make sure webkit is not just for chrome
* use PostCSS to to make sure css is same throughout different browsers
* use float property instead of grid or flexgrid
* margin: auto centres element blocks vertically and horizontally
* for text, text-align: center;
* put figure counter-reset in the :root { } css and increment it in figure { }
* use <strong instead of <b> for SEO




### latex:
* rats on treadmill (perpendicular rat is meant to retun quicker in diagram)
* need script to search and replace words with hyperlink to definition, if in caption{} will need \protect in front but to work for terms ending * with "s" and "'s"
* Add variable definitions
* format image size and captions
* miniaturise svgs
* appendix
* download button for images and text/latex/pdf options with phy-hub logo/watermark
* have a summary page with main equations
* express that time slowing and length contraction not being an optical illsuion, or is it ?
* posiibly use bibtex2html for references
* \cite{einstein1905electrodynamics} and \cite{SRtestsWiki,SRtestsUniCR} are numbered wrong in latex bibliography
* correct the firgure (Length contraction between three accelerating cars) to have last image to be when light reaches the front car


*************************************************************************
*************************************************************************
things to do (MUCH LATER):
*************************************************************************
*************************************************************************
* box for suggested changes to material or site, and to point out errors
* think of better way for mobile users to get TOC on screen
* make all images have alt text
* automate removal of background colour of tikz svg images
* add names of tikz files to diagrams
* make alt text of svg's the figure's title
* The angstrom sign is normalized into U+00C5 Å LATIN CAPITAL LETTER A WITH RING ABOVE (HTML entity &Aring;, &#xC5;, or &#197;)



writing only:

Styling tex file:

* do not use i.e and e.g. use alternatives
* remove double blank lines
* inforce all snippet formating of latex file
* see about what to do with sentences starting with "this" as you need to remember or return to previous sentences thought to understand it
* diagram captions and headings
* alternatives to the word but
* use script to find latex lines with greatest distance between two full stops
* remove "someone"
* could replace: "relative" with "with respect to" and put into dictionary

pages:

* contact/question page
* about: me, the site plans/goals
* patreon/donate page
* resources page for each topic (video/playlists, books, websites, for different topics and math pages)
* cosmythos story
* 404 and other error pages
* questions and thoughts in physics (with disclaimer)
* page on scientific biases to avoid
* historical journey
* merchandise
* physics overview page
