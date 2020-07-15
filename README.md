### Leo Dict to Quizlet
Simplify creation of Quizlet flip cards for queried translations of German words.

### TODO:
- [x] Translate the word
  - [x] load translation from Leo Dict
  - [x] render translation as a table
  - [x] implement translation suggestions
  - [ ] rename the translation sections
  - [ ] sort translation sections as in Leo Dict
- [x] Implement the transaltion Term control
  - [x] dock translation control to the bottom of the page
    - [x] made translation table scrollable
- [x] Integrate Google Docs
  - [x] list quiz Docs
  - [x] select quiz Doc
  - [x] create new quiz Doc
  - [x] append translation to the selected quiz Doc
  - [ ] rewrite in javascript (optimization)
- [ ] Improve design
  - [ ] translation control panel on the left side of table?
  - [ ] floating translation control panel?
- [ ] Restructure
  - [ ] Recreate project with new version of `vue cli` and compare generated `package.json`
  - [ ] Separate translation control into different component.