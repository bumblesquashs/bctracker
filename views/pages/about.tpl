
% rebase('base')

<div class="page-header">
    <h1 class="title">About</h1>
</div>

<div class="flex-container">
    <div class="container flex-3">
        <div class="section">
            <div class="content">
                BCTracker is a browser for the <a href="https://gtfs.org">GTFS</a> (General Transit Feed Specification) static and realtime data provided by <a href="https://bctransit.com">BC Transit</a>.
                The data is presented here for the use of whoever is interested, with the goal of making it easier to browse schedules and track down buses in communities around British Columbia. 
            </div>
        </div>
        <div class="section">
            <div class="header">
                <h2>Frequently Asked Questions</h2>
            </div>
            <div class="content">
                <div class="container">
                    <div class="section">
                        <div class="header">
                            <h3>Why is there no transit information for Vancouver?</h3>
                        </div>
                        <div class="content">
                            Transit in Vancouver is operated by <a href="https://www.translink.ca/">Translink</a> rather than BC Transit, making it harder to integrate smoothly.
                            There are numerous websites providing transit schedules and realtime information for Vancouver, including <a href="https://tcomm.bustrainferry.com/">T-Comm</a> and <a href="https://sorrybusfull.com/">Sorry Bus Full</a>.
                            BCTracker was created specifically because there were no equivalent websites for the rest of the province.
                        </div>
                    </div>
                    <div class="section">
                        <div class="header">
                            <h3>Why are some transit systems missing schedules?</h3>
                        </div>
                        <div class="content">
                            Unfortunately, BC Transit does not currently provide GTFS schedules for some of the smaller transit systems around the province.
                            This data is expected to come when NextRide finishes rolling out in these systems throughout 2024.
                            Keep an eye out for more info soon!
                        </div>
                    </div>
                    <div class="section">
                        <div class="header">
                            <h3>How long has BCTracker been recording bus history?</h3>
                        </div>
                        <div class="content">
                            Not all transit systems were added to BCTracker at the same time, so some have history going further back than others.
                            The oldest is Victoria, which was the only system available when BCTracker was created in 2020.
                            After some significant improvements to the website code in 2021, we added support for the other six transit systems with the first generation of NextRide technology.
                            This process continued in 2022 with the rollout of the second generation of NextRide.
                        </div>
                    </div>
                    <div class="section">
                        <div class="header">
                            <h3>How is BCTracker made?</h3>
                        </div>
                        <div class="content">
                            The website (both the pages and the data processing code) is written in Python using a simple web framework called Bottle.
                            The code can be found on <a href="https://github.com/bumblesquashs/bctracker">GitHub</a> if you are interested in seeing how it works or trying to run it yourself.
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="section">
            <div class="header">
                <h2>About the Developers</h2>
            </div>
            <div class="content">
                <div class="flex-column flex-gap-10">
                    <p>
                        We're a couple of software developers and transit enthusiasts from Vancouver, BC.
                        Our interest in transit systems began in 2014 when we started keeping track of the buses we rode every day.
                        Since then we've expanded our interests to photo-taking, learning the history of transit in BC, and more.
                    </p>
                    <p>
                        <b>James</b> graduated with a bachelors degree in physics from the University of British Columbia in 2020.
                        Currently he works to develop websites and other custom software for contracted clients.
                        He first started working on BCTracker in spring 2020.
                    </p>
                    <p>
                        <b>Perrin</b> graduated with a bachelors degree in information technology from Kwantlen Polytechnic University in 2019.
                        Currently he works as a mobile app developer for a construction safety startup.
                        He began helping to develop BCTracker in summer 2020.
                    </p>
                </div>
            </div>
        </div>
    </div>
    <div class="sidebar container flex-1">
        <div class="section">
            <div class="header">
                <h2>Contact</h2>
            </div>
            <div class="content">
                <p>
                    If you are curious about BCTracker, have questions, or something seems broken, you can contact us directly by emailing <a href="mailto:james@bctracker.ca">james@bctracker.ca</a>.
                    You can also chat with us more casually on the <a href="https://discord.gg/uMbxREE5b7">BCTracker Discord server</a> where we talk about transit in BC and occasionally discuss upcoming features for the website.
                </p>
                
                <br />
                <i> - James & Perrin, 2024 </i> 
            </div>  
        </div>     
    </div>
</div>
