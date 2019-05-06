# athena

**athena** is an elegant, minimalist, simple static blog generator
written in Python. It is based on Flask, Pandoc, and Tufte CSS.

![athena screenshot](/static/athena.png)

You can browse the [live demo here][demo].

## Why athena?

Because it's a simple, yet aesthetically pure, static blog generator with
paramount focus on the reading experience. As a WordPress user since 2007, I
think it's time for a change. Other static blog generators are too feature
heavy and bloated. athena just works.

### Why Tufte CSS?

Edward Tufte’s style is known for its simplicity, extensive use of sidenotes,
tight integration of graphics with text, and carefully chosen typography.
[More about ET][et].

## Quick install and run

To install athena:

1. `git clone https://github.com/apas/athena.git`
1. `python3 install.py`

To run athena:

1. `source env/bin/activate`
1. `python athena.py`

athena will start a Flask server at `127.0.0.1:5000`.

To build static HTML:

1. `python athena.py build`

athena will create a new `build/` directory (it's automatically ignored by git.)

## Documentation

You can browse the full athena documentation in [the repository's wiki][wiki].

## License

MIT

[et]: https://en.wikipedia.org/wiki/Edward_Tufte
[demo]: https://apas.github.io/athena/
[wiki]: https://github.com/apas/athena/wiki
