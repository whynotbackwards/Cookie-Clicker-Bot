import time
from inputter import Inputter
from gamer import Gamer


inputter = Inputter()

if type(inputter.achievements) == bool:
    gamer = Gamer()
    gamer.load_game()

    if inputter.mute:
        gamer.mute_game()

    gamer.change_name(randomize_name=inputter.random_name, name=inputter.name)

    if not inputter.achievements:
        gamer.close_achievements()

    total_mins = inputter.total_mins
    total_secs = total_mins * 60
    click_secs = inputter.click_secs
    item_limit = inputter.item_limit

    now = time.time()
    time_end = now + total_secs

    while now < time_end:
        gamer.click_cookie(click_secs)
        gamer.buy_upgrade()
        gamer.buy_items(item_limit)
        if not inputter.achievements:
            gamer.close_achievements()
        now = time.time()

    time.sleep(0.1)
    cps = gamer.pull_cps()
    print(f"Final Cookies Per Second After {total_mins} Minute{'s' if total_mins > 1 else ''}: {cps}")
