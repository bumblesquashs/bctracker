
% rebase('base')

<div id="page-header">
    <h1>About</h1>
</div>

<div class="page-container">
    <div class="container flex-3">
        <div class="section">
            <div class="content">
                <p>
                    ABTracker is a browser for <a href="https://gtfs.org">GTFS</a> (General Transit Feed Specification) static and realtime data from transit agencies around Alberta.
                    The data is presented here for the use of whoever is interested, with the goal of making it easier to browse schedules and track down buses in AB communities.
                </p>
                <p>Currently, we include information from these transit agencies:</p>
                <ul>
                    % for agency in agencies:
                        <li>
                            <a href="{{ agency.website }}">{{ agency }}</a>
                        </li>
                    % end
                </ul>
            </div>
        </div>
        <div class="section">
            <div class="header" onclick="toggleSection(this)">
                <h2>Frequently Asked Questions</h2>
                % include('components/toggle')
            </div>
            <div class="content">
                <div class="container">
                    <div class="section">
                        <div class="header" onclick="toggleSection(this)">
                            <h3>Is ABTracker related to <a href="https://bctracker.ca">BCTracker</a>?</h3>
                            % include('components/toggle')
                        </div>
                        <div class="content">
                            <p>
                                Yes! BCTracker was our initial project which launched in 2020 to provide transit information to people living in British Columbia.
                            </p>
                        </div>
                    </div>
                    <div id="beta-testing" class="section">
                        <div class="header" onclick="toggleSection(this)">
                            <h3>What does it mean for ABTracker to be in beta?</h3>
                            % include('components/toggle')
                        </div>
                        <div class="content">
                            <p>
                                ABTracker started as an April Fools joke, but there was so much interest in it that we've ended up keeping it around.
                                However, it technically wasn't designed to exist as a permanent website, so there are plenty of things that may be broken.
                                We're marking the website as being in beta to make sure everyone using it is aware that it isn't perfect and problems may occur.
                            </p>
                            <p>While the site is in beta, here's what you can expect:</p>
                            <ul>
                                <li>There's a possibility that bus history may get reset at any time</li>
                                <li>Some information may appear incorrectly</li>
                                <li>Some pages may not load at all</li>
                                <li>The website may be completely unavailable at times</li>
                                <li>Features that are added to BCTracker may not get added here right away</li>
                            </ul>
                            <p>
                                Although we'll do our best to keep this website functional, please be mindful that it currently isn't our top priority.
                                If you notice any issues let us know, but it may take some time for them to be addressed.
                                We currently don't have a timeline set for how long the website will be in beta, so this notice is applicable for the foreseeable future.
                                Thanks for your understanding!
                            </p>
                        </div>
                    </div>
                    <div class="section">
                        <div class="header" onclick="toggleSection(this)">
                            <h3>How is ABTracker made?</h3>
                            % include('components/toggle')
                        </div>
                        <div class="content">
                            <p>
                                The website (both the pages and the data processing code) is written in Python using a simple web framework called Bottle.
                                The code can be found on <a href="https://github.com/bumblesquashs/bctracker/tree/abtracker">GitHub</a> if you are interested in seeing how it works or trying to run it yourself.
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="section">
            <div class="header" onclick="toggleSection(this)">
                <h2>About the Developers</h2>
                % include('components/toggle')
            </div>
            <div class="content">
                <p>
                    We're a couple of software developers and transit enthusiasts from Vancouver, BC.
                    Our interest in transit systems began in 2014 when we started keeping track of the buses we rode every day.
                    Since then we've expanded our interests to photo-taking, learning the history of transit in BC, and more.
                </p>
                <p>
                    <b>James</b> graduated with a bachelors degree in physics from the University of British Columbia in 2020.
                    Currently he works to develop websites and other custom software for contracted clients.
                </p>
                <p>
                    <b>Perrin</b> graduated with a bachelors degree in information technology from Kwantlen Polytechnic University in 2019.
                    Currently he works as a mobile app developer for a construction safety startup.
                </p>
            </div>
        </div>
    </div>
    <div class="sidebar container flex-1">
        <div class="section">
            <div class="header" onclick="toggleSection(this)">
                <h2>Contact</h2>
                % include('components/toggle')
            </div>
            <div class="content">
                <p>
                    If you are curious about ABTracker, have questions, or something seems broken, you can contact us directly by emailing <a href="mailto:james@bctracker.ca">james@bctracker.ca</a>.
                    You can also chat with us more casually on the <a href="https://discord.gg/uMbxREE5b7">BCTracker Discord server</a> where we talk about transit in BC and occasionally discuss upcoming features for the website.
                </p>
                <i> - James & Perrin, 2025 </i> 
            </div>  
        </div>
    </div>
</div>
