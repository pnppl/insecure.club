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
		- enter in sites.rec as site-anim
		- generate static version named site-static.gif

- can we merge the checker with the URL input field on the submit page?

- suddenly after fighting with every browser to access http i'm discovering a bunch of them still load it just fine? wtf? totally undercuts my argument about browser defenses. remove or rework...
^^^^^^^^^^^^^^^^^^^^^

- x i think i wanna delete the sites i added when the clubhouse goes up, feels more clubby
	- easily pruned the recfile (such a good format!!!), but not sure how to deal with the yaml
		- x let's see about switching over to rec as part of the pruning
			- done but kinda uggo
	- ! i would like to keep some of the... honorary inductees around, in a "friends of the site"/"highly recommended" section
		- the byte clubs, wiby, floodgap

- indielogin fallback for rel=me
	- had to set the endpoint to /auth instead of /authorize or i got 405
	- url has to match exactly or you get an error
	- codeberg has stopped working - shows as unsupported on indielogin.com - maybe due to their dns issues earlier

- all logins started failing with the opaque bad session error it returns when you try to complete and some vars are missing. checked out older and older versions and then eventually it just... started working again. it wasn't me. so yeah don't panic, remember the server is a pile of shit
	- happened again. maybe it was the "strict" cookie setting? trying it on lax now
		- think this is working

- login/out errors should display above the h1
	- we should generate the error first, then insert it into the html later
	- for now i just slapped a css class on it
