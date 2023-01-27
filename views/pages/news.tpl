
% rebase('base', title='News Archive')

<div class="page-header">
    <h1 class="title">News Archive</h1>
    <a href="{{ get_url(system) }}">Return home</a>
    <hr />
</div>

<div class="container">
    <div class="news-post">
        <div class="header">
            <h3>Multiple Systems Anniversary</h3>
            July 12, 2022
        </div>
        <div class="content">
            <p>
                Today is exactly one year since we started tracking buses in places other than Victoria.
                We're celebrating by keeping the trend going - even more systems are now available!
            </p>
            <p>
                Starting today, you'll find <b>East Kootenay</b>, <b>Creston Valley</b>, <b>Fort St. John</b>, <b>Dawson Creek</b>, <b>Kitimat</b>, and <b>Prince Rupert</b> in the systems list.
                You may have also noticed the addition of <b>West Kootenay</b> as well as realtime information in <b>North Okanagan</b>, <b>South Okanagan</b>, and <b>Prince George</b> since the last update post.
                That brings us now to a total of <b>23</b> supported systems, which is an amazing number considering that until a year ago there was only one single system!
            </p>
            <p>
                This will likely be the last batch of new systems for a while, as BC Transit has completed the NextRide rollout in all the systems originally announced in January.
                However, if more systems are ever introduced, rest assured that we'll work hard to get them added as well!
            </p>
            <p>
                Happy tracking!
            </p>
        </div>
    </div>
    <div class="news-post">
        <div class="header">
            <h3>Spring Update</h3>
            May 1, 2022
        </div>
        <div class="content">
            <h4>New Realtime Systems</h4>
            <p>
                Since the start of this year, BC Transit has been rolling out a new NextRide program in transit systems across BC.
                We've been working hard to integrate the new API with BCTracker, which hasn't been easy as some of the data is quite different compared to existing systems.
                However, we are very pleased to announce that the first new realtime systems are active on BCTracker as of today!
            </p>
            <p>
                To start with, we're launching <b>Cowichan Valley</b>, <b>Port Alberni</b>, <b>Campbell River</b>, <b>Powell River</b>, and <b>Sunshine Coast</b> as brand-new realtime systems.
                The Central Fraser Valley and Chilliwack systems have also been combined into a new <b>Fraser Valley</b> system with realtime information.
                And on top of all that, we're introducing the <b>North Okanagan</b> and <b>South Okanagan</b> regional systems with schedule-only data.
                Expect more updates in the next few months as additional systems become available!
            </p>
            <p>
                Please keep in mind that BC Transit is still testing some components of the new NextRide API, so you may occasionally see buses with incorrect GPS positions or logged into the wrong trip.
                If you have any questions or concerns, feel free to reach out to us at <a href="mailto:james@bctracker.ca">james@bctracker.ca</a>.
                For more information about the NextRide rollout and to see what systems will be receiving it next, visit <a href="https://www.bctransit.com/nextride-faq">BC Transit's NextRide FAQ</a>.
            </p>
            <h4>Other Updates</h4>
            <p>
                Of course, new realtime systems isn't the only exciting thing we've been working on for the past few months.
                Since we posted the last update, here's some of the other changes we've made:
            </p>
            <ul>
                <li>Routes Map: View every route in a system on the map at the same time</li>
                <li>Schedules: Easily check today's schedule and upcoming buses (when available) in the overview tab of stops and routes</li>
                <li>Mobile Navigation: Updated menu makes it easier to change pages or swap to a different system</li>
                <li>Themes: Introduced new themes based on old BC transit liveries</li>
                <li>Lots of bug fixes and general improvements for the website interface</li>
            </ul>
            <p>
                We hope you enjoy the new systems and improvements, and have a great summer!
            </p>
        </div>
    </div>
    <div class="news-post">
        <div class="header">
            <h3>Winter Update</h3>
            January 2, 2022
        </div>
        <div class="content">
            <p>
                Hey everyone, it's once again time for a quick(ish) update!
            </p>
            <p>
                First of all, a huge thank you to everyone who has participated in our survey so far!
                Your feedback has been very helpful in planning upcoming additions to the site, and we're glad to know how helpful BCTracker has been for you.
                If you haven't had a chance to respond yet, you can still get to it from the link in the previous post.
            </p>
            <p>
                We've gotten a lot done over the last few months, some of which you may have already noticed, while other things have only just recently been added.
                Many of the newest features are among the most highly-requested in the survey responses, so we hope you enjoy them!
                Here's an overview of what's new:
            </p>
            <ul>
                <li>Realtime Frequency: Now updates every minute for even more accurate bus positions</li>
                <li>Global Search: An easy way to find buses, routes, and stops from anywhere on the website</li>
                <li>Upcoming Departures: Trips leaving a stop in the next 30 minutes, including realtime bus information when available</li>
                <li>Transfers and First Seen: Historic updates for when buses are transferred between systems, and when they were recorded for the first time</li>
                <li>Block/Trip History: All recorded realtime history for blocks and trips</li>
                <li>Map Improvements: Full-screen, interactive maps for buses, routes, stops, blocks, and trips</li>
                <li>Some pretty big improvements behind the scenes that made a lot of these updates possible</li>
            </ul>
            <p>
                Finally, we've updated our <a href="/about">About</a> page with some FAQs, based on some of the survey results we got back.
                We hope the answers are enlightening!
            </p>
            <p>
                As always, stay safe and have a Happy New Year!
            </p>
        </div>
    </div>
    <div class="news-post" id="survey">
        <div class="header">
            <h3>BCTracker Survey</h3>
            November 28, 2021
        </div>
        <div class="content">
            <p>
                We're running a quick survey over the next few weeks to get a better sense of who is using BCTracker, and for what purpose.
                This information will help us understand what new features should have the highest priority, as well as what improvements can be made to existing features.
                It's also a great opportunity for you to give us general feedback about things you like and things you think could be better.
            </p>
            <p>
                If you have a couple spare minutes, we would very much appreciate hearing from you.
                Thanks for supporting BCTracker!
            </p>
            <p>
                <button class="button survey-button" onclick="openSurvey()">Take the survey!</button>
            </p>
        </div>
    </div>
    <div class="news-post">
        <div class="header">
            <h3>Fall Update</h3>
            September 21, 2021
        </div>
        <div class="content">
            <p>
                Over the last couple months you may have noticed some exciting new features appearing around the website.
                We're trying to keep updates more frequent, rather than releasing massive changes once or twice per year.
            </p>
            <p>
                Since the big multi-system update earlier this summer, we've introduced:
            </p>
            <ul>
                <li>Schedule Adherence: How many minutes ahead or behind schedule a bus is (approximately)</li>
                <li>Nearby Stops: Easy transfers that are within 100m of the stop you're looking at</li>
                <li>Dark Theme: Can be set automatically based on your device's current preferences, or set manually</li>
                <li>Tablet Layouts: Specially designed for screens bigger than a phone but smaller than a computer</li>
                <li>Lots more minor improvements and fixes behind the scenes</li>
            </ul>
            <p>
                We appreciate your feedback, and we're looking forward to turning more of your suggestions into new features and improvements.
                Stay tuned for more this fall!
            </p>
        </div>
    </div>
    <div class="news-post">
        <div class="header">
            <h3>More Transit Systems</h3>
            July 12, 2021
        </div>
        <div class="content">
            <p>
                You asked for it, and we listened!
                That's right, BCTracker now supports multiple transit systems across British Columbia.
            </p>
            <p>
                We're starting with 10 cities and regions from around the province, and we plan to add more in the future.
                These initial systems include all seven currently enabled with realtime information, as well as three that only provide schedule data.
                You can easily swap between these systems at any time using the dropdown at the top right corner of your screen.
            </p>
            <p>
                In addition to all the new transit systems, we've also made a bunch of improvements to the general website design.
                System-wide realtime maps, route maps and information panels, improved desktop layouts, and many more useful features are now available!
            </p>
            <p>
                There's always more to do, and your feedback helps us figure out what comes next.
                You can send an email to <a href="mailto:james@bctracker.ca">james@bctracker.ca</a> to let us know what you like and what can be made better.
            </p>
            <p>
                Have a great summer!
            </p>
        </div>
    </div>
    <div class="news-post">
        <div class="header">
            <h3>New Deckers Out!</h3>
            April 1, 2021
        </div>
        <div class="content">
            <p>
                BCTracker has been updated to support the latest deckers, which have just entered service.
            </p>
            <p>
                Stay safe everyone!
            </p>
        </div>
    </div>
    <div class="news-post">
        <div class="header">
            <h3>New Website Look</h3>
            August 21, 2020
        </div>
        <div class="content">
            <p>
                BCTracker has a new look!
                We've been working hard to get this updated design ready, and there's a lot of new things for you to enjoy - including full mobile support, improved realtime navigation, maps, and much more.
            </p>
            <p>
                We've also moved the website to a new address at <a href="http://bctracker.ca">bctracker.ca</a>.
                The old URL will continue to be usable for a while, but if you've bookmarked any pages you'll want to make sure they're updated.
            </p>
            <p>
                Over the next few weeks we'll be making more changes to the systems that make the website work behind the scenes.
                You (hopefully) won't notice any differences, but it will allow us to add lots more new and exciting stuff in the future.
                We're always looking for ways to improve the website even more, and your feedback is always welcome.
                Send us an email anytime at <a href="mailto:james@bctracker.ca">james@bctracker.ca</a>
            </p>
            <p>
                Enjoy!
            </p>
        </div>
    </div>
</div>

% include('components/top_button')
