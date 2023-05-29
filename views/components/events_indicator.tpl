
% dates = sorted({e.date for e in events}, reverse=True)

<div class="events">
    % for date in dates:
        <div class="date">
            <div class="tooltip-anchor">
                <div class="flex-row flex-gap-5">
                    <img class="white" src="/img/white/calendar.png" />
                    <img class="black" src="/img/black/calendar.png" />
                    <div>{{ date }}</div>
                </div>
                <div class="tooltip">{{ date.format_since() }}</div>
            </div>
        </div>
        <div class="content">
            <ul>
                % date_events = [e for e in events if e.date == date]
                % for event in date_events:
                    <li class="event">
                        <div class="flex-column flex-gap-0">
                            <div>{{ event.name }}</div>
                            % if event.description is not None:
                                <div class="smaller-font lighter-text">{{ event.description }}</div>
                            % end
                        </div>
                    </li>
                % end
            </ul>
        </div>
    % end
</div>