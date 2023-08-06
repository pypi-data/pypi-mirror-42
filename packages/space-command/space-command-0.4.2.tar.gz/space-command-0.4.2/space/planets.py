
import sys

from beyond.errors import UnknownBodyError, UnknownFrameError
from beyond.frames import get_frame

import beyond.env.jpl as jpl
import beyond.env.solarsystem as solar
import beyond.utils.ccsds as ccsds

from .clock import Date, timedelta
from .utils import docopt
from .stations import StationDb


def recurse(frame, already, level=""):
    """Function allowing to draw a tree showing relations between the different
    bodies included in the .bsp files
    """

    bodies = list(frame.neighbors.keys())

    txt = ""
    for n in bodies:
        if (frame, n) not in already and (n, frame) not in already:

            if level:
                if n == bodies[-1]:
                    txt += " {}└─ {}\n".format(level[:-2], n.name)
                else:
                    txt += " {}├─ {}\n".format(level[:-2], n.name)
            else:
                txt += "  {}\n".format(n.name)

            already.add((frame, n))
            filler = level + " │ "
            txt += recurse(n, already, filler)

    return txt


def space_planets(*args):
    """Compute position of a planet of the solar system and its major moons

    Usage:
        space-planets
        space-planets fetch
        space-planets <planet>... [options]

    Options:
        fetch                Retrieve .bsp file
        <planet>             Names of the planet to compute the ephemeris of. If
                             absent, list all bodies available
        -f, --frame <frame>  Frame in which to display the ephemeris to
                             [default: EME2000]
        -d, --date <date>    Start date of the ephem (%Y-%m-%d) today at midnight
                             if absent
        -r, --range <days>   Duration of extrapolation in days [default: 3]
        -s, --step <step>    Step size of the ephemeris in min. [default: 60]
        -a, --analytical     Force analytical model instead of .bsp files

    Example:
        space-planets Mars  # Position of Mars in EME2000
        space-planets Moon -f Phobos  # Position of the moon as seen from Phobos

    This command relies on .bsp files, parsed by the incredible jplephem lib.
    Bsp file can be retrived at

        https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/

    Files examples:

        de432s.bsp     Moon, Sun, Mercury, Venus and main bodies barycenters
        mar097.bsp     Mars, Phobos and Deimos
        jup310.bsp     Jupiter and its major moons
        sat360xl.bsp   Saturn and its major moons

    The 'beyond.env.jpl' config variable must be set to a list of bsp files
    paths. See beyond documentation about JPL files:

        http://beyond.readthedocs.io/en/latest/api/env.html#module-beyond.env.jpl

    If no .bsp file is provided, the command falls back to analytical methods
    for Moon and Sun. Other bodies are not provided.
    """

    import requests
    from .config import config
    from logging import getLogger

    log = getLogger(__name__)

    args = docopt(space_planets.__doc__)

    if args['fetch']:

        url = "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/a_old_versions/"

        folder = config.folder / "jpl"

        if not folder.exists():
            folder.mkdir()

        filelist = set(config.get("beyond", "env", "jpl", fallback=[]))

        for file in ['de403_2000-2020.bsp']:

            if not (folder / file).exists():

                log.info("Fetching {}".format(file))
                log.debug(url + file)
                r = requests.get(url + file)

                r.raise_for_status()

                with open(folder / file, "bw") as fp:
                    for chunk in r.iter_content(chunk_size=128):
                        fp.write(chunk)
            else:
                log.info("File {} already downloaded".format(file))

            filelist.add(folder / file)

        log.debug("Adding {} to the list of jpl files".format(file))
        # Adding the file to the list and saving the new state of configuration
        config.set("beyond", "env", "jpl", list(filelist), save=True)
        config.save()

    elif args['<planet>']:

        # Args conversion to proper objects
        if args["--date"]:
            try:
                date = Date.strptime(args['--date'], "%Y-%m-%d")
            except ValueError as e:
                print(e, file=sys.stderr)
                sys.exit(-1)
        else:
            date = Date(Date.now().d)

        try:
            stop = timedelta(float(args['--range']))
            step = timedelta(minutes=float(args['--step']))
        except ValueError as e:
            print(e, file=sys.stderr)
            sys.exit(-1)

        # Create all frames from .bsp files, if they are available
        try:
            jpl.create_frames()
        except jpl.JplError:
            jpl_error = True
        else:
            jpl_error = False

        # Create all frames from stations database
        StationDb.list()

        try:
            frame = get_frame(args['--frame'])
        except UnknownFrameError as e:
            print(e, file=sys.stderr)
            sys.exit(-1)

        # Computation
        ephems = []

        for body_name in args['<planet>']:
            try:
                if args['--analytical'] or jpl_error:
                    body = solar.get_body(body_name).propagate(date)
                else:
                    body = jpl.get_orbit(body_name, date)
            except UnknownBodyError as e:
                print(e, file=sys.stderr)
                sys.exit(-1)

            ephem = body.ephem(start=date, stop=stop, step=step)
            ephem.frame = frame
            ephem.name = body_name
            ephems.append(ephem)
        else:
            print(ccsds.dumps(ephems))
    else:
        print("List of all available bodies")
        try:
            txt = recurse(jpl.Bsp().top, set())
        except jpl.JplError as e:
            print(" Sun")
            print(" Moon")
        else:
            print(txt)
