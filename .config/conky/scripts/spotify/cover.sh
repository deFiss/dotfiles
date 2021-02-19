#!/bin/bash

id_current=$(cat ~/.config/conky/scripts/spotify/current/current.txt)
id_new=`~/.config/conky/scripts/spotify/id.sh`
cover=
imgurl=

if [ "$id_new" != "$id_current" ]; then

	cover=`ls ~/.config/conky/scripts/spotify/covers | grep $id_new`

	if [ "$cover" == "" ]; then

		rm -f ~/.config/conky/scripts/spotify/covers/*
	    imgurl=`~/.config/conky/scripts/spotify/imgurl.sh $id_new`
	    wget -q -O ~/.config/conky/scripts/spotify/covers/$id_new.jpg $imgurl &> /dev/null
		# clean up covers folder, keeping only the latest X amount, in below example it is 10
	    
	    rm -f wget-log #wget-logs are accumulated otherwise
	    cover=`ls ~/.config/conky/scripts/spotify/covers | grep $id_new`
		
	fi

	if [ "$cover" != "" ]; then
		cp ~/.config/conky/scripts/spotify/covers/$cover ~/.config/conky/scripts/spotify/current/current.jpg
	else
		cp ~/.config/conky/scripts/spotify/empty.jpg ~/.config/conky/scripts/spotify/current/current.jpg
	fi

	echo $id_new > ~/.config/conky/scripts/spotify/current/current.txt
fi
