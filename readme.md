This executable finds tee times for golf courses in the Minneapolis-St.Paul area.
As of August 24th, 2020, only the following courses are supported:
	
	Meadowbrook
	Theodore Wirth
	Hiawatha
	Gross National
	Highland National
	Como Park
	Les Bolstad

To run application:

	cd /golfer/dist

	./golfnow/golfnow


Configuration:

	(To list enabled/disabled courses)

	./golfnow/golfnow --config
----

	(To enable/disbale courses)
	./golfnow/golfnow --enable <course id>
	./golfnow/golfnow --disable <course id>
----
	examples:

	Enable Theodore Wirth
	./golfow/golfnow --enable 1

	Enable only PCC courses
	./golfnow/golfnow --enable pcc

	Disable all courses
	./golfnow/golfnow --disable all

