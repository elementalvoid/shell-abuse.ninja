Title: What the Grok!? - A Python script to convert grok epxressions to regex
Category: Regex
Tags: regex, grok, python, haproxy
Summary: I found myself needing to parse an HAProxy log file but was too lazy to write a proper regular expression by hand. I knew that Grok had HAProxy expressions so I wrote a tool to pull out the raw regular expression.

## What is Grok?
If you've never used [Grok](https://github.com/jordansissel/grok) you're missing out. It's fantastic for
parsing (semi-?)structured data using regular expressions. The basic premise is that you construct a complex
expression by peicing together smaller epxressions. Each expression could actually be a raw regex, a
collection of other expressions, or a mix of both.

## A simple example
Say you had a simple log message with an ISO8601 timestamp:
```
2016-08-17 20:07:22 - Hello there
```

### That's easy right? Right!?
Well, what if you need to parse that into the full date and time, their individual components, and the message?
You could write a [parser](https://en.wikipedia.org/wiki/Parsing#Parser) but maybe you can't hook that into an
existing toolset. Maybe you're not a developer.  Maybe your cat ate your 'Parsers for Dummies' book. BTW,
your cat is a monster.

### Enter Regex - You're winning already!
Oh. Wait. Nope, it's not quite that easy. Unless you really like regex you're probably going to be lazy and
skip the part of the spec that said you needed each component of the date. You'll end up with something like
this:
```text
^(?<date>[^\s]+) (?<time>[^\s]+) - (?<message>.*)$
```

Let's take a look at that on [regex101.com](https://regex101.com/r/hY7zK0/1) an online regex testing tool.

That's not horrible and it works. But parsing the date and time components is extra work and I'm pretty lazy sometimes.

### Enter Grok - Are we done yet?
Keep in mind this example is fairly trivial. Using Grok we have access to a [library of prebuilt patterns](https://github.com/logstash-plugins/logstash-patterns-core/tree/master/patterns)
for things like dates, numbers, text, etc.

Here's our Grok pattern:
```text
%{TIMESTAMP_ISO8601} - %{GREEDYDATA}
```

That's a minimal pattern that will match and provide most of what we're looking for. We can be more explicit
though and meet all of our requirements.

Let's break down the `TIMESTAMP_ISO8601` pattern. You'll find it defined in the
[grok-patterns](https://github.com/logstash-plugins/logstash-patterns-core/blob/master/patterns/grok-patterns) file:
```text
TIMESTAMP_ISO8601 %{YEAR}-%{MONTHNUM}-%{MONTHDAY}[T ]%{HOUR}:?%{MINUTE}(?::?%{SECOND})?%{ISO8601_TIMEZONE}?
```

Let's just enhance that a bit.
```text
%{YEAR:year}-%{MONTHNUM:month}-%{MONTHDAY:day}[T ]%{HOUR:hour}:?%{MINUTE:minute}(?::?%{SECOND:second})?%{ISO8601_TIMEZONE:timezone}? - %{GREEDYDATA:message}
```

That's a much more complete pattern and it provides names for all the items (note the `%{PATTER:name}` syntax). And, it
was still pretty easy since we modified an existing pattern.

## A non-trivial example
### HAProxy logs
HAProxy has some pretty nice logs containing tons of information. They're also well structured and should be easy to
parse. However, when you're limited to using regex it quickly becomes a nightmare. Luckily, thanks to the pattern library
we have a prebuilt pattern to parse HAProxy logs.

The log format is also [very well documented](http://cbonte.github.io/haproxy-dconv/1.6/configuration.html#8.2.3).

Let's see what a log line looks like (line breaks added):
```text
Feb  6 12:14:14 localhost \
      haproxy[14389]: 10.0.1.2:33317 [06/Feb/2009:12:14:14.655] http-in \
            static/srv1 10/0/30/69/109 200 2750 - - ---- 1/1/1/1/0 0/0 {1wt.eu} \
                  {} "GET /index.html HTTP/1.1"
```

Lot's of work went into this behind the scenes so that all we need is this Grok pattern:
```text
%{HAPROXYHTTP}
```

That's it. That's everything. It provides proper matching and named groups for all the log elements.

## That's great, but what about my regex?
Finally, we're at the end. We have a Grok pattern that properly handles our logs but we need a regex to put into some
other tool. Unfortunately, I was unable to find anything that would provide the final compiled regex of a Grok pattern.

So, I wrote one.

Before we see the code, let's see what it can do!

### How about an IP address?
Let's see what the regex looks like for an IP address:
```
# First, clone the patterns repo
git clone git@github.com:logstash-plugins/logstash-patterns-core.git

# And run the tool
./grok-to-regex.py -d logstash-patterns-core/patterns/ '%{IP:client_ip}'
(?<client_ip>(?:((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))(%.+)?|(?<![0-9])(?:(?:[0-1]?[0-9]{1,2}|2[0-4][0-9]|25[0-5])[.](?:[0-1]?[0-9]{1,2}|2[0-4][0-9]|25[0-5])[.](?:[0-1]?[0-9]{1,2}|2[0-4][0-9]|25[0-5])[.](?:[0-1]?[0-9]{1,2}|2[0-4][0-9]|25[0-5]))(?![0-9])))
```

Wow, that's a lot of regex! But, it'll match both IPV4 and IPV6 addresses and I didn't do any _real_ work. : )

### Back to HAProxy logs for a moment
Since this all started with HAProxy logs lets see what they look like.
```
./grok-to-regex.py -d logstash-patterns-core/patterns/ '%{HAPROXYHTTP}'
```
For the sake of your eyes I'm not going to insert the output here. Instead, let's take a look at it on [regex101.com](://regex101.com/r/hY7zK0/2) again.

### And now, finally, the code
It's pure python and doesn't depend on any extra bits and peices. I suspect, though YMMV, that it will work on Windows too.

<script src="https://gist.github.com/elementalvoid/59afc405f2f5726ad1980e8d8178536b.js"></script>
