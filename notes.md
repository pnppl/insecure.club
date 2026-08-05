- do i fix up the python or switch to something less absurd? don't really want to write more php, but there are better ways to do static builds
	- i really like the python fstrings for templating. maybe i should just think about the structure and refactor it
		- either use SSI or improve things so i can put headings etc on the submit page and other handcrafted html
		- reduce verbosity/repetition, merge redundant functions
		- get rid of the fish script, i'm sure it's not hard to blank a file in python
- about page/FAQ/why
- better intro/landing page
	- improve nav - need nice submit/random/about not inline links
- 88x31 button and general cutening
	- button must be v cute to lean into the dual meaning of 'insecure' and encourage subs from people who don't use 20 year old browsers like weirdos
	- matching favicon
	- color the category icons so they're easier to tell apart. probably easy with CSS but maybe better to abandon the invert() thing for compatibility reasons. could just be darkmode only for simplicity
	- splash some color around other places
- do a security pass on submit.php so i don't crash the server with giant emails or something
- fish script to check sites with curl (already did this for nagi, just adjust and tidy)
- need to add something to the rules about how sites that are just a resume, list of ways to contact them, or blog with 1 post are not allowed


categories. right now we are mixing up different sorts of categorization which might be confusing. what if a plural site is mostly a/v? do certain categories win or do we separate these and clutter the UI? pretty reasonable if we order them something like this: personal|plural (default) -> social|useful (type) -> historical (type) -> technical|av (content) -> sexual (content)

but then how do we ask users to categorize without confusing them? and what if i add/remove/change a category?

- personal
- plural (multiple contributors)
	- this category sucks
- historical (abandoned site)
- social
- technical
- useful/practical (check the weather, search, etc.)
- audiovisual
	- need better icon
- playful? (games etc)
- sexual
- informational?

better as non-mutually-exclusive tags? how to present it without it being noisy?

personal, plural, and perhaps others are implicitly textual, why not use that instead?

what matters more, the form the content takes or what it actually is of? right now vast swathes of stuff must be subsumed into personal. how would we categorize stuff like 'special interest' sites where the content is purely informational? add that as category?

the cute icons don't matter, stop getting hung up on them
	but they are so cuteeeeee

let's boldface css-optional sites after all. that seems elegant and emphasizes the feature that's most likely to be relevant when you're on a browser that can't ssl. libre annotation can stay as text in the description area. that just leaves the categories/tags to figure out

how about if we let users select multiple categories, then only display the icon for the one that seems most significant, and relegate the rest to the description area? but we also have freeform descriptions

why is this so hard

ok some of these plainly are more like feature flags than categories: historical, a/v, sexual. they're warnings. so is technical, but hopefully it's subtle. it's a double edged sword, makes it easier to avoid but also gives it pride of place. if we're including that, why not other categories? like uh... political, diy, poetry, fiction, etc

categories AND tags? categories: text, a/v, useful, social, playful. tags: personal, plural, historical, technical, sexual, libre
useful, social, playful could all be categoried as interactive
are such broad categories even useful then? we moved everything into the tags
what about: personal, plural, technical, useful, social, playful; historical, sexual, libre, a/v. actually pretty happy with this except it doesn't really have a category for like, a zine or special interest site made by one person, like a non-personal project, and plural still feels janky

much better when i ditch the "-al" affectation and give some examples
- misc: the categorization system has failed
- personal: a homepage, blog, digital garden, or other multi-topic site run by a single person
- creative: a novel, zine, multi-user blog, or other predominantly textual creative work (not necessarily fictional)
- informative: a wiki or other site collecting news or information about a nonfiction subject
- technical: a site predominantly about programming, engineering, hacking, science, etc.
- useful: a service like checking the weather, the homepage of an application, a directory of sites, or another helpful resource
- audiovisual: a site predominantly consisting of photos, videos, or audio
- interactive: a site predominantly consisting of games, toys, or experimental art projects that require the user to do something
- social: a forum, pubnix, imageboard, or other digital community
- sexual: a site predominantly consisting of pornography, erotica, or smut
- historical: a site that has been abandoned for a long time
;
- libre
when in doubt, choose the item lower on the list

so okay not perfect by any means but this way no fucking with tags, more succinct, hopefully works ok

