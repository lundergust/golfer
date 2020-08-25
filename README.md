# golfer

This program finds tee times for golf courses in the Minneapolis-St.Paul area.
As of August 24th, 2020, only the following courses are supported on MacOS:
	
	Meadowbrook
	Theodore Wirth
	Hiawatha
	Gross National
	Highland National
	Como Park
	Les Bolstad
	Valleywood
	Chomonix

To run application on MacOS or Linux:

	cd /golfer/macOS/dist  (or)  cd /golfer/linux/dist

	./golfnow/golfnow


Configuration:
	
	(View optional arguments)

	./golfnow/golfnow -h
	./golfnow/golfnow --help
---- 
	
	(To list enabled/disabled courses)

	./golfnow.golfnow -C
	./golfnow/golfnow --config
----

	(To change the number of players)
	
	./golfnow/golfnow -P 3
	./golfnow/golfnow --players 3
----

	(To enable/diabale courses)

	./golfnow/golfnow -E <course id>
	./golfnow/golfnow --enable <course id>

	./golfnow/golfnow -D <course id>
	./golfnow/golfnow --disable <course id>
----
	examples:

	Enable Theodore Wirth
	./golfow/golfnow --enable 1

	Enable only PCC courses
	./golfnow/golfnow --enable pcc

	Disable all courses
	./golfnow/golfnow --disable all

