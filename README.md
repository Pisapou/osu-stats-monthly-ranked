# osu-stats-monthly-ranked

Program that use osu!'s apiv1 AND apiv2 to generate stats about maps ranked the last month.

## Basic setup

All you need is `python` and the `requests` library *(for more information on the request library, [click here](https://pypi.org/project/requests/))*
*And also an osu! account, but if you don't have one, what are you doing here?*

- Just go grab a **osu!api v1 key** [here](https://osu.ppy.sh/p/api/), and add it to the `line 25`. For more information about osu!api v1, check [the documentation](https://github.com/ppy/osu-api/wiki).
- Grab your **Client ID** and you **Client Secret** by creating your own OAuth Client on your [profile setting](https://osu.ppy.sh/home/account/edit) in [osu.ppy](https://osu.ppy.sh/home), and add them to the `lines 75 and 76`. For more information about osu!api v2, check [the documentation](https://osu.ppy.sh/docs/index.html).

You have done the most complicated! The program works now, you just have to try to understand it *(good luck to you, with a program so coded ;-;)*.

## How to use the programe proprely without understanding it

There are only a few things you need to understand in order to use the code correctly.

- `line 61` : Probably the most important one, is the one that defines since when maps ranked should be counted *(and yes, this program should not only work for months, but also for a decade, however you will be responsible for the performance problems)*. For monthly use, simply put the date of the first of the month you are in the format `YYYY-MM-DD` *(UTC 0)*.
**example:** we are the 29/11/2022, so I put in this variable '2022-11-01'.

- `ls` and `ld` are the 2 main lists *(ls is a list including all sets rank this month in a dictionary, and ld is a list including all difficulties rank this month in a dictionary)*

- You can normally just use the `all_stats(ls,ld)` function for most of the stats *(it's a function that returns the answer of all others, handy isn't it!)*.

- If you want to use the `new_mappers(ld)` function, be aware that a request is sent for each mapper having this month in order to know if it has only one map ranked or not. There are two **major problems**: first of all, the **number of requests** *(indeed, there are too many requests at once, so I imported the time module to limit myself to one mapper request per second. For a list of 200 mappers (which is an average per month), expect a **3min wait**)*, but also the **reliability of the program** *(indeed, the program simply checks if the mapper has only one ranked. If he has ranked his first map and then a second one in the same month, he is not counted as a new ranked mapper. Yes it's a pain, but since the program is not used, I don't have the courage to find a solution)*.

## Conclusion

So this is my first project published on github in python but also my first project using api. So I'm quite aware that in terms of optimization it's really bad, but it works, so it's cool. Feel free to use this as you like but be sure to read up on api's like osu! before you use it so you don't do anything wrong *(especially with the number of requests)*.

On those, see you next time!
