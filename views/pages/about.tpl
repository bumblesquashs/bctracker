
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
                            <h3>Why is there no transit information for Vancouver?</h3>
                            % include('components/toggle')
                        </div>
                        <div class="content">
                            <p>
                                Because Vancouver isn't in Alberta, silly!
                            </p>
                        </div>
                    </div>
                    <div class="section">
                        <div class="header" onclick="toggleSection(this)">
                            <h3>How long has ABTracker been recording bus history?</h3>
                            % include('components/toggle')
                        </div>
                        <div class="content">
                            <p>
                                ABTracker has been tracking buses since April 1st, 2025
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
                                The code can be found on <a href="https://github.com/bumblesquashs/bctracker/tree/af-2025-abtracker">GitHub</a> if you are interested in seeing how it works or trying to run it yourself.
                            </p>
                        </div>
                    </div>
                    <div class="section">
                        <div class="header" onclick="toggleSection(this)">
                            <h3>Will there ever be an ABTracker phone app?</h3>
                            % include('components/toggle')
                        </div>
                        <div class="content">
                            <p>
                                No.
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
                    You can also chat with us more casually on the <a href="https://discord.gg/uMbxREE5b7">ABTracker Discord server</a> where we talk about transit in Alberta and occasionally discuss upcoming features for the website.
                </p>
                <i> - James & Perrin, 2025 </i> 
            </div>  
        </div>
    </div>
</div>
