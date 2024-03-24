

### equations

- [ ] Variables
    - [ ] latex: put all variables in brackets {variable}
    - [ ] latex: put all variables in variable terms file for each chapter
- [ ] python function:
    - [x] parce through variable terms files and place terms and definition in a <dd> inside of a <dl> with id of varibale in {} with prefix of math_term_
        - [ ] get rid of incompatible parts of variable for html id name
    - [ ] have on hover over a variable inside dolalar signs $$ that it shows the variable and definition were it currently shows the word definitions
    - [ ] on hover over equation have all variables in it show on sidebar
        - [ ] have parser create a html/JS list/array of all varibales in the equation
        - [ ] create JS, that for this equation will read the list/array of variables and show each one in the sidebar onmousehover
    - [ ] on hover over \eqref{} show equation at top or bottom of page, and all variables as side of page
        - use latex equation label as equation divs id
        - have onmousehover have JS show div of eqution using the label/id at top or bottom of page
        - have this javascript also do what it did for on equation hover to show variables on sidebar