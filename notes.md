- do i fix up the python or switch to something less absurd? don't really want to write more php, but there are better ways to do static builds
	- i really like the python fstrings for templating tho. maybe i should just think about the structure and refactor it
		- either use SSI or improve things so i can put headings etc on the submit page and other handcrafted html
		- reduce verbosity/repetition, merge redundant functions
- color the category icons so they're easier to tell apart. probably easy with CSS but maybe better to abandon the invert() thing for compatibility reasons. could just be darkmode only for simplicity
- fish script to check sites with curl (already did this for nagi, just adjust and tidy)
- TOC for categories page? CSS category filtering on all pages?

- added animated/static button feature with prefers-reduced-motion support using some ridiculous CSS
	- for animated buttons
		- name them site-anim.gif
		- enter in site.yaml as site-anim
		- generate static version named site-static.gif

- can we merge the checker with the URL input field on the submit page?

- suddenly after fighting with every browser to access http i'm discovering a bunch of them still load it just fine? wtf? totally undercuts my argument about browser defenses. remove or rework...
^^^^^^^^^^^^^^^^^^^^^

- i think i wanna delete the sites i added when the clubhouse goes up, feels more clubby

- clubhouse: need to add indielogin fallback, preferably in a way that leaves the upstream source code alone
	- which we either need to vendor or change way the automatic git deploy works
	- ok i thought i had this working but actually no. need to debug the fallback
		- getting 405
		- independently, codeberg has stopped working - shows as unsupported on indielogin.com - maybe due to their dns issues earlier
