
% rebase('base', title='About', enable_refresh=False)

<div class="page-header">
    <h1 class="title">About</h1>
    <hr />
</div>

<div class="flex-container">
    <div class="container flex-3">
        <div class="section">
            <div class="content">
                BCTracker is a browser for the <a href="https://developers.google.com/transit/gtfs">GTFS (General Transit Feed Specification)</a> static and realtime data provided by <a href="https://bctransit.com">BC Transit</a>.
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
                            <h3>Why are some transit systems not available?</h3>
                        </div>
                        <div class="content">
                            Unfortunately, BC Transit does not currently provide GTFS schedules or realtime information for some of the smaller transit systems around the province.
                            If such information becomes available in the future, we will be sure to add any new systems as soon as possible!
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
                <i> - James & Perrin, 2022 </i> 
            </div>  
        </div>     
    </div>
</div>
