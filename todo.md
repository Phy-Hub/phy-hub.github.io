*** in my TOC dictionary it does not remove : for label, replace with _ also equations have it eg <div class="math" id="eq:_space-time_interval">
*** my \function finder check at the end didnt find the <br>\section... line also \derivation environment and probly others
*** also \begin{quote} environment
*** clicking on section reference does not load section
*** create check that all internal links have a source
*** bibtex needs same format as latex and link clickability
*** sidenote not on newline this could possible due to blank lines being removed or not registered when rendered, might need \n<br>\n for blank lines

### newly noticed:
- clicking on chapter in toc does not load it the first time (can maybe just sort out the addition of parts first, as it might solve it)

### equations
- on hover over \eqref{} show equation at top or bottom of page, and all variables as side of page
    - use latex equation label as equation divs id
    - have onmousehover have JS show div of eqution using the label/id at top or bottom of page depending on mouse position

things to do:

- using back button in browser won't bring you back to subsection or chapter if it isnt already loaded, and the site address sometimes doesnt referesh its # part at the end
* think of better way for mobile users to get TOC on screen
* make all images have alt text
* automate removal of background colour of tikz svg images
* add names of tikz files to diagrams
* make alt text of svg's the figure's title
* get \figuretitle{} to be title in html
* The angstrom sign is normalized into U+00C5 Å LATIN CAPITAL LETTER A WITH RING ABOVE (HTML entity &Aring;, &#xC5;, or &#197;)
in html chapter heading is smaller than section heading, because chapter header is just in section tag where as section header is in div inside it * (possible answer) i changed font-size of h1 to 2em this might be odd on phones, check
* create checks for math terms and definitions to make sure they are found
* decide weather to make own numbering and reference system so you can load equations on hover
* mathjax seems to make its own div with id, could look into how it does this
* see if there is automatic mathjax resizing for equations that overflow
* use .hide() .show() Instead of manually setting the style attribute with .attr(), in bottom javascript
* chapter 2's sections have same name and div ID as first chapters sections, and the TOC wont go to them when clicked
* if two or more subfigures the caption does not come out correctly
need script to search and replace dictionary words/phrases with hyperlink, if in caption{} will need \protect in front but to work for terms ending * with "s" and "'s"
* several sections named summary


page layout:

* make logo svg ( python script, miniturise, see if gzipping it is possible when being used)
* use it for favicon
* box for suggested changes to material or site, and to point out errors
* sidebar could have references tab


latex:

* format image size and captions
* bibliography
* miniaturise svgs
* appendix
* download button for images and text/latex/pdf options with phy-hub logo
* have all main equations viewable in a sidebar with variables described and equation number, possibly with diagrams, but if too much then new sub page might be needed
* maybe also have a summary page instead
* could have referenced equations/diagrams in sidebar
* if i have 2 subfigures, it only takes first subfigure, want for it to take both
* apostrapies are messed up since now using python to read using ut8 formating
* script part for changing href to <a> tag
* script all text into <p>
* have figures show when hovering on references of figures
* express that time slowing and length contraction not being an optical illsuion, or is it ?
* use bibtex2html for references
* get parser to automatically recognise multi line equations and only show final variable on LHS (last one due to case were equation is rearranged) and equation after last = on RHS and only show this and have expand button to show derivation, which will load full equation into div when clicked and change to revert button that when clicked again reverts (( or possibly for whole derivation including text, this would require flags in the * latex, whether these are just in code of in shown in pdf as well))
* on click of figure ref in html, i want it not to do anything
* parse vairables and replace with function, then need parser to undo this for html with each variable being relateded to func name and then each equation having ref to each fun name included in it, need to later add definitions into all variables

html tips:

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


*************************************************************************
*************************************************************************
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
